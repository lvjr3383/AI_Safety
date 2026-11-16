"""Shared helpers for Experiment 1 (created during the Apart AI x Epistemics sprint, Nov 2026)."""
from __future__ import annotations
import hashlib, json, os, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIGS, FIXTURES, RESULTS = ROOT / "configs", ROOT / "fixtures", ROOT / "results"
RAW, SCORED = RESULTS / "raw", RESULTS / "scored"
LEDGER = RESULTS / "cost_ledger.jsonl"
# Agent workspaces live outside the repo so the sandbox can deny the whole repo (and fixture truth) wholesale.
WS_ROOT = Path(os.environ.get("EXP1_WS_ROOT", Path(os.environ.get("TMPDIR", "/tmp")) / "exp1_workspaces")).resolve()

def load_json(p): return json.loads(Path(p).read_text())
def dump_json(p, obj): Path(p).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n")
def sha256_bytes(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def sha256_text(s: str) -> str: return sha256_bytes(s.encode("utf-8"))
def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def now_iso() -> str: return dt.datetime.now(dt.timezone.utc).isoformat()

def tree_hashes(d: Path) -> dict:
    """{relative path: sha256} for every regular file under d (symlinks are recorded, never followed)."""
    d = Path(d); out = {}
    for p in sorted(d.rglob("*")):
        rel = p.relative_to(d).as_posix()
        if p.is_symlink(): out[rel] = "symlink->" + os.readlink(p)
        elif p.is_file(): out[rel] = sha256_file(p)
    return out

def append_jsonl(p, obj):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a") as f: f.write(json.dumps(obj, sort_keys=True, default=str) + "\n")

def read_jsonl(p):
    p = Path(p)
    if not p.exists(): return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]

EXPERIMENT = load_json(CONFIGS / "experiment.json")
PROMPTS = load_json(CONFIGS / "prompts.json")
SCORING = load_json(CONFIGS / "scoring.json")

def task_prompt(pressure: str, prompts=PROMPTS) -> str:
    return prompts["task"].replace("{pressure}", prompts["pressure"][pressure])

def fixture_id(seed: int, evidence: str) -> str: return f"s{seed}_{evidence}"

KEY_FILE = Path(os.environ.get("EXP1_API_KEY_FILE", Path.home() / ".config" / "exp1" / "anthropic_api_key"))

def load_api_key() -> str:
    """ANTHROPIC_API_KEY, else the private key file (chmod 600, outside the repo). The key never enters the agent sandbox."""
    k = os.environ.get("ANTHROPIC_API_KEY")
    if not k and KEY_FILE.is_file(): k = KEY_FILE.read_text().strip()
    if not k: raise RuntimeError(f"no API key: set ANTHROPIC_API_KEY or create {KEY_FILE}")
    return k

def scorer_fingerprint() -> str:
    """sha256 over the scoring code and rules; recorded on every scored row."""
    return sha256_text((ROOT / "src" / "score.py").read_text() + (CONFIGS / "scoring.json").read_text())

# ---------- budget guard ----------
class BudgetExceeded(RuntimeError):
    pass

def usage_cost(model: str, usage: dict, pricing=None) -> float:
    pr = (pricing or EXPERIMENT["pricing_usd_per_mtok"])[model]
    return (usage.get("input_tokens", 0) * pr["input"] + usage.get("output_tokens", 0) * pr["output"]
            + usage.get("cache_read_input_tokens", 0) * pr["cache_read"]
            + usage.get("cache_creation_input_tokens", 0) * pr["cache_write_5m"]) / 1e6

class BudgetGuard:
    """Hard cap on cumulative spend across every Experiment 1 run, persisted in an append-only ledger.
    Checked before each model request; a run that would start over the cap is refused."""
    def __init__(self, cap_usd: float, ledger: Path = LEDGER):
        self.cap, self.ledger = float(cap_usd), Path(ledger)
        self.spent = sum(r.get("cost_usd", 0.0) for r in read_jsonl(self.ledger))
    def check(self, next_worst_case: float = 0.0):
        if self.spent + next_worst_case > self.cap:
            raise BudgetExceeded(f"spent ${self.spent:.4f} + worst case ${next_worst_case:.4f} > cap ${self.cap:.2f}")
    def record(self, run_id: str, model: str, usage: dict, cost: float):
        self.spent += cost
        append_jsonl(self.ledger, {"ts": now_iso(), "run_id": run_id, "model": model, "usage": usage, "cost_usd": cost})
