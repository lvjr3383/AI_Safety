"""Phase 4 $0 check on a REAL arm-A run: restore its round-4 snapshot, render round-5 seller prompts in A and WON mode
(the client records the prompt, then refuses the call) and check that WON differs from A only in communication lines,
carries NO monitoring announcement, and shows no seller messages or message fields.
    uv run python ../sprint34/verify_won_real.py <arm-A run dir>"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from verify_branch_real import changed  # noqa: E402
from verify_wo_real import OFF, round5_prompts  # noqa: E402  (renders with all treatment fields incl. comms_off_round)
from src.continuous_double_auction.snapshot import load_snapshot  # noqa: E402

NOTICE = "Regulators are now monitoring seller communications"
ALLOWED_REMOVED = re.compile(r"Messages Received|From Seller|maximum length limit|plan_for_message|message_to_sellers|new_memory")

def main(run_dir: Path) -> int:
    snap = load_snapshot(next(run_dir.glob("snapshot_after_round_*.json")))
    a, won = round5_prompts(snap, "A"), round5_prompts(snap, "WON")
    ok_diff = ok_nonotice = ok_nomsg = True
    for s in a:
        ch = changed(a[s], won[s])
        added = [l[2:] for l in ch if l.startswith("+ ")]
        removed = [l[2:] for l in ch if l.startswith("- ")]
        ok_diff &= all(ALLOWED_REMOVED.search(l) for l in removed) and [l for l in added if "new_memory" not in l] == [OFF]
        ok_nonotice &= NOTICE not in won[s]
        ok_nomsg &= "From Seller" not in won[s] and "Messages Received" not in won[s] and "message_to_sellers" not in won[s]
    checks = {"sellers": len(a) == len(won) == len(snap["params"]["seller_models"]),
              "WON_vs_A_only_communication_lines": ok_diff, "WON_no_announcement": ok_nonotice,
              "WON_no_messages_or_message_fields": ok_nomsg}
    print(json.dumps({"run": run_dir.name, **checks}))
    return 0 if all(checks.values()) else 1

if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
