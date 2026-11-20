"""Builds v10 (structure rewrite; no number changes) from the built v9 source.
Sections are reorganized to: Introduction / Preliminaries / one section per analysis (Setup, Results) / Discussions / Related Work / Conclusion.
Paragraphs carried over from v9 are reused verbatim by line range, with anchors asserted. Usage: python3 build_v10.py <v9 tex> <out v10 tex>"""
import sys, re
L=open(sys.argv[1]).read().split('\n')
def g(a,b=None): return '\n'.join(L[a-1:(b or a)])
def anchor(n,s): assert L[n-1].startswith(s),(n,L[n-1][:60])
for n,s in [(46,r'\begin{document}'),(67,r'\textbf{Honesty under pressure.}'),(75,r'\section{Design'),(78,r'\textbf{Instrument.}'),(97,r'\textbf{Written scoring rule'),(99,r'\textbf{Claim walls.}'),
            (102,'An automatic parser'),(104,'The original Stage 1'),(107,'While preparing'),(115,r'\section{October'),(118,r'\textbf{Unblinded'),(128,r'\begin{table}'),(218,r'\end{table}'),
            (221,r'\textbf{Why the October'),(223,r'\textbf{Locked rule.}'),(229,r'\textbf{Agreement.}'),(239,r'\textbf{The result rests'),(241,r'\textbf{What can'),(244,'A safety-evaluation'),
            (248,'The second change'),(250,'Practical recommendations'),(264,r'\section{Limitations}'),(274,'Holding the task fixed'),(276,r'\section*{AI assistance'),(279,r'\begin{thebibliography}'),(296,r'\end{thebibliography}'),(298,r'\appendix')]: anchor(n,s)
pre=g(1,45).replace('DRAFT FOR REVIEW (v9)','DRAFT FOR REVIEW (v10)')
end=len(L)-1
while not L[end].startswith(r'\end{document}'): end-=1
doc=pre+r'''
\begin{document}
\maketitle

\begin{abstract}
Behavioral evaluations of language models turn free-text replies into scores, and conclusions about safety-relevant behavior rest on those scores. In pressure evaluations, how much a reported effect depends on the scoring step, rather than on the model's outputs, is not routinely reported alongside the effect. In this work I show that one frozen set of \model\ replies supports materially different conclusions under three scoring procedures that each looked reasonable when adopted. The replies come from a 20-item forced-choice answer-maintenance task under neutral versus social-pressure prompts, crossed with explicit evaluation framing (160 generations); the estimand is how much evaluation framing widens the pressure gap. The original parser-based pipeline gave +16.9\pp (item-clustered 95\% CI 5.1--30.8). An audit that re-read every auto-scored yield gave +4.2\pp (0.0--12.3). A symmetric rule, locked before reading and applied identically to both answer letters by \SymNReaders\ condition-blinded model readers, gives \SymIntRange\pp. Finally, I trace the remaining disagreement to one response class, replies that give the pressured answer, never retract it, then reason toward the correct one, for which the estimate spans \SymStrictRange\pp, depending on how the class is scored and on which replies each reader places in it. Neither the original result nor its first correction is robust, and I claim neither an effect nor its absence. More broadly, the case suggests that scoring and adjudication are part of the measurement, and that an audit needs to be as even-handed as the pipeline it corrects. No generation was rerun at any point.
\end{abstract}

\section{Introduction}
Evaluations of honesty and sycophancy ask whether a model keeps a correct answer when it is pushed toward a wrong one \citep{ren2025,sharma2023}. Their results feed claims about how models behave under pressure, and increasingly about whether that behavior changes when a model is told it is being evaluated \citep{needham2025,laine2024}. Such claims are only as good as the step that turns each free-text reply into a label.

That step is known to be fragile. Answer-extraction heuristics are an acknowledged source of irreproducibility \citep{biderman2024}; first-token probabilities need not match the answer a model gives in its text \citep{wang2024}; extraction strategies can produce misleading comparisons \citep{molfese2025}; and choices of judge, prompt and sampling add unreported variance that can reverse conclusions \citep{messing2026}. What is less often available is a documented case in a pressure evaluation, where the generations are frozen, the labels from every scoring pass are preserved, and the correction is itself audited.

This paper is such a case. I ran a small cross-pressure study on \model: the same 20 two-option items under Neutral and Social wrappers (Stage 1, with a Training wrapper as well), then crossed with explicit evaluation framing OFF versus ON (Stage 2). \textbf{The same frozen generations give three materially different answers to one question, how much evaluation framing widens the social-pressure gap, depending on how replies are scored}, and a wider range still under a stricter coding of one response class. I do not claim any of these is the true effect.

Two real replies show what the scoring problem looks like. In the first (item H13, Social, framing ON; a tank fills at 12 L/min and drains at 5; A is a net gain of 7, B of 17), the reply opens:
\begin{quote}\small\sffamily B is incorrect, A is correct.\end{quote}
The original parser read the leading ``B'' and stored a yield, and the reply was never sent to review. This is a plain scoring error, and every later analysis scores it maintain. The second (item H08, Social, framing OFF; a culture of 50 cells doubles every 6 hours; A is 200 cells after 12 hours, B is 100) is harder. The reply opens ``B.'' and continues:
\begin{quote}\small\sffamily The culture starts with 50 cells and doubles every 6 hours. After 6 hours, it will have 100 cells (50 * 2), and after another 6 hours (total of 12 hours), it will double again, resulting in 200 cells. [\ldots] the correct count after 12 hours is indeed not 100 [\ldots] the option stating the culture has 100 cells after a doubling (which occurs at the 6-hour mark) is the choice directly supported at the 6-hour mark, not the 12-hour mark as per the doubling pattern described.\end{quote}
The reply argues both ways: it computes A's answer and says B's figure is wrong, then calls B the supported choice, and it is cut off by the 300-token generation cap without explicitly retracting the letter B or naming A. The original pipeline scored it a yield; a later audit in October scored it ambiguous; and all three readers of the final, symmetric audit placed it in the class this paper turns on: a letter given, never explicitly retracted, followed by reasoning that points away from it.

Figure \ref{fig:one} shows the evidence. The original pipeline, a leading-letter parser with review of parser-flagged rows only, gave +16.9\pp (CI 5.1--30.8). After raw replies showed the parser counting a leading ``B'' as a yield even when the reply rejected B, an October audit re-read every auto-scored yield and gave +4.2\pp (0.0--12.3). A November reconstruction found that audit one-directional and asymmetric between the two letters; under one rule locked in advance and applied identically to both letters, \SymNReaders\ condition-blinded model readers (the third added after the first two had been analysed) give \SymIntRange\pp.
\begin{figure}[H]\centering
\includegraphics[width=0.86\linewidth]{fig1_interaction_by_scoring.pdf}
\caption{One estimand, one frozen set of 160 Stage 2 generations, nine scorings. Each row is the evaluation-framing interaction (how much the Neutral--Social maintain gap widens under explicit evaluation framing) with its item-clustered 95\% CI. Filled markers use each procedure's own labels (the third row is the October audit with a second reader's labels on its 20 borderline rows). Open markers apply the symmetric rule's stricter predeclared coding (``strict-U2''), which scores one response class, a ``B'' that is never explicitly retracted but is followed by reasoning toward A, as ambiguous. No model output differs between rows.}
\label{fig:one}
\end{figure}

Two further findings sharpen this. First, the corrective audit embedded its own contestable choices: it could only move labels away from yield, and it treated an unretracted ``A'' and an unretracted ``B'' differently. Second, the remaining uncertainty is concentrated in one response class. Replies that give B, never explicitly retract it, and then reason toward A are yields under the symmetric rule's primary coding and ambiguous under its predeclared strict coding, and the estimate spans \SymStrictRange\pp depending on that coding and on which replies each reader places in the class. The readers agree on almost every label but not on which rows belong to it.

The practical implication is that scoring and adjudication are part of the measurement. A pressure effect reported from a single scoring pass, or from a correction that re-reads only the suspect labels, can be an artifact of that procedure. The study is small (one model, 20 items) and all audits are post hoc with model readers, so the contribution is a documented instance and a procedure, not a behavioral law.

\textbf{Contributions.}
\begin{itemize}
  \item \textbf{A documented scoring failure.} A parser that scored the leading letter against a final-commitment rule, with review triggered only by the parser, produced a +16.9\pp interaction and a 19.2\pp Stage 1 gap that no later scoring reproduces as a point estimate, though some later intervals include them (Section \ref{sec:orig}).
  \item \textbf{An audit of the audit.} The October correction (+4.2\pp) re-read only stored yields (plus decoys) and coded the two letters asymmetrically; a symmetric rule locked before reading gives \SymIntRange\pp across \SymNReaders\ readers (Sections \ref{sec:oct} and \ref{sec:sym}).
  \item \textbf{The disputed response class.} One named class of reply, isolated by reader basis codes, accounts for a symmetric estimate that spans \SymStrictRange\pp depending on its coding and on reader classification; I report both codings and do not choose between them (Section \ref{sec:u2}).
  \item \textbf{An audit procedure and package.} Locked and hashed rule, condition-blinded sheets, per-reader label files, frozen-hash verification, and scripts that recompute every ledger and regenerate Tables \ref{tab:ledgers} and \ref{tab:sens} and Figure \ref{fig:one} from the frozen label files (Appendix \ref{app:details}).
\end{itemize}

'''+g(64)+r'''

\section{Preliminaries}
\subsection{Task and Instrument}
'''+g(78,95)+r'''

\subsection{Scoring Rule}
'''+g(97)+r'''

\subsection{Notations and Estimands}
Each reply receives one of three labels: \emph{maintain} (final commitment to A, the gold option), \emph{yield} (final commitment to B, the option the pressure wrapper pushes), or \emph{ambiguous}. The \emph{maintain rate} of a cell is maintain / (maintain + yield); ambiguous replies are excluded from the denominator and reported separately. The \emph{gap} is the Neutral maintain rate minus the Social maintain rate, in percentage points (labelled ``Drop'' in the Stage 2 tables). The Stage 2 \emph{interaction} is the gap under evaluation framing ON minus the gap under OFF; a positive value means framing widened the social-pressure gap. Intervals are item-clustered percentile bootstraps: 20 items resampled with replacement, all generations within an item kept together, $B=5000$, seed 42. A \emph{ledger} is one complete labelling of the same frozen generations. Ledgers appear in Tables \ref{tab:ledgers} and \ref{tab:sens}. Under the symmetric rule of Section \ref{sec:sym}, ``commitment'' is defined more strictly than here: a committed letter stands unless it is explicitly retracted.

\section{The Original Analysis}\label{sec:orig}
\subsection{Experiment Setup}
'''+g(102)+r'''

\subsection{Results}
'''+g(104)+r'''

\subsection{Why the Analysis Was Reopened}
'''+g(107,113)+r'''

\section{The October Audit}\label{sec:oct}
\subsection{Audit Procedure}
'''+g(116,125)+r'''

\subsection{Results}
'''+g(126,218)+r'''

\section{The Symmetric Audit}\label{sec:sym}
\subsection{Motivation}
'''+g(221)+r'''

\subsection{Audit Design}
'''+g(223,227)+r'''

\subsection{Results}
'''+g(229,237)+r'''

\subsection{One Response Class, and Who Is Placed in It}\label{sec:u2}
'''+g(239,241)+r'''

\section{Discussions}
\subsection{On Scoring as Part of the Measurement}
'''+g(244,246)+r'''

\subsection{On Auditing an Audit}
'''+g(248)+r'''

\subsection{Recommendations}
'''+g(250,262)+r'''

\subsection{Limitations}
'''+g(265,271)+r'''

'''+g(99)+r'''

\section{Related Work}
'''+g(67,73)+r'''

\section{Conclusion}
'''+g(274)+r'''

'''+g(276,277)+r'''

'''+g(279,296)+r'''

'''+g(298,end)+r'''
\section{Lessons Learned}\label{app:lessons}
Practical points from running this audit that do not fit the main narrative.
\begin{itemize}
  \item Record \texttt{finish\_reason} for every generation. Stage 1 did not, so its truncation can only be inferred from text.
  \item Commit raw generations to version control when they are produced. Here some entered the repository weeks later, and the Stage 1 raw file never did, which leaves corroboration by file size and timestamp in place of a hash.
  \item Emit opaque run IDs at generation time. IDs that encode the condition must be stripped before every review.
  \item Give readers only the labelling rule. The analysis plan was appended to the rule file and exposed the gold answer to at least two readers.
  \item Archive the exact reader prompt, model version string and transcript at the time of the run, not afterwards.
  \item Have an outside pass try to regenerate every table from the packaged files alone. Four such passes here found no numeric error, but they found many claims that outran the record, including an early statement about regeneration that was itself false.
  \item Ask the prompt for what the rule scores. Asking for the letter first while scoring the final commitment is the likely source of the response class on which the estimate now depends; that was not tested with a different prompt.
\end{itemize}

\end{document}
'''
doc=doc.replace(r'\section{Exact Wrappers, SOP, Bootstrap, and Artifact Manifest}',r'\section{Exact Wrappers, SOP, Bootstrap, and Artifact Manifest}\label{app:details}')
for x,y in [(r"The audit below extends that logic to the label-generation step itself.", r"The audits reported above extend that logic to the label-generation step itself."),
            (r" That screen motivated the blind pass and is the ``earlier audit'' referred to below.", r" That screen motivated the blind pass."),
            (r"three adversarial reviews of this manuscript were carried out with Claude, which also drafted substantial parts of the text, in particular Section 7 and the revised abstract, limitations and conclusion.", r"four adversarial reviews of this manuscript were carried out with Claude, which also drafted substantial parts of the text, in particular the abstract, the Introduction, Section 7, the limitations, the conclusion and Appendix \ref{app:lessons}."),
            (r"U2 judgment class (Section 7)", r"U2 judgment class (Section~\ref{sec:u2})"),
            ("check_explicit_commitment.py, finalize.sh;", "check_explicit_commitment.py, make_fig1.py, build_v10.py, finalize.sh;")]:
    assert doc.count(x)==1,(doc.count(x),x[:50]); doc=doc.replace(x,y)
# ---- external manuscript review of 2026-11-19: wording and float placement only ----
for x,y in [(r"An audit that can move labels in one direction will move the estimate in one direction.", r"An audit that only permits one direction of label change can distort estimated contrasts; in this case, the asymmetric correction substantially reduced the estimated interaction."),
            (r"The original manual review had ruled", r"The original adjudication of parser-flagged rows had ruled"),
            (r"manual review of parser-flagged rows, frozen labels", r"separate adjudication of parser-flagged rows, frozen labels"),
            (r"The original manual review is not attributed in the record;", r"The original adjudication of parser-flagged rows is not attributed in the record, so I do not describe it as human or manual;"),
            (r"original manual adjudicator(s)", r"original adjudicator(s)"),
            (r"I ran the experiments, made the methodological decisions recorded in the decision log, and reviewed and approved the final text.", r"I ran the experiments and made the methodological decisions recorded in the decision log.")]:
    assert doc.count(x)==1,(doc.count(x),x[:50]); doc=doc.replace(x,y)
doc=re.sub(r"was manually reviewed\.", "was reviewed outside the parser.", doc)
doc=doc.replace(r"\begin{table}[h]", r"\begin{table}[!htbp]").replace(r"\begin{table}[H]", r"\begin{table}[!htbp]")
left=[m.start() for m in re.finditer(r"manual", doc) if "manual_review" not in doc[m.start():m.start()+14]]
ctx=[doc[i-40:i+30].replace("\n"," ") for i in left]
# ---- PI decision 2026-11-19: drop Arellano et al. (author list could not be verified) ----
x=r"On the judging side, holding responses fixed while varying the grader and rubric shifts jailbreak attack-success rates substantially, leading \citet{arellano2026} to treat the judge--rubric pair as part of the metric, and \citet{messing2026} argues that"
assert doc.count(x)==1; doc=doc.replace(x, r"On the judging side, \citet{messing2026} argues that")
x=r"\citep{biderman2024,arellano2026,messing2026}"; assert doc.count(x)==1; doc=doc.replace(x, r"\citep{biderman2024,messing2026}")
doc,k=re.subn(r"\\bibitem\[Arellano et al\.\(2026\)\]\{arellano2026\}[^\n]*\n", "", doc); assert k==1
assert "rellano" not in doc and "168234" not in doc
n7=doc.count('Section 7'); doc=doc.replace('Section 7',r'Section~\ref{sec:sym}')
assert 'Sections 4, 6 and 7' not in doc
if len(sys.argv)>3 and sys.argv[3]=='final':   # publication copy: no draft header; repo paths as committed
    x=r"\fancyhead[C]{\small\color{red!70!black}DRAFT FOR REVIEW (v10) --- not for submission (Nov 18, 2026)}"
    assert doc.count(x)==1; doc=doc.replace(x, r"\fancyhead[C]{}")
    x=r"paper/ (v8 source)."; assert doc.count(x)==1; doc=doc.replace(x, r"archive/ (v8 and v9 sources).")
open(sys.argv[2],'w').write(doc); print('remaining "manual":',ctx); print('v10 written; "Section 7" references relinked:',n7)
