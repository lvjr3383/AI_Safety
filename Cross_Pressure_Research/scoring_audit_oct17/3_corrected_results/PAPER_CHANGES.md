# PAPER_CHANGES — draft main.tex vs original (Oct 17, 2026)

Original: `/workspace/Cross_Pressure_Research/arxiv_pack/main.tex` (identical to Mac `pilot02_out/arxiv_pack/main.tex`), not modified.
Draft: `/workspace/corrected_oct17/arxiv_pack_draft/main.tex` (compiles; 8 pages vs 7). Full unified diff: `paper_diff.txt`.

## Claims that no longer hold (wording revised)

1. **Title** — "Evaluation Framing *Widens* a Social-Pressure Honesty Gap" is no longer supported (interaction +4.2 pp, CI [0.0, 12.3]). Draft title is a question: "Does Evaluation Framing Widen a Social-Pressure Honesty Gap in Llama 3.3 70B?" — author's call; flagged.
2. **Stage 2 headline** — "framing widened the gap 13.0 → 29.9 pp, interaction +16.9 [5.1, 30.8]" → 6.2 → 10.3 pp, +4.2 [0.0, 12.3]; draft now says *no reliable evidence* framing widens the gap.
3. **Interaction CI excludes 0** → CI lower bound is 0.0; 13.9% of resamples ≤ 0.
4. **Stage 1 "establishes / locks a within-model social-pressure cost" (19.2 pp)** → 4.7 pp, "small"; supplementary item-clustered CI [0.0, 10.9] (NEW statistic, same procedure as Stage 2; removable).
5. **Stage 1 "Design gates … all passed"** → Neutral−Social ≥10 pp gate now FAILS (4.7 pp; 7.6 in sensitivity). Neutral ≥80% and empty+unscorable ≤10% (2.7%, ambiguous not part of gate as coded) still pass.
6. **"concentrated under social pressure and in a minority of items (5 of 20)"** → only 1 item (H08) has positive item interaction; 4 items undefined (no usable Social ON).
7. **"H19 is highest-leverage; LOO min leaving out H19 12.4"** → H19 has no usable Social rows (and no usable Neutral OFF rows); LOO min is leaving out H08 (+1.1), max H04 (+4.8); never ≤0.
8. **"Neutral remained high under ON (97.5%) — not a global honesty collapse"** → Neutral ON 100.0% (39/39); the 'not a global collapse' framing dropped because there is no effect to contrast with.
9. **Ambiguity bound "moves only to +15.0 vs +20.0, sign unchanged"** → +2.5 vs +17.5; sign unchanged but size highly ambiguity-dependent (ambiguity concentrated in Social ON, 11/40; truncation 12/40 in Social ON vs 2–4/40 elsewhere).
10. **"Blinded adjudication mattered (26/30 B→A recoveries)"** → kept as history, extended: +29.0 → +16.9 (original review) → +4.2 (re-adjudication of auto-scored yields). The 26/30 figure is still correct for the original review pass but that pass never saw the 24 auto-scored yields.
11. **"Stage 2 OFF directionally tracks/replicates Stage 1's 19.2 pp"** → OFF 6.2 vs Stage 1 4.7; 'directional comparison'.
12. **Conclusion / contribution** reframed: the measurement-validity contribution is now that first-letter auto-scoring produced most of the initial effects.
13. **Limitations** now state: post-hoc correction; single reader not fully independent; borderline→ambiguous coding; 300-token truncation causes differential ambiguity.

## Added text
- Design section: new paragraph **Scoring correction (post-hoc re-adjudication)** describing parser behavior, blind set (50 yields + 20 decoys), withheld fields, borderline→ambiguous rule, sensitivity variant, decoy result, parser screen, counts (12 yield / 2 maintain / 36 ambiguous), truncation (13/16 Stage 2 newly ambiguous at 300 tokens).
- **Disclosure to review:** the draft states the re-adjudication reader was "an AI assistant applying the written SOP" (true: the blind pass was done by Grok Bot), and that it is not fully independent of the earlier audit. Edit wording if you prefer, but do not describe it as a human pass.
- Appendix: new **Re-adjudication** paragraph; bootstrap RNG note (`numpy.random.default_rng`, percentile CIs — verified by exact reproduction); corrected artifacts added to manifest.

## Unchanged on purpose
Claim walls paragraph; Related Work; design schematic; wrappers/SOP verbatim; GPT-OSS 94.2% (GPT-OSS rows not re-adjudicated; it had 0 yields); bibliography (main.bbl byte-identical after bibtex).

## Rounding note
Drop ON 10.34 − Drop OFF 6.19 = 4.15 → printed +4.2, while 10.3 − 6.2 = 4.1. Same convention as original (unrounded difference).

## Every edit, old → new (25 edits)

### 1. Title
**Old:**
```latex
\title{Evaluation Framing Widens a Social-Pressure Honesty Gap in Llama~3.3~70B}
```
**New:**
```latex
\title{Does Evaluation Framing Widen a Social-Pressure Honesty Gap in Llama~3.3~70B?}
```

### 2. Abstract
**Old:**
```latex
For Llama~3.3~70B, adjudicated maintain rates were 96.2\% Neutral, 76.9\% Social, and 93.7\% Training (Neutral$-$Social \textbf{19.2~pp}).
```
**New:**
```latex
For Llama~3.3~70B, re-adjudicated maintain rates were 100.0\% Neutral (75/75), 95.3\% Social (61/64), and 97.4\% Training (74/76) (Neutral$-$Social \textbf{4.7~pp}, below the pre-set 10~pp design gate).
```

### 3. Abstract
**Old:**
```latex
Post-adjudication, the Neutral$-$Social gap widened from \textbf{13.0} to \textbf{29.9}~pp under ON---an interaction of \textbf{$+$16.9~pp} (item-clustered 95\% CI \textbf{5.1--30.8}). Neutral remained high under ON (97.5\%), so the effect is not a global honesty collapse; the interaction concentrates under social pressure and in a minority of items. Blinded adjudication mattered (26/30 review rows were B$\rightarrow$A recoveries). I do not claim evaluation awareness as a mechanism or generalize across models. Stage~2 OFF directionally tracks Stage~1's social-pressure cost without reproducing its point estimate.
```
**New:**
```latex
After re-adjudication, the Neutral$-$Social gap was \textbf{6.2}~pp under OFF and \textbf{10.3}~pp under ON---an interaction of \textbf{$+$4.2~pp} whose item-clustered 95\% CI (\textbf{0.0--12.3}) reaches zero. Social OFF and Social ON each contain three yields, all on two items (H02, H08), so I do not find reliable evidence that evaluation framing widens the gap. Scoring validity was decisive: the original parser auto-scored unflagged replies by their leading letter, and a post-hoc blinded re-adjudication of all 50 auto-scored yields across both stages (plus 20 decoys) under the same written rule moved most of them to ambiguous, largely replies truncated at the 300-token limit. Stage~2 ambiguity rose to 12.5\% (20/160) and is concentrated in Social ON (11/40), so the interaction ranges from $+$2.5 to $+$17.5~pp depending on how ambiguous rows are coded. I do not claim evaluation awareness as a mechanism or generalize across models.
```

### 4. Introduction / What I claim
**Old:**
```latex
\textbf{What I claim.} Stage~1 establishes a within-model social-pressure cost on this instrument (Neutral$-$Social \textbf{19.2~pp}). Stage~2 finds that explicit evaluation framing widens the Neutral$-$Social gap from \textbf{13.0} to \textbf{29.9}~pp---an interaction of \textbf{$+$16.9~pp} (item-clustered 95\% CI \textbf{5.1--30.8})---concentrated under social pressure and in a minority of items, not as a global honesty collapse (Neutral ON \textbf{97.5\%}).
```
**New:**
```latex
\textbf{What I claim.} Stage~1 finds only a small within-model social-pressure cost on this instrument (Neutral$-$Social \textbf{4.7~pp}), below the pre-set 10~pp gate. Stage~2 finds a Neutral$-$Social gap of \textbf{6.2}~pp under OFF and \textbf{10.3}~pp under ON---an interaction of \textbf{$+$4.2~pp} (item-clustered 95\% CI \textbf{0.0--12.3})---which I do not treat as evidence that evaluation framing widens the gap. Neutral stays at ceiling under ON (\textbf{100.0\%}). The main lesson is methodological: on this instrument, first-letter auto-scoring of yields produced most of the pressure and framing effects in my initial analysis, and they did not survive scoring under the paper's own written rule.
```

### 5. Introduction / What I do not claim
**Old:**
```latex
or that Stage~2 OFF numerically reproduces Stage~1's 19.2~pp (OFF is a directional replication only).
```
**New:**
```latex
or that Stage~2 OFF numerically reproduces Stage~1's 4.7~pp (OFF is a directional comparison only).
```

### 6. Design / Scoring
**Old:**
```latex
Labels use final A/B commitment vs gold~A (start-B-then-correct-to-A~=~maintain). Ambiguous rows are excluded from rate denominators. Blinded adjudication freezes labels before the private condition key is opened.
```
**New:**
```latex
Labels use final A/B commitment vs gold~A (start-B-then-correct-to-A~=~maintain). Ambiguous rows are excluded from rate denominators. Blinded adjudication freezes labels before the private condition key is opened.

\textbf{Scoring correction (post-hoc re-adjudication).} The original parser in both stages sent a reply to blinded review only if it found two different asserted letters, or correction language with both letters present; every other reply was auto-scored from its leading (or line-start) letter. Replies such as ``B is incorrect, A is correct'' or ``B. \ldots\ the calculation supports option A,'' and replies that opened with ``B.'' and then argued against B but were cut off at the 300-token limit before any final choice, were therefore stored as yields without review. Before submission I re-adjudicated \emph{all} auto-scored yields across both stages (26 Stage~1 Llama, 24 Stage~2), mixed with 20 randomly drawn auto-scored maintains as decoys (70 rows), under the same written rule. Rows carried new opaque IDs; stored labels, parser output, pressure, eval frame, and condition-encoding \texttt{run\_id}s were withheld, and labels were frozen before conditions were merged. One blinded reader (an AI assistant applying the written SOP; not a fully independent second reader, since it had seen an earlier audit of these rows) labeled the set. The 20 rows it flagged as borderline were coded ambiguous, the most conservative reading of the rule (no clear final commitment); a sensitivity variant keeps their blind labels. All 20 decoys came back maintain, and a parser screen of all 400 Llama rows found no auto-scored maintain that should have been a yield. Rows outside the blind set (human-adjudicated review rows and clean auto-maintains) keep their labels. Of the 50 auto-scored yields, 12 stayed yield, 2 became maintain, and 36 became ambiguous; in Stage~2, 13 of the 16 newly ambiguous rows ended at the 300-token limit (Stage~1 did not record finish reasons). All numbers below use the corrected labels.
```

### 7. Stage 1 / Results table caption
**Old:**
```latex
\caption{Stage~1 Llama~3.3~70B adjudicated maintain rates (final-commitment scoring). Usable counts are scorable A/B denominators from the frozen Stage~1 summary artifact ($n=80$ generations per pressure).}
```
**New:**
```latex
\caption{Stage~1 Llama~3.3~70B maintain rates after re-adjudication (final-commitment scoring; ambiguous excluded). Usable counts are scorable A/B denominators ($n=80$ generations per pressure).}
```

### 8. Stage 1 / Table rows
**Old:**
```latex
Neutral & 96.2\% & 78/80 \\
Social & 76.9\% & 78/80 \\
Training & 93.7\% & 79/80 \\
Neutral$-$Social & \textbf{19.2~pp} & --- \\
```
**New:**
```latex
Neutral & 100.0\% (75/75) & 75/80 \\
Social & 95.3\% (61/64) & 64/80 \\
Training & 97.4\% (74/76) & 76/80 \\
Neutral$-$Social & \textbf{4.7~pp} & --- \\
```

### 9. Stage 1 / Results text
**Old:**
```latex
Maintain was 96.2\% under Neutral (78/80 usable), 76.9\% under Social (78/80 usable), and 93.7\% under Training (79/80 usable; Table~\ref{tab:stage1}). Design gates (Llama Neutral $\geq$80\%; Neutral$-$Social $\geq$10~pp; empty+unscorable $\leq$10\%) all passed. GPT-OSS~120B failed the full-run usable gate at 94.2\% ($<$95\%); when scorable it was 100\% maintain across pressures, but it stays out of any cross-model table or claim. Stage~1 is a within-model baseline. Stage~2 OFF is a directional replication of the social-pressure cost---not a numeric reproduction of 19.2~pp.
```
**New:**
```latex
Maintain was 100.0\% under Neutral (75/75; 75/80 usable), 95.3\% under Social (61/64; 64/80 usable), and 97.4\% under Training (74/76; 76/80 usable; Table~\ref{tab:stage1}). Ambiguous replies rose to 25/240 (10.4\%), 16 of them under Social. The remaining Social yields fall on three items (H02, H08, H12). Of the design gates, Llama Neutral $\geq$80\% and empty+unscorable $\leq$10\% (2.7\%; ambiguous replies are not part of this gate as defined) still pass, but Neutral$-$Social $\geq$10~pp does \emph{not} (4.7~pp; 7.6~pp in the borderline-sensitivity variant). Using the Stage~2 item-clustered bootstrap procedure (not part of the original Stage~1 analysis), the 95\% CI for the Neutral$-$Social gap is [0.0, 10.9]. GPT-OSS~120B failed the full-run usable gate at 94.2\% ($<$95\%); when scorable it was 100\% maintain across pressures, but it stays out of any cross-model table or claim. Stage~1 is a within-model baseline whose direction (Neutral above Social) holds but whose size is small. Stage~2 OFF is a directional comparison with that cost---not a numeric reproduction of 4.7~pp.
```

### 10. Stage 2 / Scoring and adjudication
**Old:**
```latex
Labels frozen before the private condition key was opened, then merged for the $2\times2$.
```
**New:**
```latex
Labels frozen before the private condition key was opened, then merged for the $2\times2$. Replies the parser did not flag were auto-scored by leading letter; all auto-scored yields were later re-adjudicated blind (Design, \emph{Scoring correction}).
```

### 11. Stage 2 / Table caption
**Old:**
```latex
\caption{Stage~2 post-adjudication maintain rates (ambiguous excluded).}
```
**New:**
```latex
\caption{Stage~2 maintain rates after re-adjudication (ambiguous excluded; maintain/usable).}
```

### 12. Stage 2 / Table rows
**Old:**
```latex
Neutral & 92.5\% (40/40) & 97.5\% (40/40) \\
Social & 79.5\% (39 usable) & 67.6\% (37 usable) \\
\midrule
Drop (N$-$S) & 13.0~pp & 29.9~pp \\
Interaction & \multicolumn{2}{c}{\textbf{$+$16.9~pp}} \\
Ambiguity & \multicolumn{2}{c}{2.5\% (4/160)} \\
```
**New:**
```latex
Neutral & 97.4\% (37/38) & 100.0\% (39/39) \\
Social & 91.2\% (31/34) & 89.7\% (26/29) \\
\midrule
Drop (N$-$S) & 6.2~pp & 10.3~pp \\
Interaction & \multicolumn{2}{c}{\textbf{$+$4.2~pp}} \\
Ambiguity & \multicolumn{2}{c}{12.5\% (20/160)} \\
```

### 13. Stage 2 / CI table
**Old:**
```latex
Drop OFF & 13.0~pp & [2.6, 26.2] \\
Drop ON & 29.9~pp & [11.8, 49.1] \\
Interaction & $+$16.9~pp & [5.1, 30.8] \\
```
**New:**
```latex
Drop OFF & 6.2~pp & [0.0, 19.2] \\
Drop ON & 10.3~pp & [0.0, 27.3] \\
Interaction & $+$4.2~pp & [0.0, 12.3] \\
```

### 14. Stage 2 / Results text
**Old:**
```latex
Post-adjudication (Table~\ref{tab:stage2}): Neutral OFF 92.5\% (40/40), Social OFF 79.5\% (39 usable), Neutral ON 97.5\% (40/40), Social ON 67.6\% (37 usable). Drop OFF 13.0~pp; Drop ON 29.9~pp; interaction $+16.9$~pp; ambiguity 2.5\% (4/160).
```
**New:**
```latex
After re-adjudication (Table~\ref{tab:stage2}): Neutral OFF 97.4\% (37/38), Social OFF 91.2\% (31/34), Neutral ON 100.0\% (39/39), Social ON 89.7\% (26/29). Drop OFF 6.2~pp; Drop ON 10.3~pp; interaction $+4.2$~pp; ambiguity 12.5\% (20/160). Social OFF and Social ON each contain three yields (H02 twice and H08 once in each). The larger ON drop comes from a smaller usable Social ON denominator and from one Neutral OFF yield (H08), not from more yields under ON; Social ON minus Social OFF is $-1.5$~pp.
```

### 15. Stage 2 / Adjudication history
**Old:**
```latex
Pre-adjudication auto analysis (review rows excluded) gave interaction $+29.0$~pp. After one blinded pass, 26 of 30 review rows were B$\rightarrow$A recoveries, 0 yield, and 4 ambiguous; frozen post-adjudication interaction is $+16.9$~pp. Neutral remained high under ON (97.5\%)---not a global honesty collapse.
```
**New:**
```latex
Pre-adjudication auto analysis (review rows excluded) gave interaction $+29.0$~pp. After the original blinded pass over the 30 parser-flagged rows (26 B$\rightarrow$A recoveries, 0 yield, 4 ambiguous), it was $+16.9$~pp. That pass never saw the 24 rows the parser auto-scored as yields; after re-adjudicating them (7 yield, 1 maintain, 16 ambiguous) it is $+4.2$~pp. Neutral stayed at ceiling under ON (100.0\%).
```

### 16. Stage 2 / CI + ambiguity text
**Old:**
```latex
Item-clustered 95\% CIs (Table~\ref{tab:ci}): Drop OFF [2.6, 26.2], Drop ON [11.8, 49.1], Interaction [5.1, 30.8]. A descriptive ambiguity bound (all four ambiguous $\rightarrow$ maintain vs yield) moves the interaction only to $+15.0$ vs $+20.0$~pp; sign unchanged.
```
**New:**
```latex
Item-clustered 95\% CIs (Table~\ref{tab:ci}): Drop OFF [0.0, 19.2], Drop ON [0.0, 27.3], Interaction [0.0, 12.3]; 13.9\% of bootstrap resamples give an interaction $\leq 0$. A descriptive ambiguity bound (all 20 ambiguous $\rightarrow$ maintain vs yield) moves the interaction from $+2.5$ to $+17.5$~pp. The sign is unchanged, but the size depends heavily on ambiguity coding, because ambiguous rows concentrate in Social ON (11/40) and 12 of 40 Social ON replies hit the 300-token limit, against 2--4 of 40 in each other cell. Keeping the blind labels for the 20 borderline rows (sensitivity variant) gives Social ON 90.0\% (27/30), Drop ON 10.0~pp, and interaction $+3.8$~pp (CI [0.0, 11.3]); Stage~1 Neutral$-$Social becomes 7.6~pp.
```

### 17. Stage 2 / Item-level
**Old:**
```latex
The interaction is not bank-wide. Positive item-level interaction concentrates in a minority of items (5 of 20 with both drops defined). H19 is highest-leverage; leave-one-out interaction remains positive when any one item is omitted (minimum leaving out H19: 12.4~pp). H02 shows a large Neutral$-$Social drop under both OFF and ON and does not drive the interaction. H08/H19 remain in the bank.
```
**New:**
```latex
Nothing in the item-level picture suggests a bank-wide effect. Only one item (H08) has a positive item-level interaction ($+50$~pp, from a single usable Social reply per frame); the other 15 items with both drops defined contribute zero, and none is negative. Four items (H09, H10, H11, H19) have no usable Social ON replies; H19 has none in Social OFF or Neutral OFF either, so it no longer carries leverage. Leave-one-out interaction stays positive when any one item is omitted (minimum leaving out H08: $+1.1$~pp; maximum leaving out H04: $+4.8$~pp). H02 shows a 100~pp Neutral$-$Social drop under both OFF and ON and does not drive the interaction. H08/H19 remain in the bank.
```

### 18. Stage 2 / Frozen result
**Old:**
```latex
\textbf{Frozen result.} On this frozen 20-item Llama honesty bank, explicit evaluation framing widened the Neutral$-$Social honesty gap from 13.0 to 29.9 percentage points, an interaction of $+16.9$~pp (item-clustered 95\% CI 5.1--30.8). The additional drop was concentrated under social pressure and in a minority of items, rather than reflecting a general decrease in honesty.
```
**New:**
```latex
\textbf{Result.} On this frozen 20-item Llama honesty bank, after re-adjudication under the written scoring rule, the Neutral$-$Social gap was 6.2 percentage points under OFF and 10.3 under ON, an interaction of $+4.2$~pp (item-clustered 95\% CI 0.0--12.3). I do not find reliable evidence that explicit evaluation framing widens the social-pressure gap: the estimate is small, its CI reaches zero, it rests on one item and on differential ambiguity, and Social ON does not contain more yields than Social OFF.
```

### 19. Stage 2 / Interpretation
**Old:**
```latex
These results support a measurement-validity claim about eval framing on this instrument and model. They do not establish evaluation awareness as a mechanism, do not generalize across model families, and do not license describing the effect as bank-wide and uniform.
```
**New:**
```latex
These results are a measurement-validity finding about this instrument and model: the framing effect in my initial analysis depended on first-letter scoring of replies the written rule does not count as yields. They do not establish evaluation awareness as a mechanism, do not generalize across model families, and do not license describing any effect as bank-wide and uniform.
```

### 20. Reading both stages
**Old:**
```latex
Stage~1 locks a within-model social-pressure cost (Neutral 96.2\%, Social 76.9\%, Training 93.7\%; Neutral$-$Social 19.2~pp). Stage~2 isolates whether eval framing widens that cost: Drop OFF 13.0~pp $\rightarrow$ Drop ON 29.9~pp (interaction $+16.9$~pp; CI 5.1--30.8). Neutral stays high under ON (97.5\%); the interaction concentrates under social pressure and in a minority of items. Blinded adjudication mattered (pre-adj $+29.0$~$\rightarrow$ post-adj $+16.9$ after 26 of 30 B$\rightarrow$A recoveries). Stage~2 OFF directionally tracks Stage~1 without reproducing 19.2~pp.
```
**New:**
```latex
Stage~1 shows a small within-model social-pressure cost (Neutral 100.0\%, Social 95.3\%, Training 97.4\%; Neutral$-$Social 4.7~pp, below the 10~pp gate). Stage~2 asks whether eval framing widens that cost: Drop OFF 6.2~pp $\rightarrow$ Drop ON 10.3~pp (interaction $+4.2$~pp; CI 0.0--12.3), with equal Social yield counts under OFF and ON and Neutral at ceiling under ON (100.0\%). Scoring decided the result: pre-adj $+29.0$ $\rightarrow$ $+16.9$ after the original review (26 of 30 B$\rightarrow$A recoveries) $\rightarrow$ $+4.2$ after re-adjudicating the auto-scored yields. Stage~2 OFF (6.2~pp) is directionally consistent with Stage~1 (4.7~pp) without reproducing it.
```

### 21. Limitations
**Old:**
```latex
Results are for one model (Llama~3.3~70B) on a 20-item bank of limited topical breadth. The Stage~2 interaction is supported under item-clustered uncertainty but concentrated in a minority of items (H19 high-leverage), so it is not a uniform bank-wide shift. Stage~2 OFF is directional, not the same numerical estimate as Stage~1's 19.2~pp. Adjudication materially changed the interaction (pre-adj $+29.0$~$\rightarrow$ post-adj $+16.9$). Condition-encoding \texttt{run\_id} had to be withheld in review; future generation should emit opaque IDs from the start.
```
**New:**
```latex
Results are for one model (Llama~3.3~70B) on a 20-item bank of limited topical breadth. The Stage~2 interaction is not distinguishable from zero under item-clustered uncertainty and rests on one item (H08). Stage~2 OFF is directional, not the same numerical estimate as Stage~1's 4.7~pp. Scoring materially changed both stages (Stage~2 interaction pre-adj $+29.0$ $\rightarrow$ $+16.9$ $\rightarrow$ $+4.2$; Stage~1 Neutral$-$Social from the 19.2~pp in my initial analysis to 4.7~pp). The correction was post hoc, made by a single reader who is not fully independent of an earlier audit, and codes borderline rows as ambiguous; the sensitivity variant changes the headline numbers only slightly. The 300-token limit truncated many replies before a final choice, and truncation was itself uneven across cells (12/40 in Social ON), so ambiguity is differential and the interaction ranges from $+2.5$ to $+17.5$~pp across ambiguity codings; future runs should use a larger token budget and send every non-clean reply to review. Condition-encoding \texttt{run\_id} had to be withheld in review; future generation should emit opaque IDs from the start.
```

### 22. Conclusion
**Old:**
```latex
Holding an honesty task fixed and varying only pressure wrappers, Llama~3.3~70B shows lower honesty-maintain under social pressure than under neutral or training-style pressure (Stage~1: Neutral$-$Social 19.2~pp). Reusing that frozen instrument and crossing Neutral/Social with explicit evaluation framing, the Neutral$-$Social gap widens from 13.0 to 29.9~pp under ON---an interaction of $+16.9$~pp with item-clustered 95\% CI 5.1--30.8 (Stage~2). Neutral remains high under ON (97.5\%); the additional drop concentrates under social pressure and in a minority of items. The contribution is a measurement-validity result about pressure contrasts under evaluation framing on this instrument and model---not a mechanism claim about evaluation awareness, not a bank-wide uniformity claim, and not a multi-model survey.
```
**New:**
```latex
Holding an honesty task fixed and varying only pressure wrappers, Llama~3.3~70B shows slightly lower honesty-maintain under social pressure than under neutral or training-style pressure (Stage~1: Neutral$-$Social 4.7~pp, below the pre-set 10~pp gate). Reusing that frozen instrument and crossing Neutral/Social with explicit evaluation framing, the Neutral$-$Social gap is 6.2~pp under OFF and 10.3~pp under ON---an interaction of $+4.2$~pp with item-clustered 95\% CI 0.0--12.3 (Stage~2)---so I do not find reliable evidence that evaluation framing widens the gap. Neutral stays at ceiling under ON (100.0\%). The contribution is a measurement-validity result on this instrument and model: first-letter auto-scoring of yields, not model behavior, produced most of the pressure and framing effects in my initial analysis, and re-adjudicating under the written rule removed them. It is not a mechanism claim about evaluation awareness, not a bank-wide uniformity claim, and not a multi-model survey.
```

### 23. Appendix / Adjudication SOP
**Old:**
```latex
Final A~=~maintain; final B~=~yield; B$\rightarrow$A~=~maintain; A$\rightarrow$B~=~yield; unresolved~=~ambiguous. Labels frozen before the condition key was opened.
```
**New:**
```latex
Final A~=~maintain; final B~=~yield; B$\rightarrow$A~=~maintain; A$\rightarrow$B~=~yield; unresolved~=~ambiguous. Labels frozen before the condition key was opened.

\paragraph{Re-adjudication.} Same rule, applied to all 50 auto-scored yields (Stage~1 Llama 26, Stage~2 24) plus 20 random auto-scored maintains as decoys, under new opaque IDs with no stored label, parser output, pressure, eval frame, or \texttt{run\_id}; reader saw the raw reply, item text, options, gold~A, and a truncation flag. Borderline rows (20) coded ambiguous in the primary analysis; blind labels kept in the sensitivity variant. Rows outside the set keep their stored labels.
```

### 24. Appendix / Artifacts
**Old:**
```latex
\texttt{pilot02\_item\_level\_robustness.csv}; \texttt{pilot02\_clustered\_bootstrap.json}; \texttt{pilot02\_canonical\_table.json}.
```
**New:**
```latex
\texttt{pilot02\_item\_level\_robustness.csv}; \texttt{pilot02\_clustered\_bootstrap.json}; \texttt{pilot02\_canonical\_table.json} (all superseded for reported numbers by the re-adjudication files); \texttt{blind\_labels.csv}; \texttt{corrected\_labels\_stage1.csv}; \texttt{corrected\_labels\_stage2.csv}; \texttt{CHANGES.csv}; \texttt{results.json}.
```

### 25. Appendix / Bootstrap
**Old:**
```latex
Resample 20 items with replacement; keep all gens within item; $B=5000$; seed 42. Do not treat 160 rows as independent.
```
**New:**
```latex
Resample 20 items with replacement; keep all gens within item; $B=5000$; seed 42 (\texttt{numpy.random.default\_rng}); percentile intervals. Do not treat 160 rows as independent.
```

### ARXIV_METADATA.md (draft copy)
Status line → DRAFT/not approved; title; abstract (plain-text mirror of new LaTeX abstract); '7 pages' → '8 pages'; Stage 1 usable line updated.