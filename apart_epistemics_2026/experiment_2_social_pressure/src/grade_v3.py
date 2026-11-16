"""Rubric v3 automated regrade of the 40 frozen pilot conversations with one AI grader.
Created during the Apart AI x Epistemics sprint, Nov 13-15 2026 (Nov 14).

Graders (configs/v3/graders_v3.json): claude_sonnet46_anthropic (direct Anthropic API, ANTHROPIC_API_KEY)
and qwen38max_openrouter (OpenRouter, OPENROUTER_API_KEY). Keys are read from the environment only and never
printed, logged or written. Each grader has its own ledger and hard cap (BudgetGuard reserves worst case first).

Input: validation_v3/local_private/blind_items.jsonl (gitignored; built by validation_v3/build_blind_input.py).
Output: results_v3/grades/<grader>.jsonl, every attempt kept, keyed by blind_id only (no conv_id, no post text,
only a hash of the grader input). Invalid outputs (bad JSON, bad labels, missing or non-verbatim required quote)
get exactly one regrade.

Usage:
  python src/grade_v3.py --grader qwen38max_openrouter --estimate      # free: model/price check + cost estimate
  python src/grade_v3.py --grader qwen38max_openrouter --run [--limit N]
"""
from __future__ import annotations
import argparse, json, os, random, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent)); sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "validation_v3"))
from common import BudgetGuard, BudgetExceeded, worst_case_cost, est_tokens, sha256_text, now_iso
from deterministic_checks import quote_in_text

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "configs/v3/graders_v3.json").read_text())
SCHEMA = json.loads((ROOT / "configs/v3/grader_schema_v3.json").read_text())
TEMPLATE = (ROOT / "configs/v3/grader_prompt_v3.txt").read_text()
ITEMS = ROOT / "validation_v3/local_private/blind_items.jsonl"
GRADES = ROOT / "results_v3/grades"
CHECKS = ROOT / "results_v3/model_checks.jsonl"
RETRY_STATUS = (408, 429, 500, 502, 503, 504, 529)

def build_prompt(item: dict) -> str:
    s = TEMPLATE
    for k in ("blind_id", "message_1", "reply_1", "message_2", "reply_2", "message_3", "reply_3"):
        s = s.replace("{" + k + "}", (item[k] or "").strip())
    return s

def allowed_for(key: str):
    a = SCHEMA["allowed"]
    if key.startswith("verdict_"): return a["verdict"]
    if key.startswith("judgment_change_") and not key.endswith("_quote"): return a["judgment_change"]
    if key.startswith("allegation_code_"): return a["allegation_code"]
    if key.startswith(("allegation_grounded", "marks_claim")): return a["yes_no"]
    return None  # quote fields

def normalise_labels(d: dict) -> dict:
    out = {}
    for k in SCHEMA["keys"]:
        v = d.get(k)
        v = "" if v is None else str(v).strip()
        if allowed_for(k) is not None: v = v.lower().replace(" ", "_").replace("-", "_")
        out[k] = v
    return out

def validate(d: dict | None, item: dict) -> list[str]:
    """Problems with one parsed grade (empty list = valid)."""
    if d is None: return ["no_json"]
    probs = [f"missing:{k}" for k in SCHEMA["keys"] if k not in d]
    d = normalise_labels(d)
    for k in SCHEMA["keys"]:
        ok = allowed_for(k)
        if ok is not None and d[k] not in ok: probs.append(f"bad_label:{k}={d[k]!r}")
    for qk, rule in SCHEMA["quote_required"].items():
        if d.get(rule["field"]) in (None, "", rule["unless"]): continue
        if not d.get(qk): probs.append(f"quote_missing:{qk}")
        elif not quote_in_text(d[qk], item[f"reply_{rule['reply']}"]): probs.append(f"quote_not_verbatim:{qk}")
    return probs

def parse_json(text: str | None):
    if not text: return None
    m = re.search(r"\{.*\}", text, re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None

def _post(url, headers, body, timeout=300):
    import requests
    r = requests.post(url, headers=headers, json=body, timeout=timeout)
    try: return r.status_code, r.json()
    except Exception: return r.status_code, {"raw": r.text[:500]}

class Grader:
    def __init__(self, name: str, poster=_post, ledger_root: Path = ROOT, out_dir: Path = GRADES):
        self.name, self.cfg, self.post = name, CFG["graders"][name], poster
        if self.cfg["provider"] not in ("anthropic", "openrouter"): raise ValueError(f"{name} is not an API grader")
        self.ledger = ledger_root / self.cfg["ledger"]; self.out = out_dir / f"{name}.jsonl"
        self.max_tokens = self.cfg.get("max_tokens", CFG["common"]["max_tokens"])
    def key(self):
        k = os.environ.get(self.cfg["api_key_env"])
        if not k: raise RuntimeError(f"{self.cfg['api_key_env']} is not set")
        return k
    def prices(self):
        p = self.cfg["price_usd_per_token"]; return float(p["input"]), float(p["output"])
    def request(self, prompt):
        if self.cfg["provider"] == "anthropic":
            return (self.cfg["endpoint"], {"x-api-key": self.key(), "anthropic-version": self.cfg["anthropic_version"], "content-type": "application/json"},
                    {"model": self.cfg["model"], "max_tokens": self.max_tokens, "temperature": CFG["common"]["temperature"],
                     "messages": [{"role": "user", "content": prompt}]})
        body = {"model": self.cfg["model"], "messages": [{"role": "user", "content": prompt}], "max_tokens": self.max_tokens,
                "temperature": CFG["common"]["temperature"], "provider": self.cfg["routing"], "usage": {"include": True}}
        if "reasoning" in self.cfg: body["reasoning"] = self.cfg["reasoning"]
        if "seed" in self.cfg: body["seed"] = self.cfg["seed"]
        return self.cfg["endpoint"], {"Authorization": f"Bearer {self.key()}", "Content-Type": "application/json", "X-Title": "apart-epistemics-exp2-v3"}, body
    def parse_response(self, status, b):
        """-> text, usage dict (tokens, cost, cost_source, response_model, request_id, provider), error"""
        if status != 200 or "error" in b or b.get("type") == "error":
            return None, {}, {"status": status, "body": b.get("error", b)}
        if self.cfg["provider"] == "anthropic":
            u = b.get("usage") or {}; pin, pout = self.prices()
            it, ot = u.get("input_tokens") or 0, u.get("output_tokens") or 0
            text = "".join(c.get("text", "") for c in b.get("content", []) if c.get("type") == "text") or None
            return text, {"input_tokens": it, "output_tokens": ot, "reasoning_tokens": None, "cost_usd": round(it * pin + ot * pout, 8),
                          "cost_source": "computed_from_list_price", "response_model": b.get("model"), "request_id": b.get("id"),
                          "served_by": "anthropic", "stop_reason": b.get("stop_reason")}, None
        u = b.get("usage") or {}; ch = (b.get("choices") or [{}])[0]
        return (ch.get("message") or {}).get("content"), {
            "input_tokens": u.get("prompt_tokens"), "output_tokens": u.get("completion_tokens"),
            "reasoning_tokens": (u.get("completion_tokens_details") or {}).get("reasoning_tokens"), "cost_usd": u.get("cost"),
            "cost_source": "openrouter_usage_cost", "response_model": b.get("model"), "request_id": b.get("id"),
            "served_by": b.get("provider"), "stop_reason": ch.get("finish_reason")}, None
    def worst_case(self, prompt):
        pin, pout = self.prices(); return worst_case_cost(est_tokens(prompt), self.max_tokens, pin, pout)
    def grade_item(self, item, guard: BudgetGuard, attempt: int) -> dict:
        prompt = build_prompt(item); wc = self.worst_case(prompt)
        guard.reserve(wc)
        status, b, text, use, err = None, {}, None, {}, None
        for i in range(3):
            try: status, b = self.post(*self.request(prompt))
            except Exception as e: status, b = None, {"error": repr(e)[:300]}
            text, use, err = self.parse_response(status, b)
            if err is None or status not in RETRY_STATUS + (None,): break
            if self.post is _post: time.sleep(5 * (i + 1))
        guard.settle(wc, use.get("cost_usd") or 0.0, {"kind": "grader_v3", "grader": self.name, "model": self.cfg["model"],
                     "blind_id": item["blind_id"], "attempt": attempt, "request_id": use.get("request_id"),
                     "cost_source": use.get("cost_source"), "input_tokens": use.get("input_tokens"),
                     "output_tokens": use.get("output_tokens"), "utc": now_iso()})
        parsed = parse_json(text)
        probs = validate(parsed, item) if err is None else ["api_error"]
        rec = {"blind_id": item["blind_id"], "attempt": attempt, "utc": now_iso(), "grader": self.name, "model_requested": self.cfg["model"],
               "prompt_template_sha256": sha256_text(TEMPLATE), "grader_input_sha256": sha256_text(prompt),
               "raw_output": text, "parsed": normalise_labels(parsed) if parsed else None, "valid": not probs, "problems": probs,
               **use, "error": err}
        self.out.parent.mkdir(parents=True, exist_ok=True)
        with guard.lock:
            with open(self.out, "a") as f: f.write(json.dumps(rec) + "\n")
        return rec

def load_items(path: Path = ITEMS):
    if not path.exists(): raise SystemExit(f"{path} missing: run validation_v3/build_blind_input.py (needs data/raw)")
    return [json.loads(l) for l in open(path)]

def prior(out: Path):
    recs = [json.loads(l) for l in open(out)] if out.exists() else []
    tmpl = sha256_text(TEMPLATE); done, natt = set(), {}
    for r in recs:
        if r["prompt_template_sha256"] != tmpl: continue
        natt[r["blind_id"]] = max(natt.get(r["blind_id"], 0), r["attempt"])
        if r["valid"]: done.add(r["blind_id"])
    return done, natt

def run(grader: Grader, items, limit=None, workers=4, max_attempts=2):
    guard = BudgetGuard(grader.cfg["cap_usd"], grader.ledger)
    done, natt = prior(grader.out)
    todo = [it for it in items if it["blind_id"] not in done and natt.get(it["blind_id"], 0) < max_attempts]
    random.Random(20261114).shuffle(todo)
    if limit: todo = todo[:limit]
    print(f"[{grader.name}] {len(todo)} to grade; ledger spend so far ${guard.spent:.4f} of cap ${grader.cfg['cap_usd']:.2f}", flush=True)
    def one(it):
        recs = []
        a = natt.get(it["blind_id"], 0)
        while a < max_attempts:
            a += 1
            try: r = grader.grade_item(it, guard, a)
            except BudgetExceeded as e: print(f"  {it['blind_id']} BUDGET STOP: {e}", flush=True); return recs
            recs.append(r)
            print(f"  {it['blind_id']} attempt {a}: {'valid' if r['valid'] else r['problems']} cost={r.get('cost_usd')}", flush=True)
            if r["valid"]: break
        return recs
    with ThreadPoolExecutor(workers) as ex: res = [r for rs in ex.map(one, todo) for r in rs]
    print(f"[{grader.name}] done: {len(res)} calls; ledger spend now ${guard.spent:.4f}", flush=True)
    return res

def free_model_check(grader: Grader, getter=None) -> dict:
    """Free model-list check (no inference). Raises if the configured model is not listed."""
    import requests
    getter = getter or (lambda url, headers: requests.get(url, headers=headers, timeout=60).json())
    if grader.cfg["provider"] == "anthropic":
        data = getter("https://api.anthropic.com/v1/models?limit=1000", {"x-api-key": grader.key(), "anthropic-version": grader.cfg["anthropic_version"]})
        ids = [m.get("id") for m in data.get("data", [])]
        rec = {"grader": grader.name, "model": grader.cfg["model"], "listed": grader.cfg["model"] in ids,
               "sonnet_ids_listed": [i for i in ids if i and "sonnet" in i], "price_check": "not available via API (list price used)"}
    else:
        data = getter("https://openrouter.ai/api/v1/models", {})
        m = next((x for x in data.get("data", []) if x["id"] == grader.cfg["model"]), None)
        pin, pout = grader.prices()
        rec = {"grader": grader.name, "model": grader.cfg["model"], "listed": m is not None,
               "listed_price": (m or {}).get("pricing", {}) and {k: m["pricing"][k] for k in ("prompt", "completion")},
               "price_matches_config": bool(m) and float(m["pricing"]["prompt"]) == pin and float(m["pricing"]["completion"]) == pout}
    rec["utc"] = now_iso()
    CHECKS.parent.mkdir(parents=True, exist_ok=True)
    with open(CHECKS, "a") as f: f.write(json.dumps(rec) + "\n")
    if not rec["listed"]: raise SystemExit(f"model {grader.cfg['model']} NOT listed: {rec}")
    return rec

def estimate(grader: Grader, items):
    pin, pout = grader.prices()
    prompts = [build_prompt(it) for it in items]
    worst = sum(grader.worst_case(p) for p in prompts)
    typ_out = 900 if grader.cfg["provider"] == "openrouter" else 600   # assumption: JSON ~500 tokens (+ low reasoning for OpenRouter)
    typical = sum(len(p) / 4 * pin + typ_out * pout for p in prompts)
    return {"n": len(prompts), "mean_prompt_chars": round(sum(map(len, prompts)) / len(prompts)), "typical_usd_one_pass": round(typical, 4),
            "typical_usd_with_all_regrades": round(2 * typical, 4), "worst_case_usd_one_pass": round(worst, 4),
            "assumptions": f"typical = chars/4 input tokens + {typ_out} output tokens per call; worst = chars/3 x1.3 safety, max_tokens output"}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--grader", required=True, choices=[k for k, v in CFG["graders"].items() if v["provider"] in ("anthropic", "openrouter")])
    ap.add_argument("--estimate", action="store_true"); ap.add_argument("--run", action="store_true"); ap.add_argument("--limit", type=int)
    a = ap.parse_args(); g = Grader(a.grader); items = load_items()
    print(json.dumps(free_model_check(g)))
    print(json.dumps(estimate(g, items)))
    if a.run: run(g, items, a.limit)

if __name__ == "__main__":
    main()
