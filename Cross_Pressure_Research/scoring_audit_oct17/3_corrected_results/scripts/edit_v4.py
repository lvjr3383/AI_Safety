import json
P="/workspace/corrected_oct17/arxiv_pack_v4/main.tex"
s=open(P,encoding='utf-8').read()
E=[]
def R(sec,old,new): E.append((sec,old,new))
R("Header","DRAFT FOR REVIEW (v3) --- not for submission (Oct 17, 2026)","DRAFT FOR REVIEW (v4) --- not for submission (Oct 17, 2026)")
R("Header comment","%% REVIEW COPY v3 (Oct 17, 2026). Title chosen. Abstract near-final.","%% REVIEW COPY v4 (Oct 17, 2026). Title chosen. Abstract near-final.")
R("Abstract: split audit sentence",
"All 50 auto-scored yields (plus 20 decoys) were re-adjudicated under the same written rule, in a condition-blinded re-adjudication by an AI assistant applying the written SOP; the reader was not fully independent of the earlier audit. It reclassified 36 as ambiguous and 2 as maintain.",
"All 50 auto-scored yields, mixed with 20 decoy maintains under opaque IDs with condition, label, and run identifiers removed, were re-adjudicated against the same written rule. This was a condition-blinded re-adjudication by an AI assistant applying the written SOP; the reader was not fully independent of the earlier audit. It reclassified 36 yields as ambiguous and 2 as maintain.")
R("Related work: evaluation pipelines",
r"""\textbf{Measurement validity.}""",
r"""\textbf{Evaluation pipelines.}
Implementation details of language-model evaluation, including the answer-extraction heuristics used to score generated outputs, can change both scores and the conclusions drawn from them~\citep{biderman2024lessons}. Seemingly minor formatting choices can also shift measured accuracy substantially, partly through outputs that match no valid option~\citep{sclar2023quantifying}. This paper is a concrete case on the scoring side: the generations are held fixed, and only the extraction and review layer changes.

\textbf{Measurement validity.}""")
R("Design: Stage 1 gate definition",
r"""Pre-set gates: Neutral $\geq$80\%; Neutral$-$Social $\geq$10~pp; empty+unscorable $\leq$10\%.""",
r"""Pre-set gates: Neutral $\geq$80\%; Neutral$-$Social $\geq$10~pp; and a scorability gate, coded as empty/error plus unscorable (no interpretable A/B) $\leq$10\% of all 480 Stage~1 rows, which did not count adjudicated-ambiguous replies.""")
R("Sec 6: reader/borderline operationalization",
r"""The SOP was applied unchanged. Each label carries its deciding quote, and a script confirmed every quote appears verbatim in its reply. The reader flagged 20 rows as borderline (e.g., replies that reject B and state A's content without naming A, or are cut off right after arguing for A's content). These were resolved by the most conservative reading---no clear final commitment, so ambiguous---with a sensitivity variant that keeps the reader's labels (15 ambiguous, 2 maintain, 3 yield).""",
r"""Each label carries its deciding quote, and a script confirmed every quote appears verbatim in its reply. The reader flagged 20 rows as borderline, where the written rule does not by itself settle the label: for example, ``B is incorrect'' followed by A's content without ever naming A, or a reply cut off right after arguing for A's content. For these rows I adopted an audit-time conservative operationalization of the existing final-commitment rule: a reply without a clear, explicit final A or B commitment is ambiguous. This operationalization was fixed during the audit; it is not stated in the original SOP. A sensitivity variant keeps the reader's own labels for these rows (15 ambiguous, 2 maintain, 3 yield).""")
R("Sec 6: Stage 1 gate statement",
r"""so the pre-set $\geq$10~pp gate now \emph{fails} (7.6~pp in the sensitivity variant); the Neutral and empty+unscorable gates still pass (the latter, 2.7\%, does not count ambiguous replies as defined). Ambiguity rose to 25/240 (10.4\%), 16 of them under Social;""",
r"""so the pre-set $\geq$10~pp gate now \emph{fails} (7.6~pp in the sensitivity variant). The Neutral $\geq$80\% gate still passes. The scorability gate, as originally coded (empty/error plus unscorable over all 480 rows, excluding ambiguous replies), also still passes as originally defined (13/480 = 2.7\%). But the corrected Llama ambiguity rate is 25/240 = 10.4\%, above 10\%: if ambiguous replies counted as unscorable, the scorability gate would in practice fail for the Llama arm. Of the 25 ambiguous replies, 16 are under Social;""")
R("Sec 6: bootstrap wording",
r"""interaction $+$4.2~pp [0.0, 12.3], with 13.9\% of bootstrap draws $\leq 0$.""",
r"""interaction $+$4.2~pp [0.0, 12.3]. Of the 5000 bootstrap draws, 13.5\% are exactly 0 and 0.4\% are negative (minimum $-1.3$~pp), so the lower bound of 0.0 is exact rather than a rounded negative value. The zeros arise because every Stage~2 yield is on H02 or H08: the 12.8\% of resamples that omit both items have 100\% maintain in every cell, and all their contrasts are exactly zero (the same mechanism gives the 0.0 lower bounds for both drops, which have no negative draws).""")
R("Sec 6: sensitivity bootstrap",
r"""The sensitivity variant gives $+$3.8~pp [0.0, 11.3].""",
r"""The sensitivity variant gives $+$3.8~pp [0.0, 11.3] (14.1\% of draws exactly 0, 0.7\% negative).""")
R("Sec 6: truncation / differential missingness",
r"""\textbf{Ambiguity is differential.} Ambiguity is 20/160 (12.5\%), 11 of them in Social ON, and 16 of the 20 ended at the 300-token limit. Truncation itself varied with condition: 12 of 40 Social ON replies hit the limit, against 4 of 40 in Social OFF and 2 of 40 in each Neutral cell. Coding all ambiguous rows maintain vs yield moves the interaction from $+$2.5 to $+$17.5~pp, so the corrected estimate is uncertain rather than a precise null.""",
r"""\textbf{Truncation and ambiguity are differential.} Truncation at the 300-token cap (\texttt{finish\_reason} = length) varied by cell: Social ON 12/40, Social OFF 4/40, Neutral OFF 2/40, Neutral ON 2/40. Ambiguity is 20/160 (12.5\%), 11 of them in Social ON, and 16 of the 20 ended at the cap. Coding all ambiguous rows maintain vs yield moves the interaction from $+$2.5 to $+$17.5~pp, so the corrected estimate is uncertain rather than a precise null.""")
R("Discussion: token cap sentence + MNAR",
r"""The experimental setup was not the main problem, but one design choice is itself a measurement issue: the 300-token cap interacted with condition, and truncation turned long Social ON replies into missing outcomes in exactly the cell the interaction depends on.""",
r"""The primary discovered failure was in scoring and review coverage, while the 300-token cap materially amplified the problem by creating condition-dependent truncation. Truncation turned long Social ON replies into missing outcomes in exactly the cell the interaction depends on. Excluding ambiguous rows from denominators treats them as missing at random, and they are not: missingness is concentrated in one cell, and a reply cut off under social pressure need not have ended where completed replies did. The $+$2.5 to $+$17.5~pp ambiguity bounds show how much the interaction depends on that untestable assumption.""")
R("Limitations: borderline + MNAR",
r"""Borderline rows were coded ambiguous, the most conservative reading; the sensitivity variant shows this does not change the conclusions. Truncation cannot be fixed without new generations, which I did not run; truncated replies remain missing outcomes, unevenly across cells.""",
r"""Borderline rows were coded ambiguous under an audit-time conservative operationalization of the final-commitment rule; the sensitivity variant shows this does not change the conclusions. Truncation cannot be fixed without new generations, which I did not run. Truncated replies remain missing outcomes, and their exclusion is not missing at random (Social ON 12/40 truncated vs 2--4/40 elsewhere), so the corrected estimates rest on an untestable assumption bracketed by the $+$2.5 to $+$17.5~pp ambiguity bounds.""")
R("Appendix: audit paragraph",
r"""Same rule, applied to all 50 auto-scored yields""",
r"""The written final-commitment rule, applied to all 50 auto-scored yields""")
R("Appendix: borderline",
r"""Borderline rows (20) coded ambiguous in the primary analysis; blind labels kept in the sensitivity variant.""",
r"""Borderline rows (20) coded ambiguous in the primary analysis under an audit-time conservative operationalization (no clear, explicit final A or B commitment $\rightarrow$ ambiguous); the reader's labels are kept in the sensitivity variant.""")
R("Appendix: bootstrap",
r"""seed 42 (\texttt{numpy.random.default\_rng}); percentile intervals.""",
r"""seed 42 (\texttt{numpy.random.default\_rng}); percentile intervals (\texttt{numpy.percentile}, linear interpolation). Draw-level diagnostics (counts of negative, exactly-zero, and positive draws) are in \texttt{bootstrap\_check.md}.""")
out=s; log=[]
for sec,old,new in E:
    n=out.count(old); assert n==1,(sec,n)
    out=out.replace(old,new); log.append(dict(section=sec,old=old,new=new))
# Table rows
old_amb=r"""Ambiguous & 5/240 & \textbf{25/240 (10.4\%)} & 21/240 \\"""
new_amb=r"""Scorability gate (as coded) & pass (2.7\%) & pass (2.7\%) & pass (2.7\%) \\
Ambiguous & 5/240 & \textbf{25/240 (10.4\%; $>$10\%)} & 21/240 \\"""
assert out.count(old_amb)==1; out=out.replace(old_amb,new_amb); log.append(dict(section="Table 3 Stage 1 rows",old=old_amb,new=new_amb))
old_cap=r"""$^\dagger$Added during the corrected analysis; not part of the original locked analysis.}"""
new_cap=r"""$^\dagger$Added during the corrected analysis; not part of the original locked analysis. Lower bounds of 0.0 are exact (see text).}"""
assert out.count(old_cap)==1; out=out.replace(old_cap,new_cap); log.append(dict(section="Table 3 caption",old=old_cap,new=new_cap))
open(P,'w',encoding='utf-8').write(out)
json.dump(log,open('/workspace/corrected_oct17/scripts/v4_edits.json','w'),indent=1,ensure_ascii=False)
print(len(log))
