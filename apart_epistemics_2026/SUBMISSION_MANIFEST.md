# Apart AI x Epistemics sprint: submission manifest

Two **separate** entries. The PDFs listed here are authoritative. Earlier drafts (`experiment_1_research_integrity/report/paper.md`, `report.md`, and earlier commits of either PDF) are historical only.

## Commits

| Role | Commit | Notes |
|---|---|---|
| Code/data snapshot linked from both papers' Code and Data sections | [`3086241b28ff15012c6e891e1989668810df94a1`](https://github.com/lvjr3383/AI_Safety/tree/3086241b28ff15012c6e891e1989668810df94a1/apart_epistemics_2026) | Both experiment directories integrated from current `main` (`eddbce7`), with the package editorial edits, frozen-file restore and folder README. |
| Submission PDFs (final editorial commit) | [`2645d97d4186f559ee5f9e1876e976dd96859041`](https://github.com/lvjr3383/AI_Safety/tree/2645d97d4186f559ee5f9e1876e976dd96859041/apart_epistemics_2026) | Code/Data links changed to the snapshot permalink; PDFs regenerated. No data or analysis files changed. |
| This manifest | The commit that adds this file (the tip of `apart-epistemics-2026-submission`) | Documentation only. |
| Exp 1 data/analysis provenance | `138cdd65ea7356b838ba1932921008a4c85f9bc0` | Reviewed base. Results are unchanged in the snapshot. |
| Exp 2 analysis provenance | `932bb8b5f54ee401bea2017684431ded220eba42` | The last analysis/figure commit. Results are unchanged in the snapshot. |
| Exp 2 frozen pilot snapshot | `f9f6b18` (tag `exp2-pilot-frozen-v1`) | Checked by `verify_frozen.py`. |

Branches (all retained): `apart-epistemics-2026-submission` (integration; PR to `main`), `apart-exp1-research-integrity` (PR #5), `apart-epistemics-exp2-pilot`, `frozen/*`.

## Submission PDFs

| Entry | Path (in commit `2645d97`) | SHA-256 | Pages | Main text |
|---|---|---|---|---|
| Exp 1: *When the Evidence Is Available: Testing Research Agents Against Corrupted and Falsely Verified Results* (Track 2: Trust Infrastructure) | [`experiment_1_research_integrity/report/submission/exp1_submission.pdf`](https://github.com/lvjr3383/AI_Safety/blob/2645d97d4186f559ee5f9e1876e976dd96859041/apart_epistemics_2026/experiment_1_research_integrity/report/submission/exp1_submission.pdf) | `657e2c0cf07f2fbe0ae7e3038a0b34c18191ff216ea8cd9bba6d935065662989` | 11 | Title page through Conclusion, Code and Data and Author Contributions ends on p. 7. References: p. 8. Appendix A: from p. 9. LLM Usage Statement: p. 11. |
| Exp 2: *Does Evaluation Awareness Mask Social Sycophancy?* | [`experiment_2_social_pressure/paper/exp2_submission.pdf`](https://github.com/lvjr3383/AI_Safety/blob/2645d97d4186f559ee5f9e1876e976dd96859041/apart_epistemics_2026/experiment_2_social_pressure/paper/exp2_submission.pdf) | `881a9cf72cc68ece73b3de7172ca6b1c28ec081247db2a7bd200b24f178eb25d` | 10 | Conclusion: p. 7. Code and Data and Author Contributions end on p. 8. References and Appendix A begin on p. 8. |

Both main texts end by page 8, counting the title page.

How the PDFs were made:

- **Exp 1:** `src/make_submission.py --html-only` runs the data assertions and writes `exp1_submission.html`. WeasyPrint 70.0 then renders that HTML, using Crimson Pro and Libre Baskerville. As a control, the box first re-rendered the supplied package HTML, and the text layout matched the supplied verified PDF exactly.
  - The only change after that is the Code/Data block, which now uses the snapshot permalink and the provenance commit.
  - Effect on layout: the References heading moved from the foot of p. 7 to p. 8. Main-text end, Appendix A start and the total page count are unchanged.
- **Exp 2:** exported from the official-template Google Doc after editing only the Code and Data bullets. Figures, tables and styles are untouched. Apart from those bullets, the text is identical to the supplied package PDF, and the page breaks are the same.

The SHA-256 of the supplied package PDFs was checked against `PDF_SHA256.json` before any work:

- Exp 1: `45f7e70d…f274ea`
- Exp 2: `abc5dd2f…3886d4`

## Editable sources

- **Exp 1:** `report/submission/template.html`, built by `src/make_submission.py` into `report/submission/exp1_submission.html`.
- **Exp 2:**
  - Official-template Google Doc: https://docs.google.com/document/d/1iVqX7KnkhqZdMt8XRou6V9CVPn7VkF1vqndCtH3WNRc/edit
  - Markdown mirror: `paper/manuscript.md`

## Google Drive (folder https://drive.google.com/drive/folders/1wftqwL8TI72CaEWVwsXSRdfl6fmLCXF_)

| File | Link |
|---|---|
| Exp 1 PDF | https://drive.google.com/file/d/18rvHJbfBPJnBfct9xLuJzlWc-9zWzd1i/view |
| Exp 1 source `template.html` | https://drive.google.com/file/d/1WJ6eX8GBmc1cdVHNcmECO0MgrECQb7O9/view |
| Exp 1 source `exp1_submission.html` | https://drive.google.com/file/d/1r0cYycjLUDQ0qbm1JzGzhuClwmB34J7O/view |
| Exp 1 builder `make_submission.py` | https://drive.google.com/file/d/1aC_NMcNQwMDstTMHwlrC0xyXtLpGfzkW/view |
| Exp 2 PDF | https://drive.google.com/file/d/1g7iDg1OrJalgENLGHLp_QXwVSJnm72g6/view |
| Exp 2 native Google Doc (edited in place, not replaced) | https://docs.google.com/document/d/1iVqX7KnkhqZdMt8XRou6V9CVPn7VkF1vqndCtH3WNRc/edit |
| Exp 2 Markdown mirror | https://drive.google.com/file/d/1APL32SXUT3tHxPM6CRSPIaevfvlxeNkq/view |

Both Drive PDFs were downloaded back and matched the submission files byte for byte. The repository PDFs, downloaded from `raw.githubusercontent.com` at commit `2645d97`, also matched byte for byte.

## Validation (offline only; no inference was rerun and no API credits were used)

Every check below was actually run, on 15-16 Nov 2026 (CT).

**Exp 2 (Linux box, Python 3.13):**

- `verify_frozen.py`: OK, 0 changed of 38.
  - Before the fix it reported `README.md`, `requirements.txt` and `.gitignore` as changed. Those three files were restored to `f9f6b18`. The current setup notes moved to `REPRODUCTION.md` and `requirements-analysis.txt`, and the extra ignore rules moved to `apart_epistemics_2026/.gitignore`.
- `v2_study/verify_protocol.py`: OK, 15 files.
- `v2_study_anthropic/verify_addendum.py`: OK, 11 files.
- `pytest tests v2_study/tests v2_study_anthropic/tests`: 91 passed, 1 skipped.
- `analyze_anthropic.py`, `analyze_anthropic.py --exclude-ceiling` and `report_anthropic.py`, rerun on a copy:
  - CSV, JSON and `RESULTS_TABLES.md` outputs were byte-identical to the committed files.
  - The SVG figures differ only in matplotlib metadata (date and clip-path ids).
- Headline counts recomputed from `conversation_outcomes.csv`:
  - 720 conversations: 9 moved toward the push, 17 away, 694 unchanged.
  - Toward-push by model: Haiku 3, Sonnet 0, Opus 6.
  - Pooled honesty contrast on `moved_toward_push_t3`: -0.0194 [-0.0361, -0.0028].
- `run_stats.json`:
  - 730 attempts: 720 complete, 10 interrupted.
  - 2,172 returned turn calls, a count that includes partial interrupted attempts. The analytic unit is the 720 completed conversations.

**Exp 1:**

- macOS (Jack's MacBook, `sandbox-exec` available), at commit `2645d97`: `pytest`: 88 passed.
- Linux box (no `sandbox-exec`):
  - `pytest`: 75 passed, 12 skipped (macOS sandbox required) and 1 failed: `test_v2_dry_run_pipeline` raised `FileExistsError` on a timestamped run directory. The same test passed on macOS.
  - `generate_fixtures.py --check`: OK, 10 fixtures.
  - `generate_fixtures_v2.py --check`: OK, 15 fixtures.
  - `make_submission.py --html-only`: "all data assertions passed".
- Headline counts recomputed from `results/summary/cells.csv` and `results/v2/summary/cells.csv`:
  - v1: 60 completed, 30 compromised, 0 corrupted headlines published.
  - v2: 90 completed, 60 compromised, 0 corrupted headlines published.
  - Total: 150 sessions, 90 compromised, 0 published.

**Repository hygiene:**

- `git diff --check`: clean.
- No tracked file matches the ignore rules.
- No `local_private/`, `data/raw/`, `.env` or key files are tracked.
- Pattern scan for API-key and token formats: no hits.
- The live `ANTHROPIC_API_KEY` and `OPENROUTER_API_KEY` values do not occur in the tree.
- ELEPHANT text check: 1,993 60-character snippets from the AITA-YTA posts were searched for in all tracked files under `apart_epistemics_2026/`, with 0 found.
- Relative Markdown links under `apart_epistemics_2026/` and in the root README: 0 broken.
- Every URL in both PDFs resolved to HTTP 200, including the snapshot permalinks, PR #5, both provenance commits and the references.

**Not run:**

- Any paid inference, the Exp 1 macOS Chrome PDF builder, and the Exp 2 case selection, which needs the unredistributed ELEPHANT files.
- AI audits and graders are not human validation.
