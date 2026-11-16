"""Shared helpers for Experiment 2 (created during the Apart AI x Epistemics sprint, Nov 13-15 2026)."""
from __future__ import annotations
import hashlib, json, os, re, threading, time, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIGS, DATA, RESULTS = ROOT / "configs", ROOT / "data", ROOT / "results"
RAW = DATA / "raw"                       # gitignored
PRIVATE = RESULTS / "local_private"      # gitignored
LEDGER = RESULTS / "cost_ledger.jsonl"

def load_json(p): return json.loads(Path(p).read_text())
def sha256_text(s: str) -> str: return hashlib.sha256(s.encode("utf-8")).hexdigest()
def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def now_iso() -> str: return dt.datetime.now(dt.timezone.utc).isoformat()

PROMPTS = load_json(CONFIGS / "prompts.json")

def system_prompt(condition: str, prompts=PROMPTS) -> str:
    c = prompts["conditions"][condition]
    return prompts["system_template"].format(system_base=prompts["system_base"],
                                             framing=prompts["framing"][c["framing"]],
                                             intervention=prompts["intervention"][c["intervention"]])

def user_turn1(post: str, prompts=PROMPTS) -> str:
    return prompts["user_turn1_template"].format(post=post)

def redacted_turn1(row_id: int, post: str, prompts=PROMPTS) -> str:
    """Public-repo version of the first user message: post text replaced by id + hash."""
    return prompts["user_turn1_template"].format(
        post=f"[ELEPHANT AITA-YTA post omitted: row_id={row_id}, sha256={sha256_text(post)}]")

# ---------- deterministic parsing ----------
_VERDICT_RE = re.compile(r"verdict\s*[:\-]\s*\**\s*\[?\s*(.+)", re.I)
_CONF_RE = re.compile(r"confidence\s*[:\-]\s*\**\s*\[?\s*(\d{1,2})(?:\s*/\s*10)?", re.I)

def parse_verdict(text: str | None) -> str:
    if not text: return "unparsed"
    m = list(_VERDICT_RE.finditer(text))
    if not m: return "unparsed"
    v = m[-1].group(1).lower()
    v = re.sub(r"[\*\]\[_`]", "", v).strip()
    if v.count("/") >= 1 and "mixed" in v and "in the wrong" in v: return "unparsed"   # echoed the template
    if re.search(r"\bnot in the wrong\b|n['\u2019]?t in the wrong\b|\bnta\b", v): return "not_in_wrong"
    if re.search(r"\bin the wrong\b|\byta\b", v): return "in_wrong"
    if re.search(r"\bmixed\b|\besh\b", v): return "mixed"
    return "unparsed"

def parse_confidence(text: str | None):
    if not text: return None
    m = list(_CONF_RE.finditer(text))
    if not m: return None
    x = int(m[-1].group(1))
    return x if 0 <= x <= 10 else None

def rebuttal_key(initial_verdict: str) -> str:
    """Push against the model's own turn-1 stance. Unparsed is treated as Mixed (and flagged by caller)."""
    return "when_initial_verdict_not_in_wrong" if initial_verdict == "not_in_wrong" else "when_initial_verdict_in_wrong_or_mixed"

def pushed_direction(initial_verdict: str) -> str:
    return "toward_in_wrong" if initial_verdict == "not_in_wrong" else "toward_not_in_wrong"

# ---------- budget guard ----------
class BudgetExceeded(RuntimeError):
    pass

class BudgetGuard:
    """Hard cap on cumulative spend. Each call reserves its worst-case cost before it is sent;
    the reservation is replaced by the actual cost reported by OpenRouter afterwards.
    Spend is persisted in an append-only ledger so the cap spans smoke test + pilot + grading."""
    def __init__(self, cap_usd: float, ledger: Path = LEDGER):
        self.cap, self.ledger = float(cap_usd), Path(ledger)
        self.lock = threading.Lock(); self.reserved = 0.0
        self.spent = self._load()
    def _load(self) -> float:
        if not self.ledger.exists(): return 0.0
        return sum(json.loads(l).get("cost_usd") or 0.0 for l in self.ledger.read_text().splitlines() if l.strip())
    def reserve(self, worst_case: float) -> None:
        with self.lock:
            if self.spent + self.reserved + worst_case > self.cap:
                raise BudgetExceeded(f"projected {self.spent + self.reserved + worst_case:.4f} > cap {self.cap:.2f} "
                                     f"(spent {self.spent:.4f}, reserved {self.reserved:.4f})")
            self.reserved += worst_case
    def settle(self, worst_case: float, actual: float, record: dict) -> None:
        with self.lock:
            self.reserved -= worst_case; self.spent += actual or 0.0
            self.ledger.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ledger, "a") as f: f.write(json.dumps({**record, "cost_usd": actual, "cumulative_usd": round(self.spent, 6)}) + "\n")

def worst_case_cost(prompt_tokens_est: int, max_tokens: int, price_in: float, price_out: float, safety: float = 1.3) -> float:
    return safety * (prompt_tokens_est * price_in + max_tokens * price_out)

def est_tokens(text: str) -> int:
    return max(1, len(text) // 3)   # deliberately pessimistic (~3 chars/token) for the pre-call guard

# ---------- OpenRouter ----------
def _key() -> str:
    k = os.environ.get("OPENROUTER_API_KEY")
    if not k: raise RuntimeError("OPENROUTER_API_KEY not set")
    return k

def model_prices(model: str) -> tuple[float, float]:
    cache = RESULTS / "openrouter_models_snapshot.json"
    if cache.exists():
        data = load_json(cache)
    else:
        import requests
        data = requests.get("https://openrouter.ai/api/v1/models", timeout=60).json()
        cache.parent.mkdir(parents=True, exist_ok=True)
        keep = [m for m in data["data"] if m["id"] in {"openai/gpt-5.5", "google/gemini-3.1-pro-preview", "anthropic/claude-sonnet-4.6"}]
        data = {"fetched_utc": now_iso(), "data": keep}
        cache.write_text(json.dumps(data, indent=1))
    m = next(x for x in data["data"] if x["id"] == model)
    return float(m["pricing"]["prompt"]), float(m["pricing"]["completion"])

def key_status() -> dict:
    import requests
    d = requests.get("https://openrouter.ai/api/v1/key", headers={"Authorization": f"Bearer {_key()}"}, timeout=30).json()["data"]
    return {"usage_usd": d["usage"], "limit_usd": d["limit"], "limit_remaining_usd": d["limit_remaining"], "checked_utc": now_iso()}

def chat(body: dict, timeout: int = 300, retries: int = 2) -> tuple[dict | None, dict | None, float]:
    """Returns (response_json, error, latency_s). Retries only on network errors / 429 / 5xx;
    every attempt that returns is reported to the caller (no silent replacement)."""
    import requests
    t0 = time.time(); err = None
    for attempt in range(retries + 1):
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                              headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json",
                                       "X-Title": "apart-epistemics-exp2"},
                              json=body, timeout=timeout)
            j = r.json() if r.content else {}
            if r.status_code == 200 and "error" not in j:
                return j, None, time.time() - t0
            err = {"status": r.status_code, "body": j.get("error", j), "attempt": attempt}
            if r.status_code not in (408, 429, 500, 502, 503, 504): break
        except Exception as e:  # network
            err = {"status": None, "body": repr(e), "attempt": attempt}
        time.sleep(3 * (attempt + 1))
    return None, err, time.time() - t0

def usage_fields(j: dict | None) -> dict:
    if not j: return {}
    u = j.get("usage") or {}
    ctd = u.get("completion_tokens_details") or {}
    return {"prompt_tokens": u.get("prompt_tokens"), "completion_tokens": u.get("completion_tokens"),
            "reasoning_tokens": ctd.get("reasoning_tokens"), "total_tokens": u.get("total_tokens"),
            "cost_usd": u.get("cost"), "cost_details": u.get("cost_details"), "is_byok": u.get("is_byok")}
