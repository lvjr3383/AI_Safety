# V4_CHANGES (Oct 17, 2026)

v4 = `/workspace/corrected_oct17/arxiv_pack_v4/` (copied from v3; v3 and earlier untouched). Review copy: DRAFT header and watermark, built as `main_structure_review.pdf` (**9 pages**, 0 errors/warnings). `main.bbl` regenerated (11 entries).

## Summary by request
1. **Bootstrap check** (`bootstrap_check.md`, `bootstrap_check.json`, `scripts/bootstrap_check.py`). Primary interaction: 20 draws negative (0.4%), 675 exactly 0 (13.5%), 4305 positive (86.1%). The 2.5th percentile is exactly 0.0 and the 97.5th is 12.2774, so **no CI changes**. The zeros come from the 12.8% of resamples that omit both H02 and H08, the only items with yields. Wording in §6 replaced: "13.9% ≤ 0" → "13.5% are exactly 0 and 0.4% are negative (min −1.3 pp); lower bound exact". Sensitivity: 14.1% / 0.7%. Drops: no negatives.
2. **SOP wording**: removed "The SOP was applied unchanged". Borderline treatment is now described as an audit-time conservative operationalization of the existing final-commitment rule, with an example ("B is incorrect" plus A's content without naming A), a note that it is not in the original SOP, and the sensitivity variant. Limitations and appendix updated to match.
3. **Token cap**: removed "The experimental setup was not the main problem…" and inserted the requested sentence verbatim in the Discussion. Truncation per cell is in §6 (Social ON 12/40, Social OFF 4/40, Neutral OFF 2/40, Neutral ON 2/40, verified from `finish_reason`). The missing-not-at-random discussion is added in the Discussion and Limitations, with the +2.5 to +17.5 bounds.
4. **Stage 1 gate**: the Design section now states the gate exactly as coded. §6 says it still passes as originally defined (13/480 = 2.7%), then states that the corrected Llama ambiguity of 25/240 = 10.4% exceeds 10%, so the gate would in practice fail if ambiguous replies counted. Table 3 now has two rows: "as coded" (pass) and "if ambiguous counted" (corrected **fail (10.4%)**; sensitivity pass at 8.8%; original pass).
5. **Item-level old story**: confirmed one sentence only (§4: "…5 of 19…, H19 highest-leverage, leave-one-out minimum +12.4 pp"). The old values otherwise appear only in Table 3.
6. **Related Work**: new "Evaluation pipelines" paragraph citing Biderman et al. 2024 (arXiv:2405.14782, https://arxiv.org/abs/2405.14782; title and authors checked on the arXiv abs page) and Sclar et al. 2023 (arXiv:2310.11324, https://arxiv.org/abs/2310.11324; title and authors checked). The Biderman bib entry lists the first three authors plus "others", because the full list is long and its order differs across arXiv versions.
7. **Abstract**: the dense sentence is split into (a) audit set and blinding, (b) reader identity and the independence caveat, (c) result. The spine sentence is verbatim.
8. **Table 3** (Original/Corrected/Sensitivity) stays central at the top of page 5. Its caption adds "Lower bounds of 0.0 are exact" and a ‡ footnote with the gate definition.
9. Title unchanged; the line "An independent human second read of the 20 borderline rows was not performed at the time of writing." is kept.

## Every edit, old → new
### 1. Header
Old:
```latex
DRAFT FOR REVIEW (v3) --- not for submission (Oct 17, 2026)
```
New:
```latex
DRAFT FOR REVIEW (v4) --- not for submission (Oct 17, 2026)
```

### 2. Header comment
Old:
```latex
%% REVIEW COPY v3 (Oct 17, 2026). Title chosen. Abstract near-final.
```
New:
```latex
%% REVIEW COPY v4 (Oct 17, 2026). Title chosen. Abstract near-final.
```

### 3. Abstract: split audit sentence
Old:
```latex
All 50 auto-scored yields (plus 20 decoys) were re-adjudicated under the same written rule, in a condition-blinded re-adjudication by an AI assistant applying the written SOP; the reader was not fully independent of the earlier audit. It reclassified 36 as ambiguous and 2 as maintain.
```
New:
```latex
All 50 auto-scored yields, mixed with 20 decoy maintains under opaque IDs with condition, label, and run identifiers removed, were re-adjudicated against the same written rule. This was a condition-blinded re-adjudication by an AI assistant applying the written SOP; the reader was not fully independent of the earlier audit. It reclassified 36 yields as ambiguous and 2 as maintain.
```

### 4. Related work: evaluation pipelines
Old:
```latex
\textbf{Measurement validity.}
```
New:
```latex
\textbf{Evaluation pipelines.}
Implementation details of language-model evaluation, including the answer-extraction heuristics used to score generated outputs, can change both scores and the conclusions drawn from them~\citep{biderman2024lessons}. Seemingly minor formatting choices can also shift measured accuracy substantially, partly through outputs that match no valid option~\citep{sclar2023quantifying}. This paper is a concrete case on the scoring side: the generations are held fixed, and only the extraction and review layer changes.

\textbf{Measurement validity.}
```

### 5. Design: Stage 1 gate definition
Old:
```latex
Pre-set gates: Neutral $\geq$80\%; Neutral$-$Social $\geq$10~pp; empty+unscorable $\leq$10\%.
```
New:
```latex
Pre-set gates: Neutral $\geq$80\%; Neutral$-$Social $\geq$10~pp; and a scorability gate, coded as empty/error plus unscorable (no interpretable A/B) $\leq$10\% of all 480 Stage~1 rows, which did not count adjudicated-ambiguous replies.
```

### 6. Sec 6: reader/borderline operationalization
Old:
```latex
The SOP was applied unchanged. Each label carries its deciding quote, and a script confirmed every quote appears verbatim in its reply. The reader flagged 20 rows as borderline (e.g., replies that reject B and state A's content without naming A, or are cut off right after arguing for A's content). These were resolved by the most conservative reading---no clear final commitment, so ambiguous---with a sensitivity variant that keeps the reader's labels (15 ambiguous, 2 maintain, 3 yield).
```
New:
```latex
Each label carries its deciding quote, and a script confirmed every quote appears verbatim in its reply. The reader flagged 20 rows as borderline, where the written rule does not by itself settle the label: for example, ``B is incorrect'' followed by A's content without ever naming A, or a reply cut off right after arguing for A's content. For these rows I adopted an audit-time conservative operationalization of the existing final-commitment rule: a reply without a clear, explicit final A or B commitment is ambiguous. This operationalization was fixed during the audit; it is not stated in the original SOP. A sensitivity variant keeps the reader's own labels for these rows (15 ambiguous, 2 maintain, 3 yield).
```

### 7. Sec 6: Stage 1 gate statement
Old:
```latex
so the pre-set $\geq$10~pp gate now \emph{fails} (7.6~pp in the sensitivity variant); the Neutral and empty+unscorable gates still pass (the latter, 2.7\%, does not count ambiguous replies as defined). Ambiguity rose to 25/240 (10.4\%), 16 of them under Social;
```
New:
```latex
so the pre-set $\geq$10~pp gate now \emph{fails} (7.6~pp in the sensitivity variant). The Neutral $\geq$80\% gate still passes. The scorability gate, as originally coded (empty/error plus unscorable over all 480 rows, excluding ambiguous replies), also still passes as originally defined (13/480 = 2.7\%). But the corrected Llama ambiguity rate is 25/240 = 10.4\%, above 10\%: if ambiguous replies counted as unscorable, the scorability gate would in practice fail for the Llama arm. Of the 25 ambiguous replies, 16 are under Social;
```

### 8. Sec 6: bootstrap wording
Old:
```latex
interaction $+$4.2~pp [0.0, 12.3], with 13.9\% of bootstrap draws $\leq 0$.
```
New:
```latex
interaction $+$4.2~pp [0.0, 12.3]. Of the 5000 bootstrap draws, 13.5\% are exactly 0 and 0.4\% are negative (minimum $-1.3$~pp), so the lower bound of 0.0 is exact rather than a rounded negative value. The zeros arise because every Stage~2 yield is on H02 or H08: the 12.8\% of resamples that omit both items have 100\% maintain in every cell, and all their contrasts are exactly zero (the same mechanism gives the 0.0 lower bounds for both drops, which have no negative draws).
```

### 9. Sec 6: sensitivity bootstrap
Old:
```latex
The sensitivity variant gives $+$3.8~pp [0.0, 11.3].
```
New:
```latex
The sensitivity variant gives $+$3.8~pp [0.0, 11.3] (14.1\% of draws exactly 0, 0.7\% negative).
```

### 10. Sec 6: truncation / differential missingness
Old:
```latex
\textbf{Ambiguity is differential.} Ambiguity is 20/160 (12.5\%), 11 of them in Social ON, and 16 of the 20 ended at the 300-token limit. Truncation itself varied with condition: 12 of 40 Social ON replies hit the limit, against 4 of 40 in Social OFF and 2 of 40 in each Neutral cell. Coding all ambiguous rows maintain vs yield moves the interaction from $+$2.5 to $+$17.5~pp, so the corrected estimate is uncertain rather than a precise null.
```
New:
```latex
\textbf{Truncation and ambiguity are differential.} Truncation at the 300-token cap (\texttt{finish\_reason} = length) varied by cell: Social ON 12/40, Social OFF 4/40, Neutral OFF 2/40, Neutral ON 2/40. Ambiguity is 20/160 (12.5\%), 11 of them in Social ON, and 16 of the 20 ended at the cap. Coding all ambiguous rows maintain vs yield moves the interaction from $+$2.5 to $+$17.5~pp, so the corrected estimate is uncertain rather than a precise null.
```

### 11. Discussion: token cap sentence + MNAR
Old:
```latex
The experimental setup was not the main problem, but one design choice is itself a measurement issue: the 300-token cap interacted with condition, and truncation turned long Social ON replies into missing outcomes in exactly the cell the interaction depends on.
```
New:
```latex
The primary discovered failure was in scoring and review coverage, while the 300-token cap materially amplified the problem by creating condition-dependent truncation. Truncation turned long Social ON replies into missing outcomes in exactly the cell the interaction depends on. Excluding ambiguous rows from denominators treats them as missing at random, and they are not: missingness is concentrated in one cell, and a reply cut off under social pressure need not have ended where completed replies did. The $+$2.5 to $+$17.5~pp ambiguity bounds show how much the interaction depends on that untestable assumption.
```

### 12. Limitations: borderline + MNAR
Old:
```latex
Borderline rows were coded ambiguous, the most conservative reading; the sensitivity variant shows this does not change the conclusions. Truncation cannot be fixed without new generations, which I did not run; truncated replies remain missing outcomes, unevenly across cells.
```
New:
```latex
Borderline rows were coded ambiguous under an audit-time conservative operationalization of the final-commitment rule; the sensitivity variant shows this does not change the conclusions. Truncation cannot be fixed without new generations, which I did not run. Truncated replies remain missing outcomes, and their exclusion is not missing at random (Social ON 12/40 truncated vs 2--4/40 elsewhere), so the corrected estimates rest on an untestable assumption bracketed by the $+$2.5 to $+$17.5~pp ambiguity bounds.
```

### 13. Appendix: audit paragraph
Old:
```latex
Same rule, applied to all 50 auto-scored yields
```
New:
```latex
The written final-commitment rule, applied to all 50 auto-scored yields
```

### 14. Appendix: borderline
Old:
```latex
Borderline rows (20) coded ambiguous in the primary analysis; blind labels kept in the sensitivity variant.
```
New:
```latex
Borderline rows (20) coded ambiguous in the primary analysis under an audit-time conservative operationalization (no clear, explicit final A or B commitment $\rightarrow$ ambiguous); the reader's labels are kept in the sensitivity variant.
```

### 15. Appendix: bootstrap
Old:
```latex
seed 42 (\texttt{numpy.random.default\_rng}); percentile intervals.
```
New:
```latex
seed 42 (\texttt{numpy.random.default\_rng}); percentile intervals (\texttt{numpy.percentile}, linear interpolation). Draw-level diagnostics (counts of negative, exactly-zero, and positive draws) are in \texttt{bootstrap\_check.md}.
```

### 16. Table 3 Stage 1 rows
Old:
```latex
Ambiguous & 5/240 & \textbf{25/240 (10.4\%)} & 21/240 \\
```
New:
```latex
Scorability gate (as coded) & pass (2.7\%) & pass (2.7\%) & pass (2.7\%) \\
Ambiguous & 5/240 & \textbf{25/240 (10.4\%; $>$10\%)} & 21/240 \\
```

### 17. Table 3 caption
Old:
```latex
$^\dagger$Added during the corrected analysis; not part of the original locked analysis.}
```
New:
```latex
$^\dagger$Added during the corrected analysis; not part of the original locked analysis. Lower bounds of 0.0 are exact (see text).}
```

### Table 3 scorability rows (final form)
```latex
Scorability gate: as coded$^\ddagger$ & pass & pass & pass \\
\quad if ambiguous counted & pass & \textbf{fail (10.4\%)} & pass (8.8\%) \\
```

### references.bib
Added `biderman2024lessons` and `sclar2023quantifying` (arXiv misc entries).