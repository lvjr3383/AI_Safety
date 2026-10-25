"""
Verify a real round-4 snapshot without any model calls:
  1. restore it into a freshly built market and re-serialise -> must equal the file;
  2. its market rounds must equal rounds 1..k in the run's auction_results.md;
  3. each agent's memories / scratchpad must equal what the agent wrote in its logged responses up to round k.

    uv run python ../sprint34/verify_snapshot.py <run dir>
"""

import json
import random
import re
import sys
from pathlib import Path

from src.continuous_double_auction.cda_types import ExperimentParams
from src.continuous_double_auction.market.agents import LMBuyer, LMSeller
from src.continuous_double_auction.market.market import Market
from src.continuous_double_auction.snapshot import load_snapshot, restore_state, snapshot_state
from src.resources.model_wrappers import ModelWrapper


# Amendment 2026-10-24 (WO_FOLLOWUP_PROTOCOL.md §8): fields added to the code after the A snapshots were saved.
# A re-serialised snapshot may contain these, and ONLY these, extra keys, and only with these default values.
ALLOWED_NEW_PARAMS = {"comms_off_round": None}
ALLOWED_NEW_ROUND = {"seller_messaging_off": False, "seller_messages_attempted": {}}


def _compat(new: dict, old: dict, allowed: dict, where: str, problems: list) -> None:
    """Every key in `old` must be equal in `new`; keys only in `new` must be allowlisted and hold their default."""
    for k in old:
        if k not in new:
            problems.append(f"{where}: missing field {k}")
        elif new[k] != old[k]:
            problems.append(f"{where}: field {k} differs")
    for k in set(new) - set(old):
        if k not in allowed:
            problems.append(f"{where}: unexpected new field {k}")
        elif new[k] != allowed[k]:
            problems.append(f"{where}: new field {k} has non-default value {new[k]!r}")


def compat_equal(again: dict, snap: dict) -> list:
    """Snapshot round-trip comparison under the schema-compatibility amendment. Returns a list of problems ([] = equal)."""
    problems = []
    if set(again) != set(snap):
        problems.append(f"top-level keys differ: {sorted(set(again) ^ set(snap))}")
    for k in set(again) & set(snap):
        if k == "params":
            _compat(again[k], snap[k], ALLOWED_NEW_PARAMS, "params", problems)
        elif k == "market":
            a, o = again[k], snap[k]
            if set(a) != set(o):
                problems.append(f"market keys differ: {sorted(set(a) ^ set(o))}")
            for mk in set(a) & set(o):
                if mk == "rounds":
                    if len(a[mk]) != len(o[mk]):
                        problems.append("market.rounds length differs")
                    for i, (ra, ro) in enumerate(zip(a[mk], o[mk])):
                        _compat(ra, ro, ALLOWED_NEW_ROUND, f"market.rounds[{i}]", problems)
                elif mk == "current_round":
                    _compat(a[mk], o[mk], ALLOWED_NEW_ROUND, "market.current_round", problems)
                elif a[mk] != o[mk]:
                    problems.append(f"market.{mk} differs")
        elif again[k] != snap[k]:
            problems.append(f"{k} differs")
    return problems


class NoCallClient(ModelWrapper):
    def generate(self, messages):
        raise RuntimeError("verification must not call a model")


def logged_agent_state(md: Path, k: int) -> tuple[dict, str]:
    mem, pad = {}, ""
    for rnd, js in re.findall(r"## Response: Round (\d+) - .*?\n````json\n(.*?)\n````", md.read_text(), re.S):
        if int(rnd) > k:
            continue
        d = json.loads(js)
        if d.get("new_memory"):
            mem[str(int(rnd))] = d["new_memory"]
        if d.get("scratch_pad_update"):
            pad = d["scratch_pad_update"]
    return mem, pad


def main(run_dir: Path) -> int:
    snap_file = next(run_dir.glob("snapshot_after_round_*.json"))
    snap = load_snapshot(snap_file)
    k = snap["snapshot_after_round"]
    params = ExperimentParams(**snap["params"])
    agents = {a["id"]: (LMSeller if a["role"] == "seller" else LMBuyer)(
        id=a["id"], company=a["company"], valuation=a["valuation"], expt_params=params, client=NoCallClient("none"))
        for a in snap["agents"]}
    sellers = [agents[a["id"]] for a in snap["agents"] if a["role"] == "seller"]
    buyers = [agents[a["id"]] for a in snap["agents"] if a["role"] == "buyer"]
    market = Market(sellers=sellers, buyers=buyers, announce_round=params.announce_round, cap_round=params.cap_round,
                    cap_chars=params.cap_chars,
                    overseer_rng=random.Random(params.seed) if params.seed is not None else None)
    restore_state(snap, market, [*sellers, *buyers])
    problems = compat_equal(snapshot_state(market, params, k), snap)
    checks = {"roundtrip_equal": not problems}

    logged = [json.loads(b) for b in re.findall(r"````json\n(.*?)\n````", (run_dir / "auction_results.md").read_text(), re.S)]
    checks["rounds_match_auction_log"] = snap["market"]["rounds"] == logged[:k]
    checks["no_treatment_in_prefix"] = all(not r["monitoring_notice_active"] and not r["cap_active"] for r in logged[:k])
    agent_ok = True
    for a in snap["agents"]:
        mem, pad = logged_agent_state(run_dir / f"{a['id']}.md", k)
        agent_ok &= (a["memories"] == mem and (a["scratch_pad"] or "") == pad)
    checks["agent_memory_scratchpad_match_logs"] = agent_ok
    print(json.dumps({"run": run_dir.name, "snapshot": snap_file.name, **checks, "roundtrip_problems": problems[:5]}))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
