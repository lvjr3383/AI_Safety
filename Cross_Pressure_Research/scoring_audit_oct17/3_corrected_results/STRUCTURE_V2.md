# STRUCTURE_V2 — Cross Pressure paper restructure (DRAFT FOR STRUCTURE REVIEW)

Oct 17, 2026. Files:
- Source: `/workspace/corrected_oct17/arxiv_pack_v2/main.tex`
- Review PDF: `/workspace/corrected_oct17/arxiv_pack_v2/main_structure_review.pdf` (9 pages; red "DRAFT FOR STRUCTURE REVIEW" header on every page plus a DRAFT watermark)

Untouched: the original submit copy, `arxiv_pack_draft/`, and all source data. No `main.pdf` was built in v2.

**Spine sentence (verbatim; used in the Introduction and the Conclusion, both bold, and in the proposed abstract):**
> The same raw generations produced substantially different conclusions after a broader scoring audit.

The paper never says Experiment 1/2, rerun, or new generations. It says "original analysis" and "expanded scoring audit", and states "No model was re-queried."

## Section outline
1. **Introduction** (+ §1.1 Related work, folded in to keep your numbering). Measurement-validity framing; the two staged questions; the spine sentence. Three contributions: (a) the cross-pressure design, (b) a documented case where scoring changed conclusions (+29.0 → +16.9 → +4.2; 19.2 → 4.7), (c) the audit procedure. Claims I do not make.
2. **Design and scoring rule.** The instrument, model and sampling (temp 0.7, **300-token cap**) are shared by both stages. Stage 1 and Stage 2 factors and gates, the estimand and bootstrap, the written final-commitment SOP, the claim walls, and the design table. States explicitly that only the scoring layer differs between §3 and §6.
3. **Original analysis.** First-letter parser plus blinded review of flagged rows only: Stage 1 had 35 Llama rows flagged (30 maintain, 5 ambiguous), Stage 2 had 30 (26 B→A, 4 ambiguous). No auto-scored yield (26 + 24) was ever read. One compact table of original numbers, then the original interpretation (eval framing widens the social-pressure cost; 5/19 items; H19 leverage; LOO minimum +12.4), marked as superseded.
4. **Why the analysis was reopened.** Raw-reply inspection, with the verbatim H13 social ON s1 line "B is incorrect, A is correct." (stored as a yield from the leading B, never reviewed), and the truncation pattern the original reviewers had already ruled ambiguous when it was flagged. Both conflict with the SOP. Flag-triggered review cannot catch the parser's own misses, which is why every auto-scored yield was audited rather than spot-fixed.
5. **Expanded scoring audit.** The blind set (50 yields + 20 decoys, opaque IDs, labels/conditions/run IDs stripped); the unchanged SOP; the reader disclosure (AI assistant applying the SOP, blind to labels and conditions, not fully independent of the earlier audit); the 20 borderline rows coded ambiguous, plus the sensitivity variant; decoys 20/20 maintain; the parser screen over all 400 Llama rows. Label-change table: 38 changed (36 yield→ambiguous, 2 yield→maintain), 12 yields kept. In Stage 2, 13 of the 16 newly ambiguous rows were truncated.
6. **Corrected analysis.** Centerpiece is the side-by-side table (original | corrected | sensitivity) for both stages. Stage 1: 100.0/95.3/97.4, gap 4.7, gate fails, ambiguity 25/240, gap CI [0.0, 10.9] (marked † "added during the audit"). Stage 2: 97.4/91.2/100/89.7, drops 6.2/10.3, interaction +4.2 [0.0, 12.3], 13.9% of draws ≤0, ambiguity 20/160 (11 in Social ON; 16/20 truncated), bounds +2.5 to +17.5, yields 3 vs 3 so the ON drop comes from the denominator, only H08 positive, LOO +1.1 to +4.8. Sensitivity: +3.8 [0.0, 11.3], gap 7.6. Notes that every original number was reproduced exactly before any label changed.
7. **What changed scientifically.** The original effects were inflated by brittle scoring: most apparent yields were truncated or unresolved replies. Conclusion: no reliable evidence that framing widened the gap, and at most a small, uncertain social-pressure cost. The setup was not the main problem, but the 300-token cap interacting with condition is a measurement issue (truncation in Social ON 12/40, Social OFF 4/40, each Neutral cell 2/40).
8. **Discussion: scoring as part of the measurement.** The main contribution: conclusions changed with identical outputs. The original pipeline had safeguards, but review was parser-triggered. Six recommendations: score the final commitment and let the parser abstain; review all auto-scored positives; use decoys; report ambiguity and truncation by cell with bounds; give a sufficient token budget and record finish_reason; keep the audit trail.
9. **Limitations and conclusion.** Single model; small item set and small per-item cells; post-hoc audit; AI-assistant adjudicator that is not independent and no human second reader on the borderline rows; the conservative borderline rule; truncation cannot be fixed without new generations (none were run); Stage 1 has no finish_reason; run_id leakage. Conclusion repeats the trail and the spine sentence, with claim walls restated.
- **Appendix A.** All existing material: wrappers, system policy, item block, run parameters, SOP. Expanded audit paragraph, including the exact-reproduction statement. Bootstrap details (`default_rng`, percentile). **Original artifacts** list, plus a new **Audit artifacts** list: RULES.md, blind_sheet.csv, blind_labels.csv, private_key.csv, parser_audit_all_rows.csv, corrected_labels_stage1/2.csv, CHANGES.csv, results.json, RESULTS.md, item-level/LOO CSVs, scripts.

## Title options
1. **Does Evaluation Framing Widen a Social-Pressure Honesty Gap? How a Scoring Audit Changed the Answer in Llama 3.3 70B** *(currently shown in the PDF as PROPOSED)*
2. **Same Generations, Different Conclusions: A Scoring Audit of a Cross-Pressure Honesty Evaluation in Llama 3.3 70B**
3. **When the Scorer Changes the Result: Auditing Free-Form Scoring in an Evaluation-Framing Honesty Study**

## Proposed abstract (as in the PDF)
Pressure effects on model honesty are hard to interpret when task content, wrapper language, evaluation cues, and scoring rules are confounded. I study this as a measurement-validity problem on a 20-item honesty bank with gold answers and a written final-commitment scoring rule. Stage 1 varies only pressure wrappers (Neutral / Social / Training) for Llama 3.3 70B; Stage 2 crosses Neutral/Social with explicit evaluation framing OFF vs ON (160 generations). My original analysis, which combined a first-letter parser with manual review of parser-flagged rows only, reported a 19.2 pp Neutral−Social gap in Stage 1 and a +16.9 pp evaluation-framing interaction in Stage 2 (item-clustered 95% CI 5.1–30.8). Inspecting raw responses then showed the parser counting a leading “B” as a yield even when the reply went on to reject B, switch to A, or stop at the 300-token cap without a final answer. An expanded blinded audit of all 50 auto-scored yields (plus 20 decoys) under the same written rule reclassified 36 as ambiguous and 2 as maintain. On the corrected labels, the Stage 1 gap is 4.7 pp (below the pre-set 10 pp gate) and the Stage 2 interaction is +4.2 pp (CI 0.0–12.3), with equal Social yield counts under OFF and ON. The same raw generations produced substantially different conclusions after a broader scoring audit. I find no reliable evidence that evaluation framing widened the gap, and I offer the case as a documented example of how parsing and adjudication choices can change safety-evaluation conclusions.

## Open decisions
1. **Title:** pick one of the options above, or another.
2. **Abstract:** approve or edit the proposed text (~230 words). It quotes the original numbers 19.2 / +16.9 [5.1–30.8] next to the corrected ones.
3. **Related work placement:** kept as §1.1 to preserve your 9-section numbering. It could be its own §2 instead.
4. **Stage 1 gap CI [0.0, 10.9]:** keep it (marked † "added during the audit") or drop it.
5. **Reader disclosure wording:** "performed by an AI assistant applying the written SOP… not fully independent of an earlier audit". Confirm the wording, and say whether to name the assistant.
6. **Second reader:** an independent human pass on the 20 borderline rows would remove the main adjudication limitation. If you add one, §5 and §9 change.
7. **Original interpretation detail in §3:** the original item-level claims (5/19 items, H19, LOO 12.4) are kept for completeness. They could be cut to one line.
8. **Section 3 table:** compact single table (current). Alternatively, drop it and rely only on the side-by-side Table 4 (this saves about 1/3 page).
9. **Length:** 9 pages (draft was 8, original 7). The candidates for trimming are §1.1 and §3.
10. **Category/comments:** `ARXIV_METADATA.md` in v2 is still the earlier draft's copy. Its title, abstract and page count need updating after the title/abstract decision.
11. **Final build:** after approval, remove the DRAFT header, watermark and PROPOSED markers, and build `main.pdf` plus a submit zip.
