"""Configurable grading provider for Experiment 2 (Apart AI x Epistemics sprint, Nov 13-15 2026).
Providers: 'openrouter' (default, used for the frozen pilot) and 'anthropic' (direct Messages API).
Same model (Claude Sonnet 4.6), same prompt, same settings. Each provider writes its own cost ledger.
Not used by the frozen pilot scripts. No network call happens at import; tests inject a fake HTTP poster."""
from __future__ import annotations
import json, os, time
from dataclasses import dataclass, field
from pathlib import Path
from common import BudgetGuard, worst_case_cost, est_tokens, now_iso

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/v2/grading_providers.json"

@dataclass
class GradeResult:
    text: str | None
    provider: str
    model_requested: str
    response_model: str | None
    request_id: str | None
    input_tokens: int | None
    output_tokens: int | None
    cost_usd: float | None
    cost_source: str
    error: dict | None = None
    raw_usage: dict = field(default_factory=dict)

def _requests_post(url, headers, json_body, timeout):
    import requests
    r = requests.post(url, headers=headers, json=json_body, timeout=timeout)
    try: body = r.json()
    except Exception: body = {"raw": r.text[:2000]}
    return r.status_code, body

class Provider:
    name = "base"
    def __init__(self, cfg: dict, common: dict, poster=_requests_post, ledger_root: Path = ROOT):
        self.cfg, self.common, self.post = cfg, common, poster
        self.ledger = ledger_root / cfg["ledger"]
    def api_key(self) -> str:
        k = os.environ.get(self.cfg["api_key_env"])
        if not k: raise RuntimeError(f"{self.cfg['api_key_env']} is not set (provider '{self.name}')")
        return k
    def prices(self) -> tuple[float, float]: raise NotImplementedError
    def build(self, prompt: str) -> tuple[str, dict, dict]: raise NotImplementedError
    def parse(self, status: int, body: dict) -> GradeResult: raise NotImplementedError
    def grade(self, prompt: str, guard: BudgetGuard | None = None, retries: int = 2, record: dict | None = None) -> GradeResult:
        url, headers, body = self.build(prompt)
        pin, pout = self.prices()
        wc = worst_case_cost(est_tokens(prompt), self.common["max_tokens"], pin, pout)
        if guard: guard.reserve(wc)            # raises BudgetExceeded -> caller pauses
        res = None
        for attempt in range(retries + 1):
            status, rb = self.post(url, headers, body, 300)
            res = self.parse(status, rb)
            if res.error is None or status not in (408, 429, 500, 502, 503, 504, 529): break
            time.sleep(0 if self.post is not _requests_post else 3 * (attempt + 1))
        if guard:
            guard.settle(wc, res.cost_usd or 0.0, {"kind": "grader", "provider": self.name, "model": res.model_requested,
                                                   "request_id": res.request_id, "cost_source": res.cost_source, "utc": now_iso(),
                                                   **(record or {})})
        return res

class OpenRouterProvider(Provider):
    name = "openrouter"
    def prices(self):
        from common import model_prices
        return model_prices(self.cfg["model"])
    def build(self, prompt):
        body = {"model": self.cfg["model"], "messages": [{"role": "user", "content": prompt}],
                "max_tokens": self.common["max_tokens"], "temperature": self.common["temperature"],
                "provider": self.cfg["routing"], "usage": {"include": True}}
        return self.cfg["endpoint"], {"Authorization": f"Bearer {self.api_key()}", "Content-Type": "application/json"}, body
    def parse(self, status, b):
        if status != 200 or "error" in b:
            return GradeResult(None, self.name, self.cfg["model"], None, None, None, None, None, "none (error)", {"status": status, "body": b.get("error", b)})
        u = b.get("usage") or {}
        return GradeResult(((b.get("choices") or [{}])[0].get("message") or {}).get("content"), self.name, self.cfg["model"],
                           b.get("model"), b.get("id"), u.get("prompt_tokens"), u.get("completion_tokens"), u.get("cost"),
                           "openrouter_usage_cost", None, u)

class AnthropicProvider(Provider):
    name = "anthropic"
    def prices(self):
        p = self.cfg["price_usd_per_token"]; return float(p["input"]), float(p["output"])
    def build(self, prompt):
        body = {"model": self.cfg["model"], "max_tokens": self.common["max_tokens"], "temperature": self.common["temperature"],
                "messages": [{"role": "user", "content": prompt}]}
        headers = {"x-api-key": self.api_key(), "anthropic-version": self.cfg["anthropic_version"], "content-type": "application/json"}
        return self.cfg["endpoint"], headers, body
    def parse(self, status, b):
        if status != 200 or b.get("type") == "error":
            return GradeResult(None, self.name, self.cfg["model"], None, None, None, None, None, "none (error)", {"status": status, "body": b.get("error", b)})
        u = b.get("usage") or {}
        text = "".join(c.get("text", "") for c in b.get("content", []) if c.get("type") == "text") or None
        pin, pout = self.prices()
        it, ot = u.get("input_tokens") or 0, u.get("output_tokens") or 0
        cost = round(it * pin + ot * pout, 8)
        return GradeResult(text, self.name, self.cfg["model"], b.get("model"), b.get("id"), it, ot, cost,
                           "computed_from_config_prices", None, u)

PROVIDERS = {"openrouter": OpenRouterProvider, "anthropic": AnthropicProvider}

def get_provider(name: str | None = None, poster=_requests_post, config_path: Path = CONFIG, ledger_root: Path = ROOT) -> Provider:
    cfg = json.loads(Path(config_path).read_text())
    name = name or cfg["default_provider"]
    if name not in PROVIDERS: raise ValueError(f"unknown grading provider {name!r}; choose from {sorted(PROVIDERS)}")
    return PROVIDERS[name](cfg["providers"][name], cfg["common"], poster, ledger_root)

def guard_for(provider: Provider, cap_usd: float) -> BudgetGuard:
    """Separate ledger (and spend total) per provider."""
    provider.ledger.parent.mkdir(parents=True, exist_ok=True)
    return BudgetGuard(cap_usd, provider.ledger)

def free_model_check(name: str, getter=None) -> dict:
    """Free, inference-free model-list check. NOT run automatically. Anthropic requires ANTHROPIC_API_KEY."""
    import requests
    getter = getter or (lambda url, headers: requests.get(url, headers=headers, timeout=30).json())
    p = get_provider(name)
    if name == "openrouter":
        data = getter("https://openrouter.ai/api/v1/models", {})
        return {"model": p.cfg["model"], "listed": any(m["id"] == p.cfg["model"] for m in data.get("data", []))}
    data = getter("https://api.anthropic.com/v1/models?limit=1000", {"x-api-key": p.api_key(), "anthropic-version": p.cfg["anthropic_version"]})
    return {"model": p.cfg["model"], "listed": any(m.get("id") == p.cfg["model"] for m in data.get("data", []))}
