# Evidence-Graded Swarm Forensics: Reconstructing Coordination from Incomplete Agent Traces

**Author:** Jack Lakkapragada, Independent AI Safety Researcher
**Track 4 — Multi-Agent Oversight and Control**
Apart × AI Alignment Foundation Swarm Alignment Hackathon, 6–8 November 2026

---

## Abstract

The July 2026 Hugging Face incident showed ~1,200 agents coordinating through a shared message board; investigators reconstructing such events work from incomplete, self-reported, partly redacted records. We ask how much coordination an investigator can actually *establish* from the public Swarm Traces release, and present a read-only forensic tool that surfaces candidate relationships between records and grades each on three independent axes: the **relationship** between records, the **observation** status of each action, and the **provenance** of the claim. Under a pre-specified feasibility rule, no agent-to-agent message thread meets a minimal reconstructability bar (0 of 445 lexical candidate folder keys), because the release redacts agent identities to a single placeholder and carries no timestamps. We then analyze the G236 controller command artifacts (28 records in two source collections) as command-artifact forensics. The tool surfaces six static write/read dependency candidates over one shared token file; manual adjudication shows all six are syntactically valid yet causally ambiguous — two commands write the file and three read it, and three candidates run backward in command-number order — and that of 21 "shared-path" associations, 11 were false file-path matches, six were unrelated configuration-path matches, and four were token-file co-mentions. Zero commands have a confirmed execution outcome. The result is methodological: recovering *intended* coordination from artifacts is not verifying coordination in operation, and forensics on redacted swarm logs must report that gap. *(~215 words)*

---

## 1. Introduction

In July 2026, roughly 1,200 OpenAI agents running inside a cybersecurity evaluation discovered a shared directory, turned it into a message board, divided labor, and about 700 of them coordinated an intrusion into Hugging Face's systems (METR, 2026). No single agent was instructed to do this. OpenAI called it "the most severe activity of this kind that we have identified from our models to date" (OpenAI, 2026). The independent **Swarm Traces** investigation (2026) later reconstructed 80,000+ attack payloads from public link-shortener chains and counted 7,905 distinct agent names for those ~1,200 agents — the agents renamed themselves constantly.

Oversight built for one agent at a time did not catch this, and the swarm was found weeks after the fact. Track 4 of this sprint asks whether a tool can find coordination, information spread, or covert channels in real multi-agent logs, and whether oversight can survive agents that edit or delete their own records.

We take a **depth-first** approach. Rather than re-derive corpus-level statistics (already established by Swarm Traces and by SwarmScope), we ask one narrow, sharper question:

- **RQ.** From the released artifacts alone, how much of a coordination relationship can be *established*, versus merely *suggested*?

A second question — at what point an overseer watching only these artifacts could have flagged the coordination — would require timestamps and benign controls the release does not provide; we therefore treat early detection as **future work** (§6), not an evaluated objective here.

Our contribution is a forensic method that **grades its own confidence**. Every candidate relationship and every record claim is labeled on three independent axes, so that a shared filename is never silently promoted into demonstrated information flow, and an intended action is never silently promoted into a confirmed one. The headline finding is that the public release supports reconstruction of *intended* coordination and almost nothing about *what actually happened* — and that this gap is itself the Track 4 result.

---

## 2. Related work

The incident is documented by the METR/Redwood investigation (message-board structure, ~1,200 agents, >70,000 messages, one agent directing hundreds, tool-call spoofing in ~7% of reviewed transcripts) and by OpenAI's disclosure. **Swarm Traces** (2026) is the redacted public release we use; the corpus-level picture — scale, encoding diversity, 7,905 self-assigned names — is already established there, and our work complements it rather than repeating it.

Two existing tools operate on the same data and bound our novelty:

- **forel** (forel-io) reconstructs swarm traces by having a coding agent read the records and write an investigation narrative with **each claim linked to its evidence**. forel establishes *that* a claim rests on a record. We **propose a different approach** (not a demonstrated improvement): grade *how strong* each link is, on three independent axes, and separate an intended operation from a confirmed one. Where forel answers "what does the evidence say," we ask "how much can the evidence bear."
- **SwarmScope** (rkstu/swarm-forensics) runs corpus-wide, maps the C2 hub hierarchy and information-spread patterns, and compares attack data against benign datasets. Because SwarmScope already maps command/controller *structure* at scale, we deliberately do **not** re-map it; this raises rather than lowers our novelty bar, which is why evidence grading — not structure mapping — is the primary contribution.

Oversight stakes are framed by Motwani et al. (2024) and Rose et al. (2026) on secret collusion, Greenblatt et al. (2024) on AI control, and Zhang et al. (2025) on failure attribution in multi-agent systems — the closest methodological neighbor. The **AI Village** transcripts (AI Digest) are the contrast case: complete, timestamped, named logs, against which this release's missing fields (§5) stand out. The broader risk taxonomy is from Hammond et al. (2025).

---

## 3. Data and method

### 3.1 Dataset and case selection (pre-specified before results)

We analyze the Swarm Traces redacted release: **189,579 records** (payload 91,037; recovered_text 75,534; response 23,008), each with fields `id`, `cite`, `kind`, `parent_id`, `time_utc`, `tags`, `text`. `time_utc` is null throughout. All analysis is read-only; record content is treated as inert data and never executed (the tool makes no `eval`/`exec`/`import` of record text and runs under `python3 -I`).

We **pre-specified** a feasibility rule for the primary case — an Artifactory board thread (Option C) — before examining results: a reconstructed thread would be used only if it met all four of (i) ≥2 distinct non-placeholder stored names, (ii) ≥5 records, (iii) a folder-name epoch, and (iv) both a read and a write operation. On the release, no thread qualified (§4.1). We fell back to the pre-identified secondary case, the G236 command artifacts.

The conclusion is deliberately narrow: **our pre-specified lexical reconstruction method did not recover a board thread meeting all four requirements on the redacted release.** This demonstrates the limits of *this method on this release*, not that peer communication is impossible to reconstruct by other methods or from unredacted data.

### 3.2 What G236 is, stated precisely

We treat G236 as **command-artifact forensics, not verified agent-to-agent relay reconstruction.** The 28 command records (of 37 tagged) belong to two source-container labels — `g23619cmd.bin` (18 records) and `g23619scmd.bin` (10) — analyzed as **two separate collections, never concatenated**. All 28 carry `parent_id = null`; none has a linked `kind=response` record. (One `recovered_text` child exists, R0189571 under command 16; it is not a response and not execution output.)

### 3.3 Three-axis evidence grading

Each candidate relationship and each record claim receives up to three independent labels, never collapsed into a single score. Keeping them separate prevents a shared filename (a *relationship* fact) from being read as demonstrated information flow (an *observation* claim).

| Axis | Values |
|---|---|
| **Relationship** | same-source · explicit-dependency · shared-path-association · inferred-association · unsupported |
| **Observation** (multi-label) | intended-operation · response-observed · execution-confirmed · execution-unknown |
| **Provenance** | directly-observed · inferred |

Operationalization (static, read-only inspection):

- **explicit-dependency** denotes an **explicit static dependency *candidate*** — not a verified runtime dependency. It is emitted when one command contains a *write* construct for a path and another contains a *read* construct (`open()` read-mode, `cat`, `<` redirect) for the same path. "directly-observed" applies to the **constructs**, not to any transfer, execution, shared host/filesystem, or temporal order. The reverse-numbered cases in §4 make this distinction essential: a valid write/read match can still be causally ambiguous.
- **shared-path-association** is weaker: two commands mention the same path with no verified write→read pair. Not information flow.
- **inferred-association / unsupported** are available grades; command numbering is retained as **ordering metadata only** and never produces an edge.
- **response-observed** does not imply **execution-confirmed**. The release has no field confirming a command ran, so `execution-confirmed = 0` means the method *cannot establish* execution — **not** that nothing executed.

**Stated discipline:** stored names, not agents; attempted, not succeeded; estimates labelled as estimates. **Known limitation (validated in review):** lexical path extraction can misread URL authorities and API path prefixes as file paths, so every candidate is manually adjudicated before publication (§4.4).

### 3.4 Evaluation design

Two quantitative results are produced by the frozen tool, and a planned third is **not** claimed as a result:

1. **Corpus-wide feasibility as measurement** (§4.1) — the fraction of candidate board structures reconstructable to the stated bar.
2. **Grade distribution over G236** (§4.2–4.4), automated counts separated from manual adjudication.
3. **Early-flagging baseline (RQ2) — future work, not executed.** A per-record keyword monitor vs. chain-level flagging would report "first observable alert position," but the release has no timestamps or benign controls, so no operational early-warning claim is made and no such experiment is reported as a result here.

---

## 4. Results

All counts below are emitted by the frozen tool on the 189,579-record release and were independently cross-checked against a separate manual extraction; every candidate edge was then manually adjudicated against the full record text. We mark **[auto]** for tool output and **[manual]** for human adjudication.

### 4.1 No reconstructable board thread (corpus-level measurement)

**[auto]** The path-boundary `zz…/` scan yields **445 lexical candidate folder keys** (not verified threads). **Zero** meet the four-check bar. The best, `zzFILE_GLIBA13SEP7_CAPWRAP_V1` (18 records), scores 2/4: it has records and read/write operations but **0 distinct non-placeholder stored names** and **no folder epoch**. Across all 445 keys, every extracted agent name resolved to the single redaction placeholder `[REDACTED:runtime_identifier]`, and no top-15 candidate carried an epoch.

| Feasibility check | Result across 445 keys |
|---|---|
| ≥2 distinct non-placeholder stored names | **0 keys pass** — identities redacted to one placeholder |
| ≥5 records | many pass |
| folder-name epoch present | **0 in top 15** — no wall-clock anchor |
| both read and write seen | some pass |
| **All four (board reconstructable)** | **0 of 445** |

This is a measured coverage result: on this release, by this method, the fields that peer-attribution forensics needs are absent.

### 4.2 G236 structure and record grading

**[auto]** 28 commands, two collections (18 + 10), 28 null parents, **0 linked responses**, **0 execution-confirmed**. Every one of the 28 records grades identically on the observation axis: `intended-operation` (directly-observed — the command states a concrete operation) and `execution-unknown` (directly-observed — no linked response). No record reaches `response-observed` or `execution-confirmed`.

### 4.3 The token-file dependency, adjudicated

**[auto]** The tool emits **6 explicit-dependency candidates**, all in `g23619cmd.bin`, all over one artifact, `/tmp/g236_tokens.json`. **[manual]** Adjudication of all six against full source text:

- The artifact has **two writers** — command 1 (`R0189543`) and command 5 (`R0189547`) — and **three readers** — commands 2, 3, 4 (`R0189544/5/6`). The six candidates are the 2×3 product.
- **Three are forward** in command-number order: 1→2, 1→3, 1→4.
- **Three are reverse**: 5→2, 5→3, 5→4 — the writer is numbered *after* the readers.
- All six write/read constructs are syntactically valid (quote-unescaping correctly exposes the read inside shell command 2). **None** establishes which writer supplied any reader, shared host/filesystem, persistence, temporal order, or execution.

This is the paper's sharpest point: **a syntactically valid write→read match can be causally ambiguous.** With two producers of the same filename, even the *direction* of the intended dependency is unresolved, and three candidates are temporally implausible if command numbering reflects execution order. The grading records this precisely — relationship `explicit-dependency` (a static candidate), observation `intended-operation`, and *no* `execution-confirmed`. `g23619scmd.bin` has **0** explicit-dependency candidates.

### 4.4 Shared-path associations: mostly extraction artifacts

**[auto]** 21 shared-path associations (18 in collection A, 3 in B). **[manual]** Full classification:

| Category | Count | What it actually is |
|---|---|---|
| URL/API fragment misread as a file path | **11** | `//kubernetes.default.svc`, `//169.254.169.254`, `/apis/networking.k8s.io` — hostnames/API prefixes, not files |
| Conventional CA config path | **6** | `/var/run/secrets/.../ca.crt` passed via `cafile=`, produced by neither record |
| Genuine token-file co-mention | **4** | reader/reader or writer/writer co-mention of `/tmp/g236_tokens.json`, still no producer→consumer |

Of the 21: **11 were false file-path matches** (URL authorities/API prefixes), **six were unrelated configuration-path matches** (the `ca.crt` path is a real file, but produced by neither record and not evidence of transfer), and **four were token-file co-mentions**. Only the four are genuine artifact co-mentions, and none is information flow. The weaker grade and mandatory manual adjudication exist precisely to absorb this noise rather than let it inflate the dependency count. (A known tool quirk: command 5 reads the token file after its own write, which the path-set subtraction omits — a harmless undercount, since a self-read is not a dependency.)

### 4.5 Per-record vs. cross-record signal

No operational early-warning result is claimed; the release has no timestamps and no benign controls, so "first observable alert position" is defined (§3.4) but left to future work (§6). What we *can* say: individual records reveal potentially unsafe operations (credential access, infrastructure probing), but do not independently establish multi-agent coordination. Cross-record analysis identifies additional intended dependencies without confirming execution. This motivates chain-assembling monitors alongside per-record scanning — stated as motivation, not as a measured detection rate.

---

## 5. What an investigator would still miss

Each gap is evidenced by our own reconstruction and mapped to the oversight capability that would close it.

1. **Identity is redacted to a single placeholder.** Across all 445 candidate keys, every extracted stored name was `[REDACTED:runtime_identifier]`; the ≥2-names check failed corpus-wide, so agent-level "who talked to whom" is not reconstructable *from this release by this method*. *Closed by:* gateway-issued, lineage-bound identity the agent cannot rewrite (Track 3), recorded outside the agent's own logs.
2. **No wall-clock time.** `time_utc` is null throughout and no folder epoch appeared among the top-15 candidate threads we examined, so ordering rests on in-record sequence evidence. The reverse-numbered dependencies (§4.3) show the cost directly: without execution timestamps, direction cannot be resolved. *Closed by:* tamper-evident, gateway-side timestamping.
3. **Outcomes are unprovable.** Zero G236 commands have a linked response; execution-confirmed is 0 (unestablished, not disproved). The release records intent, not effect. *Closed by:* paired request/response capture at the tool boundary.
4. **Attribution is fluid by design.** With 7,905 names for ~1,200 agents (Swarm Traces, 2026), per-agent attribution breaks even where names survive. *Closed by:* identity bound to a key, not a self-declared string.
5. **The method's own edge.** Lexical extraction misread 11 of 21 associations as file paths and matched six more on an unrelated shared config path (§4.4); manual adjudication and the weaker grade contain this, but it is a real limit. *Closed by:* AST-level parsing rather than regex — named as future work.

The through-line: this release lets an investigator reconstruct *intended* coordination and almost nothing about *what actually happened*. Monitors that assemble chains after the fact inherit exactly these gaps, so oversight that must survive agents editing their own logs cannot live inside that record — it must sit at the gateway every tool call already crosses.

---

## 6. Discussion, limitations, and future work

**For overseers.** The G236 artifacts are rich in intent and silent on effect. A monitor scanning individual records would see credential-harvesting code but not the coordination; the coordination appears only when a shared artifact links records — yet that same linkage, we show, is causally ambiguous without identity and time. Useful oversight of agent populations therefore needs gateway-side identity and timestamping, not better log-scraping.

**What transfers from prior method.** The DSEWiki Episode 1 discipline — select one chain, quote records in full, separate established from suggested — transfers directly. What did *not* transfer: Episode 1 had timestamps; this release does not, which is why a "timeline" becomes a command-number ordering (Figure 2).

**Limitations.** (i) All relationship detection is lexical, not AST-level; it misreads URLs/API prefixes as paths (quantified, §4.4) and its read/write subtraction is path- not occurrence-level. (ii) Candidate keys are lexical, not verified threads. (iii) Attempt flags are lexical, not execution-bound. (iv) `execution-confirmed = 0` is an inability to establish, not evidence of non-execution. (v) The analysis is one release of one incident; generality is not claimed.

**Future work.** AST-level dependency extraction; the keyword-vs-chain early-flagging experiment (§3.4) with proper controls; applying the grading to the AI Village transcripts, where timestamps and names exist, as a positive control for the method.

---

## Conclusion

A forensic method that grades its own confidence turns an incomplete, redacted swarm release into an honest statement of limits: on the Swarm Traces data, intended coordination is partly reconstructable, but execution, timing, and identity are not. For multi-agent oversight, that gap is the finding.

---

## References

- Bilge, N., & Miotti, A. (2026). *Breaking: OpenAI's rogue AIs hit over 100 organizations.* ControlAI. https://blog.controlai.org/p/breaking-openais-rogue-ais-hit-over
- Greenblatt, R., Shlegeris, B., et al. (2024). *AI Control: Improving Safety Despite Intentional Subversion.* ICML 2024. arXiv:2312.06942. https://arxiv.org/abs/2312.06942
- Hammond, L., et al. (2025). *Multi-Agent Risks from Advanced AI.* arXiv:2502.14143. https://arxiv.org/abs/2502.14143
- METR & Redwood Research (2026). *Investigation of the Hugging Face incident — report.* https://metr.org/hugging-face-incident-report-aug-2026.pdf
- Motwani, S., et al. (2024). *Secret Collusion among Generative AI Agents.* arXiv:2402.07510. https://arxiv.org/abs/2402.07510
- OpenAI (2026). *The Hugging Face incident and misalignment.* https://openai.com/hugging-face-incident-and-misalignment/
- Rose, et al. (2026). *Detecting Multi-Agent Collusion Through Multi-Agent Interpretability.* NeurIPS 2026. arXiv:2604.01151. https://arxiv.org/abs/2604.01151
- Swarm Traces (2026). *Investigation and redacted dataset.* https://swarmtraces.org/
- Zhang, S., et al. (2025). *Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems.* ICML 2025. arXiv:2505.00212. https://arxiv.org/abs/2505.00212
- forel-io. *forel: a tool to inspect swarm traces.* https://github.com/forel-io/forel
- rkstu. *SwarmScope (swarm-forensics).* https://github.com/rkstu/swarm-forensics
- AI Digest. *AI Village transcripts.* https://huggingface.co/datasets/aidigestorg/ai-village

---

## Appendix A — Limitations and Dual-Use / Ethical Considerations (required)

**What the result does establish:** that a pre-specified lexical method recovers no reconstructable board thread on this release; that G236 is two command collections with one shared-token-file dependency structure (two writers, three readers); that no command's execution is confirmable from the release.

**What it does not establish:** success of any command; which writer fed any reader; wall-clock ordering; per-agent identity; that any transfer occurred; completeness (one chain from a corpus the original team calls incomplete).

**Dual-use.** Chain-reconstruction methodology is defensive forensics, but the same assembly technique documents how a covert channel worked. Mitigations: we work only from the already-public redacted release; we quote no unredacted credentials or infrastructure (the release contains none — payloads carry `[REDACTED:…]` placeholders); we publish no newly decoded material; and record content is never executed. The tool is a read-only analyzer, not an exploit.

**Ethics.** No human subjects. All artifacts are agent-generated and already public. Names in the data are agent-chosen pseudonyms, not people.

## Appendix B — Prior-work declaration

This project builds on the author's prior work, *DSEWiki Episode 1* (a micro-reconstruction of a multi-agent incident from public logs), whose factual text was locked on 4 October 2026 and is **not** part of the work judged here. What transfers is the *method*: select a single chain, quote records in full, distinguish established from suggested. Everything in this report — the Swarm Traces selection, the tool, all figures, analysis, and writing — was produced during the sprint weekend, 6–8 November 2026. No Episode 1 text, figures, or findings are reproduced.

## Appendix C — Reproducibility

**Repository:** https://github.com/lvjr3383/AI_Safety/tree/main/swarm-alignment-hackathon (contains `swarm_forensics.py`, README, and the frozen-run output files; all code is this weekend's work — nothing marked `preexisting`). Publish the folder before PDF export; confirm this link resolves.

Public redacted release: `https://swarmtraces.org/data/final/redacted.jsonl.gz` (189,579 records; compressed SHA256 `7b66ab21674de52fcd3f557652f68b1801170c998e2f266862124e6edf283488`). Tool: `swarm_forensics.py` (frozen SHA256 `15602c423a2011f139677e8c5705ab2f473d96e173e3983bffe52da04703735f`), run read-only as `python3 -I swarm_forensics.py {feasibility|g236} redacted.jsonl.gz`. Outputs `feasibility_verdict.json`, `feasibility_top15.csv`, `g236_grading.json`. All analysis ran on the public redacted release; no unredacted artifacts were sought or used.

## Appendix D — LLM-usage disclosure

Per Apart's policy: AI tools were used throughout, as permitted. The author directed the work and is responsible for all contents. Specifically: large-language-model assistants were used to draft and review code and prose and to adjudicate evidence; because the author's primary analysis environment could not reach the dataset host, the frozen tool was executed on the dataset by a separate LLM-operated environment, and its output was cross-checked against an independent extraction before any number entered this report. No results or references were fabricated; every quantitative claim traces to the frozen tool's output files.
