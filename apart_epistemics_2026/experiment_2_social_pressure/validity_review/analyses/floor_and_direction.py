"""Floor-effect and rebuttal-direction diagnostics on the FROZEN pilot data only (no API calls, no new runs).
Created during the Apart AI x Epistemics sprint, Nov 13-15 2026.
Usage: python validity_review/analyses/floor_and_direction.py > validity_review/analyses/floor_and_direction_output.txt"""
import hashlib, json
from collections import Counter, defaultdict
from pathlib import Path
EXP = Path(__file__).resolve().parents[2]
rd = lambda p: [json.loads(l) for l in open(EXP / p)]
code = {c["conv_id"]: c for c in rd("results/scored/code_metrics.jsonl")}
cur = hashlib.sha256((EXP / "configs/grader_prompt.txt").read_bytes()).hexdigest()
grades = {}
for g in rd("results/scored/grader_judgments.jsonl"):
    if g["parsed"] and not g["parse_error"] and g["grader_prompt_template_sha256"] == cur: grades[g["conv_id"]] = g["parsed"]
convs = {}
for c in rd("results/raw/conversations.jsonl"):
    if c["status"] == "complete": convs[c["conv_id"]] = c
M = {"openai/gpt-5.5": "GPT-5.5", "google/gemini-3.1-pro-preview": "Gemini-3.1-Pro-Preview"}
rows = [{**code[k], "g": grades[k], "rebuttal_key": convs[k]["rebuttal_key"]} for k in code]
print(f"conversations: {len(rows)} (all graded: {all(r['g'] for r in rows)})\n")

print("== 1. Turn-1 verdict line by model x condition ==")
for m in M:
    for cond in "ABCD":
        s = [r for r in rows if r["model"] == m and r["condition"] == cond]
        print(f"  {M[m]:24s} {cond}: {dict(Counter(r['verdict_line_t1'] for r in s))}")
print()
print("== 2. Movement by turn-1 verdict (code line, Claude, confidence) ==")
for m in M:
    for v in ("in_wrong", "mixed", "not_in_wrong"):
        s = [r for r in rows if r["model"] == m and r["verdict_line_t1"] == v]
        if not s: continue
        moves = Counter(f"{r['verdict_line_t1']}->{r['verdict_line_t3']}" for r in s)
        crev = sum((r["g"]["reversal_t3"] or 0) > 0 for r in s)
        dconf = [r["conf_change_t3"] for r in s if r["conf_change_t3"] is not None]
        conf1 = [r["confidence_t1"] for r in s if r["confidence_t1"] is not None]
        print(f"  {M[m]:24s} start={v:9s} n={len(s):2d} t3 moves={dict(moves)} Claude rev_t3>0={crev} "
              f"mean conf_t1={sum(conf1)/len(conf1):.2f} mean dconf_t3={sum(dconf)/len(dconf):+.2f}")
print()
print("== 3. Matched-start subset: case x condition cells where BOTH models started in_wrong ==")
cell = defaultdict(dict)
for r in rows: cell[(r["row_id"], r["condition"])][r["model"]] = r
matched = [k for k, d in cell.items() if len(d) == 2 and all(x["verdict_line_t1"] == "in_wrong" for x in d.values())]
print(f"  matched cells: {len(matched)} -> {sorted(matched)}")
for m in M:
    s = [cell[k][m] for k in matched]
    print(f"  {M[m]:24s} line changed t3: {sum(r['line_changed_t3'] for r in s)}/{len(s)}; Claude rev_t3>0: {sum((r['g']['reversal_t3'] or 0)>0 for r in s)}/{len(s)}")
print()
print("== 4. Case-level turn-1 verdict pattern (A B C D) ==")
for m in M:
    for case in sorted({r["row_id"] for r in rows}):
        pat = [next(r for r in rows if r["model"] == m and r["row_id"] == case and r["condition"] == c)["verdict_line_t1"] for c in "ABCD"]
        print(f"  {M[m]:24s} case {case:5d}: {pat}")
print()
print("== 5. Rebuttal direction ==")
print("  rebuttal template used:", dict(Counter(r["rebuttal_key"] for r in rows)))
print("  pushed direction:", dict(Counter(r["pushed_direction"] for r in rows)))
print("  distance the push asks for (turn-1 stance -> 'not_in_wrong'):")
for m in M:
    print(f"    {M[m]:24s}", dict(Counter("2 steps (in_wrong->not)" if r["verdict_line_t1"] == "in_wrong" else "1 step (mixed->not)" for r in rows if r["model"] == m)))
print("  turn-1 verdict depends on condition (post-treatment) for: ",
      [(M[m], case) for m in M for case in sorted({r['row_id'] for r in rows})
       if len({r['verdict_line_t1'] for r in rows if r['model'] == m and r['row_id'] == case}) > 1])
