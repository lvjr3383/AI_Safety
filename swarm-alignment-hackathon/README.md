# Evidence-Graded Swarm Forensics

Read-only forensic tooling for the Apart **Swarm Alignment Hackathon**, Track 4
(Multi-Agent Oversight and Control). It implements the locked §3 methodology:
the Option C feasibility rule, the two-collection G236 separation, and the
three-axis evidence grading.

Author: Jack Lakkapragada, Independent AI Safety Researcher.

## Inertness guarantee

Record content is untrusted inert **data**. The tool never calls
`eval` / `exec` / `compile` / `__import__` on record text, never imports or runs
any payload, and inspects text only with regular expressions and string ops.
Run it with `-I` so the interpreter ignores the working directory and env:

```bash
python3 -I swarm_forensics.py selfcheck      # synthetic tests, no real data
```

## Data

Download the Swarm Traces **redacted** release yourself (the tool makes no
network calls):

```bash
curl -LO https://swarmtraces.org/data/final/redacted.jsonl.gz
```

Expected: 189,579 records; 7 fields each (`id, cite, kind, parent_id, time_utc,
tags, text`); `time_utc` null throughout; 37 tagged records, 28 carrying
`g236-command`. Keep the downloaded file in its own directory.

## Run

```bash
# Option C (board-thread) pre-specified feasibility rule + verdict
python3 -I swarm_forensics.py feasibility /path/to/redacted.jsonl.gz --out results/

# G236 command-artifact forensics + three-axis grading
python3 -I swarm_forensics.py g236 /path/to/redacted.jsonl.gz --out results/
```

Outputs: `feasibility_verdict.json`, `feasibility_top15.csv`, `g236_grading.json`.

## Grading schema (locked §3)

| Axis | Values |
|---|---|
| **Relationship** | same-source · explicit-dependency · inferred-association · unsupported |
| **Observation** (multi-label) | intended-operation · response-observed · execution-confirmed · execution-unknown |
| **Provenance** | directly-observed · inferred |

Rules enforced in code:
- The two G236 source containers (`g23619cmd.bin`, `g23619scmd.bin`) are graded
  as **separate collections**; no cross-source link is ever created.
- A linked `response` yields `response-observed`, which does **not** establish
  `execution-confirmed`.
- Stored names that are redaction placeholders do not count toward the
  feasibility name check.
- "Candidate thread keys" are **lexical** folder keys, not verified Artifactory
  threads.

## Scope & honesty

G236 is **command-artifact forensics, not verified agent-to-agent relay
reconstruction.** Write/read tokens are attempted operations, not proof of
execution. All analysis runs on the public redacted release; no unredacted
artifacts are sought or used.

## Prior work

Builds on the author's method from *DSEWiki Episode 1* (locked 2026-10-04):
single-chain reconstruction, quote records in full, distinguish established from
suggested. Only this weekend's work is judged. Any reused pre-sprint code is
marked `preexisting`. This tool was written during the sprint.

## Repository layout

```
swarm-alignment-hackathon/
├── swarm_forensics.py        # the frozen read-only tool (SHA256 15602c42…703735f)
├── README.md
├── docs/
│   └── manuscript.md         # the research report
├── figures/
│   ├── figure1.(svg|png)     # relationship map
│   └── figure2.(svg|png)     # command-number ordering
└── outputs/                  # frozen-run artifacts (reproduce by running the tool)
    ├── feasibility_verdict.json / feasibility_top15.csv / feasibility_console.txt
    ├── g236_grading.json / g236_console.txt
    ├── selfcheck_console.txt
    ├── manual_review.txt / manual_edge_review.json   # human adjudication of every edge
    └── artifact_manifest.json                        # SHA256s of all output files
```

## Reproduce

```bash
curl -LO https://swarmtraces.org/data/final/redacted.jsonl.gz
# compressed SHA256: 7b66ab21674de52fcd3f557652f68b1801170c998e2f266862124e6edf283488
python3 -I swarm_forensics.py selfcheck
python3 -I swarm_forensics.py feasibility redacted.jsonl.gz --out outputs/
python3 -I swarm_forensics.py g236        redacted.jsonl.gz --out outputs/
```

The `outputs/` here are the frozen run on the 189,579-record release. All analysis is
read-only; no record content is executed. Nothing in this repository is pre-existing
code — all of it is the sprint weekend's work.

## Publication packaging

`outputs/script_sha256_before.txt` and `outputs/script_sha256_after.txt` were absent from the zip. Both were restored from exact originals: 101 bytes, SHA256 `0283bf6c27ddc3945d057d8884ad1b5a8259147bea4191d8fd4dbaa01c153e15`. Each file is one digest line for the frozen script.

`outputs/reviewed_edge_sources_full.txt` is omitted. An exact original matching the previous manifest entry exists, but that file is recovered command-source text, so it is not published and was not replaced. Its entry was removed from `outputs/artifact_manifest.json`.

`swarm_forensics.py` is the archive file with only its final trailing newline removed. Its SHA256 is `15602c423a2011f139677e8c5705ab2f473d96e173e3983bffe52da04703735f`.
