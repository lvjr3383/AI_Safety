# Red-team pass 3: cross_pressure_v9_review.tex as staged for publication (Nov 18 2026)

Fresh reviewer. Read-only on inputs; no project script run; no model queried; nothing checked online.
Own code: `/home/claude/redteam3/recompute.py`, `check2.py` (run with `python3 -I`). The paper was recompiled from a copy in `/home/claude/redteam3/tex/`.
`V9` = `paper_v9/cross_pressure_v9_review.tex`, `GEN` = `paper_v9/v9_generated.tex`, `PKG` = `scoring_audit_nov17_symmetric/` (all under `/home/claude/package_staging/Cross_Pressure_Research/`).

Counts: 0 BLOCKER, 4 MAJOR, 17 MINOR. No numeric mismatch anywhere.

## Findings

| ID | Sev | Location | Evidence | Minimal fix |
|---|---|---|---|---|
| G1 | MAJOR | `PKG/PROVENANCE_AND_CONFLICTS.md:21-22` | "Readers did not see: ... gold answer". False for Readers 1-2 (V9:227; `READER12_PROMPT.md:26`; `DECISION_LOG.md:29`) and unrecorded for Reader 3. Line 21 says they saw "the locked rule", which is the file that states gold = A. A packaged file asserts the gold-blindness the paper retracts. | Remove "gold answer" from line 22; add "Readers 1-2 saw the gold answer in the rule file; Reader 3 not recorded." |
| G2 | MAJOR | V9:71 "one named response class is shown to decide the sign of the estimate" (new sentence, related-work refresh) | Overclaim. Under strict-U2 the sign is negative for one of three readers only (R1 +12.6, R2 +3.8, R3 -2.3). R3's value rests on 3 yields, all H02; no item has a negative item-level interaction (0 positive, 0 negative of 16); 62.4% of draws are below zero and 37.6% exactly zero, from pooled denominators. V9:239 itself says this. | "...is shown to move the estimate between -2.3 and +12.6 depending on reader." |
| G3 | MAJOR | V9:50 "three blinded model readers", "A third blinded reader" (GEN:54); V9:62(d) "separate blinded readers"; GEN:48; V9:274 "three blinded model readers" | "Blinded" is unqualified in abstract, contributions and conclusion, while V9:227 says Readers 1-2 saw the gold answer and Reader 3 was run by the unblinded author after results were known, packet not recorded. The paper uses "condition-blinded" for the October reader (V9:122) and the stronger word for the readers known to have seen gold. Residue of REDTEAM_2 F4. | "condition-blinded" in those five places (two are in `make_tables.py` lines 58 and 68). |
| G4 | MAJOR | V9:274 (Conclusion); also V9:60 and V9:62(b) | Conclusion gives the symmetric result as "7.7-10.3 pp and +9.7 to +12.2 pp" and says only that it "changes again (Table 6)". The abstract and V9:241 give the strict-U2 range -2.3 to +12.6. Conclusion and Introduction therefore present the primary coding as the symmetric finding and never state that the strict coding spans a sign change. Residue of REDTEAM_2 F2. | Add "(to -2.3 to +12.6 across readers)" after "changes again" at 274, and the same range at 60 and 62(b). |
| g1 | MINOR | V9:62(c) "reproduces its estimate only under one of that rule's predeclared codings, for some readers" (the F1 fix) | "Some readers" is one reader. R2 strict-U2 gives +3.8, which equals the October first-reader sensitivity (same cells) and not the +4.2 primary; R1 gives +12.6, R3 -2.3. No reader reproduces the Stage 1 4.7 (3.2, 6.2, 3.2). | "comes close to its Stage 2 estimate only under the strict-U2 coding, for one of three readers". |
| g2 | MINOR | V9:241 "the symmetric intervals are wide enough to include it" (REDTEAM_2 m2, not fixed) | True for the 3 primary intervals, R1 strict, R2 and R3 semantic. False for R1 semantic [0.0, 15.0], R2 strict [0.0, 11.3], R3 strict [-7.0, 0.0], agreement-only [0.0, 16.8]. | "the symmetric primary intervals". |
| g3 | MINOR | V9:235 "the interval excludes zero for 3 of 3 readers" (Stage 1 gap) | Primary coding only. Under strict-U2 the Stage 1 lower bound is 0.0 for all three readers. The interaction parenthesis names strict-U2 but not R1 semantic [0.0, 15.0]. | Add "under the primary coding" to the Stage 1 clause. |
| g4 | MINOR | V9:227 "Label files were hashed before labels were joined to conditions" (REDTEAM_2 m3, not fixed) | Reader 3 files came through the unblinded author and were hashed at ingestion (manifest 23:45:04Z). | "Reader 3's files were hashed on ingestion, after passing through the author." |
| g5 | MINOR | V9:265 / GEN:52 | Not recorded and not stated: whether Reader 3 used a fresh chat, memory off, one chat per chunk, no retries (`HOW_TO_RUN.md` asks for all four). | One clause in Limitations. |
| g6 | MINOR | V9:239 | Overlap sentence appears twice in one paragraph ("8 ... of 23" via `\SymUtwoOverlap` and again in `\ThirdReaderStrictNote`). The low overlap is driven by Reader 2: R1 and R3 share 14 of 20; R1-R2 8 of 20; R2-R3 9 of 21. | Drop one copy; optionally give the pairwise figures. |
| g7 | MINOR | V9:50, 102 "manual review" (REDTEAM_2 m9, not fixed) | V9:265 and 271 say the original adjudicator is not recorded. | "review". |
| g8 | MINOR | `PKG/scripts/analyze.py:1` (REDTEAM_2 m5, not fixed) | Header "Written BEFORE reader labels were opened"; V9:227 says two bugs were fixed after unblinding. | Correct the header. |
| g9 | MINOR | `PKG/scripts/finalize.sh:5,10-12` | Hard-codes `/home/claude/sym` and `/home/claude/lvjr3383/...`; expects `paper_v9` inside the audit folder, which is not the package layout; needs `reader3_incoming` CSVs that are not shipped. It is the only script with an absolute private path. | Header line: "historical record of the run; not runnable outside the original workspace". |
| g10 | MINOR | V9:390-405 and `PKG/README.md` | Every listed file exists. In the package but unlisted: `out/second_reader_map_by_text.csv` (required by `analyze.py` and `analyze_v1_as_run.py`), `out/symmetric_labels_unblinded.csv`, `out/symmetric_ledgers_stage{1,2}.csv`, `out/run_FINAL.log`. README layout says `out/reader*/chunk*/data/` but reader3 has no `data/`. README omits `build_v9.py`, `check_explicit_commitment.py`, `ENVIRONMENT.txt`. | Add the four files to the list; fix the README line. |
| g11 | MINOR | `PKG/README.md:9-11` | Argument order matches all three scripts. `analyze_final.py` reads `out/second_reader_id_map.csv`, which `second_reader_repro.py` writes; README runs them in the other order. Works only because the map is shipped. | Put the `second_reader_repro.py` line first. |
| g12 | MINOR | `PKG/reader3_packet_v2/HOW_TO_RUN.md:15`; `RULES_LOCKED.md:34`; `DECISION_LOG.md:28` | Archived statements now contradicted by the record: "Reader 3 is therefore the only reader not shown the gold answer"; "Readers are not told this"; "identical rule and prompt". | One README line noting these are archival and superseded by DECISION_LOG entries 29, 33, 38. |
| g13 | MINOR | `PKG/scripts/make_tables.py:62` | "no item has a negative item-level interaction" is a fixed string, not computed from `items_neg`. True for the frozen data. | Assert `items_neg == []` before writing it. |
| g14 | MINOR | GEN:61, 92 (REDTEAM_2 m6) | 8.750 prints 8.8 and 1.250 prints 1.2. | Note or two decimals. |
| g15 | MINOR | Table 6 rows "Ambiguity bounds", "Items with ...", "Leave-one-out" (REDTEAM_2 m8) | Primary coding only, unlabelled. Under R3 strict-U2: 0 of 16 items positive, leave-one-out -2.7 to 0.0, bounds -2.5 / +17.5. | "(primary)". |
| g16 | MINOR | V9:33 | PDF header "DRAFT FOR REVIEW (v9) --- not for submission (Nov 18, 2026)" on pages 2-14. | Remove at submission. |
| g17 | MINOR | V9:277-292 bibliography | Metadata of the five new entries cannot be confirmed from the package and `DECISION_LOG.md:39` says only abstracts were read: Baek "PMLR 306:5125--5143"; Arellano author list and workshop name; Messing arXiv number; Molfese arXiv number. | Author to verify each against the source. |

## Task 1: REDTEAM_2 F1-F8

| ID | Status | v9 line |
|---|---|---|
| F1 | FIXED | 62(c) reworded; 193 "depends on how a 'B' that is never retracted ... gets coded"; 241 gives all four values including `\SymStrictRange`. Residual g1. |
| F2 | PARTIALLY | 239 / GEN:50 adds "rests on 3 Stage 2 yields, and no item has a negative item-level interaction; its difference from Reader 1 comes from basis codes, not labels". All three statements verified. Conclusion 274 not changed (G4). |
| F3 | FIXED | 265 + GEN:52. Residual g5. |
| F4 | PARTIALLY | GEN:48 "added after the Reader 1-2 results were known ... prompt adapted ... no transcript was archived"; 227 "not recorded"; both packets shipped. "blinded" still unqualified (G3). |
| F5 | FIXED | 390-405; every listed file present. Residual g9, g10. |
| F6 | FIXED | `\resizebox` at GEN:59, 72, 88; 0 Overfull boxes on recompilation; tables inside margins on page 8. |
| F7 | FIXED | 235 "fails for 2 of 3 readers (Reader 1 fails; Reader 2 passes; Reader 3 fails)"; "under this primary coding ... the strict-U2 coding below does not preserve that". Residual g3. |
| F8 | FIXED | 248 "Readers agree closely on labels ... but not on which rows belong to the decisive class". |

New false or overclaimed statements introduced by the fixes: g1 (from F1), G2 (from the related-work refresh), g6 (duplicate from F2/F8). PROVENANCE file (G1) predates the fixes and was not updated.

## Task 2: recomputation

All reproduce from row-level label files; no bootstrap replicate dropped in any ledger.
- Abstract/conclusion: 19.2; +16.9 [5.1, 30.8]; 4.7; +4.2 [0.0, 12.3]; 7.0; +3.6; 36 and 2 of 50; 149 rows; R1 +9.7 [0.7, 20.7]; R2 +11.9 [2.7, 23.5]; R3 7.7 and +12.2 [2.8, 24.3]; strict +12.6 [0.0, 31.7], +3.8 [0.0, 11.3], -2.3 [-7.0, 0.0].
- Ranges: Stage 1 gap 7.673, 10.312, 7.673 gives 7.7-10.3; interaction 9.702, 11.881, 12.199 gives +9.7 to +12.2; strict 12.632, 3.808, -2.311 gives -2.3 to +12.6.
- Gate: R1 fail, R2 pass, R3 fail (2 of 3 fail).
- U2: 16 / 12 / 18, all labelled B; R1 and R2 8 of 20; all three 8 of 23.
- R3 strict-U2: cells 37/37, 32/34, 39/39, 27/28; 3 yields (H02 Social OFF 2, H02 Social ON 1); 16 items defined, 0 positive, 0 negative.
- Agreement 143/149 (0.92), 148/149 (0.99), 144/149 (0.94), all three 143. Strata 56/56, 34/34, yields 23/23/4, 23/23/4, 24/22/4. 56 adjudicated maintains all open with "B"; 251 unread rows all auto-maintain opening with "A". Quotes verbatim 149/149 for each reader.

## Task 3: wording checks

No sentence claims a true effect, a null, a majority vote, human readers, independence of same-family readers, or new generations. Gold-blindness: paper body is correct (227); the unqualified "blinded" (G3) and the PROVENANCE file (G1) are the exceptions. Reader 3 description matches the record (name as reported, packet not recorded, after results known, no transcript); g5 lists what is missing. Abstract and Section 7 agree; Conclusion omits the strict range (G4).

## Task 4: citations

(a) 16 keys cited, 16 `\bibitem`s, exact match both ways.
(b) Sentences to verify against the full papers:
1. V9:69 "\citet{baek2026} argue that behavior changes under evaluation cues can reflect sycophancy toward researchers rather than strategic awareness".
2. V9:71 "an instruction-tuned model's first-token choice often differs from the answer in its generated text \citep{wang2024}". As I recall it, the cited paper's headline is that text answers are more robust than first-token answers; the mismatch result belongs mainly to the same group's earlier paper "My Answer is C". "First-token" there means first-token probabilities, not the leading letter of generated text as in this paper.
3. V9:71 "extraction strategies, including LLM-based extractors, can produce misleading comparisons \citep{molfese2025}" ("misleading comparisons" is the author's wording).
4. V9:71 "holding responses fixed while varying the grader and rubric shifts jailbreak attack-success rates substantially, leading \citet{arellano2026} to treat the judge--rubric pair as part of the metric".
5. V9:71 "\citet{messing2026} argues that conventional intervals omit variance from judge, prompt and sampling choices that can reverse conclusions".
6. V9:274 "That scoring is part of the measurement is an established point \citep{biderman2024,arellano2026,messing2026}" (one workshop paper and one preprint cited for "established").
7. Bibliography metadata (g17).

## Task 5: package

All files named in the appendix and README exist. Both manifests match (9 of 9 sha256; rule hash f085892d...9155a53). README argument order matches the scripts. Only `finalize.sh` has absolute private paths. Unlisted files in g10. `ENVIRONMENT.txt` matches this machine (python 3.13.18, pandas 3.0.5, numpy 2.5.3). `RULES_FOR_READER.md` equals `RULES_LOCKED.md` minus the final section; sheets are byte-identical across readers 1-2 and both packets.

## Task 6: PDF

Packaged PDF text equals a fresh compilation of the packaged tex. No undefined reference, no "??", 0 overfull boxes, tables within margins. DRAFT header on pages 2-14 (g16).
