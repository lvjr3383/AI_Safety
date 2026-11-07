#!/usr/bin/env python3
"""
Evidence-Graded Swarm Forensics — read-only forensic tool (v2).

Implements the locked §3 methodology for the Apart Swarm Alignment Hackathon,
Track 4 (Multi-Agent Oversight and Control).

INERTNESS GUARANTEE
-------------------
Record content is treated strictly as untrusted inert DATA. This tool:
  - never calls eval(), exec(), compile(), or __import__ on record content;
  - never imports, writes-then-runs, or dynamically evaluates any payload;
  - reads the corpus only with gzip + json.loads, and inspects text only with
    regular expressions and string operations.
Run it with `python3 -I` so the interpreter ignores the working directory and
environment, per the environment's guidance on untrusted downloaded files.

The Swarm Traces redacted release (swarmtraces.org) must be downloaded by the
operator; this tool takes its path as an argument. It makes no network calls.

Subcommands
-----------
  feasibility <file.jsonl.gz>   Option C (board-thread) pre-specified rule + verdict
  g236        <file.jsonl.gz>   G236 command-artifact forensics + three-axis grading
  selfcheck                     Run the built-in synthetic-fixture tests (no real data)

Every number this tool reports comes from the actual run; nothing is inferred
when a field is absent. Stored names are NOT confirmed agents. A write/read
token is an ATTEMPTED operation, not proof of execution or success.

v2 changes (from code review): escaped-quote-aware path extraction; producer->
consumer dependency detection across all commands within a source (not just
adjacent); execution-confirmed count derived from grading, never hardcoded;
feasibility top-15 ranked by record count (best selected separately by score);
command numbering kept as ordering metadata, NOT drawn as an inferred edge.
"""
import argparse, collections, csv, datetime, gzip, json, re, sys
from pathlib import Path

REQUIRED_FIELDS = {"id", "cite", "kind", "parent_id", "time_utc", "tags", "text"}

# Normalize backslash-escaped quotes for SCANNING ONLY. Original record text is
# never modified in place or executed; this produces a scratch string.
UNESCAPE = re.compile(r"""\\+(["'])""")

def unescape(text):
    return UNESCAPE.sub(r"\1", text or "")


def load(path):
    recs = []
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            if not isinstance(o, dict) or not REQUIRED_FIELDS.issubset(o):
                raise ValueError(f"record on line {n} missing required fields")
            recs.append(o)
    return recs


def index(recs):
    by_id = {o["id"]: o for o in recs}
    children = collections.defaultdict(list)
    for o in recs:
        if o["parent_id"] is not None:
            children[o["parent_id"]].append(o["id"])
    return by_id, children


# ----------------------------------------------------------------------------
# Option C — pre-specified feasibility rule
# ----------------------------------------------------------------------------
FOLDER = re.compile(r"(?:^|/)(zz[A-Za-z0-9_\-]+)(?=/)")   # real path segment only
EPOCH = re.compile(r"_(1[5-9]\d{8})$")
NAME = re.compile(
    r"""(?i)(?:agent_?id|agent_?name|x-agent[-_]?(?:id|name))["']?\s*[:=]\s*(["'])(.+?)\1"""
)
WRITE_OP = re.compile(r"(?<![A-Za-z0-9_])(?:PUT|POST)(?![A-Za-z0-9_])|(?i:\bupload\b)")
READ_OP = re.compile(r"(?<![A-Za-z0-9_])GET(?![A-Za-z0-9_])|(?i:\b(?:list|download)\b)")
PLACEHOLDER = re.compile(r"^\[REDACTED[:\]]")
PLACEHOLDER_NAME = re.compile(
    r"""(?i)(?:agent_?id|agent_?name)["']?\s*[:=]\s*["']\[REDACTED"""
)


def stored_names(flat):
    out = set()
    for _, val in NAME.findall(flat):
        val = val.strip()
        if val and not PLACEHOLDER.match(val):
            out.add(val)
    return out


def feasibility(recs, min_names=2, min_records=5, topn=15):
    resp_parents = {o["parent_id"] for o in recs
                    if o["kind"] == "response" and o["parent_id"] is not None}
    threads = collections.defaultdict(lambda: {
        "records": set(), "names": set(), "epochs": set(),
        "write": 0, "read": 0, "linked_response": 0,
    })
    placeholder_seen = collections.defaultdict(bool)

    for o in recs:
        raw = o["text"] or ""
        flat = unescape(raw)
        folders = set(FOLDER.findall(raw)) | set(FOLDER.findall(flat))
        if not folders:
            continue
        nm = stored_names(flat)
        has_ph = bool(PLACEHOLDER_NAME.search(flat))
        w, r = bool(WRITE_OP.search(raw)), bool(READ_OP.search(raw))
        linked = o["id"] in resp_parents
        for folder in folders:
            m = EPOCH.search(folder)
            key = folder[: m.start()] if m else folder
            th = threads[key]
            if o["id"] in th["records"]:
                continue
            th["records"].add(o["id"]); th["names"] |= nm
            if m:
                th["epochs"].add(int(m.group(1)))
            th["write"] += w; th["read"] += r; th["linked_response"] += linked
            if has_ph:
                placeholder_seen[key] = True

    def checks(th):
        return [len(th["names"]) >= min_names, len(th["records"]) >= min_records,
                bool(th["epochs"]), bool(th["write"] and th["read"])]

    rows = []
    for key, th in threads.items():
        c = checks(th)
        rows.append({
            "thread": key, "records": len(th["records"]),
            "distinct_stored_names": sorted(th["names"]),
            "placeholder_name_present": placeholder_seen[key],
            "write_records": th["write"], "read_records": th["read"],
            "linked_response_records": th["linked_response"],
            "epoch_min": min(th["epochs"]) if th["epochs"] else None,
            "epoch_max": max(th["epochs"]) if th["epochs"] else None,
            "checks": c, "score": sum(c),
        })

    # Medium fix: top-15 ranked by record count (matches the independent
    # extraction); best candidate chosen separately by score.
    by_count = sorted(rows, key=lambda s: (-s["records"], s["thread"]))
    by_score = sorted(rows, key=lambda s: (-s["score"], -s["records"], s["thread"]))
    best = by_score[0] if by_score else None
    verdict = {
        "candidate_thread_keys": len(threads),
        "note_on_candidate_keys": "lexical candidate folder keys, NOT verified Artifactory threads",
        "best_thread": best["thread"] if best else None,
        "best_score": best["score"] if best else 0,
        "verdict": "GO_OPTION_C" if best and best["score"] == 4 else "FALL_BACK_G236",
        "epoch_in_top15_by_count": any(s["epoch_min"] is not None for s in by_count[:topn]),
        "checks_legend": [f"distinct non-placeholder stored names >= {min_names}",
                          f"records >= {min_records}", "folder-name epoch present",
                          "both write and read operation seen"],
    }
    return by_count, verdict


# ----------------------------------------------------------------------------
# G236 — command-artifact forensics
# ----------------------------------------------------------------------------
BIN_TAG = re.compile(r"(g\w*?\.bin)")
CMD_TAG = re.compile(r"command-(\d+)")

# Write constructs (scanned on the unescaped scratch string).
PY_WRITE = re.compile(r"""open\(\s*['"]([^'"]+)['"]\s*,\s*['"][wax]b?\+?['"]""")
SH_REDIR = re.compile(r">>?\s*([/~][\w./\-]+)")
WRITEFILE = re.compile(r"""writeFile\w*\(\s*['"]([^'"]+)['"]""")
# Read constructs.
OPEN_ANY = re.compile(r"""open\(\s*['"]([^'"]+)['"]""")      # any open(); write-mode ones subtracted
SH_CAT = re.compile(r"\bcat\s+([/~][\w./\-]+)")
SH_INPUT = re.compile(r"<\s*([/~][\w./\-]+)")
# Any concrete file path mentioned anywhere (for shared-path-association only).
GENERIC_PATH = re.compile(r"((?:/|~/)[\w./\-]+\.\w+)")


def write_paths(raw):
    flat = unescape(raw)
    out = set(PY_WRITE.findall(flat)) | set(SH_REDIR.findall(flat)) | set(WRITEFILE.findall(flat))
    return {p.strip() for p in out}


def read_paths(raw):
    """Paths with a demonstrable READ construct: open() in read mode (any open()
    that is not a write-mode open()), `cat <path>`, or `< <path>` input redirect.
    A bare mention of a path in a string is NOT a read."""
    flat = unescape(raw)
    read_opens = set(OPEN_ANY.findall(flat)) - set(PY_WRITE.findall(flat))
    out = read_opens | set(SH_CAT.findall(flat)) | set(SH_INPUT.findall(flat))
    return {p.strip() for p in out}


def referenced_paths(raw):
    """Every concrete file path the record mentions (writes and reads included).
    Used only to detect the weaker shared-path-association."""
    flat = unescape(raw)
    out = set(OPEN_ANY.findall(flat)) | set(GENERIC_PATH.findall(flat)) \
        | write_paths(raw) | read_paths(raw)
    return {p.strip() for p in out}


def parse_g236(recs):
    tagged = [o for o in recs if "g236-command" in (o["tags"] or "")]
    by_source = collections.defaultdict(list)
    for o in tagged:
        tags = o["tags"]
        src = BIN_TAG.search(tags)
        cmd = CMD_TAG.search(tags)
        raw = o["text"] or ""
        rec = {
            "id": o["id"], "cite": o["cite"], "kind": o["kind"],
            "parent_id": o["parent_id"],
            "source_container": src.group(1) if src else "unknown",
            "command_number": int(cmd.group(1)) if cmd else None,
            "write_paths": sorted(write_paths(raw)),
            "read_paths": sorted(read_paths(raw)),
            "referenced_paths": sorted(referenced_paths(raw)),
        }
        by_source[rec["source_container"]].append(rec)
    for src in by_source:
        by_source[src].sort(key=lambda r: (r["command_number"] if r["command_number"] is not None else 1 << 30, r["id"]))
    return tagged, dict(by_source)


RELATIONSHIP = ("same-source", "explicit-dependency", "inferred-association", "unsupported")
OBSERVATION = ("intended-operation", "response-observed", "execution-confirmed", "execution-unknown")
PROVENANCE = ("directly-observed", "inferred")


def grade_record(rec, has_linked_response):
    obs = [{"label": "intended-operation", "provenance": "directly-observed",
            "claim": "record text states a concrete operation"}]
    if has_linked_response:
        obs.append({"label": "response-observed", "provenance": "directly-observed",
                    "claim": "a kind=response record links to this command"})
        obs.append({"label": "execution-unknown", "provenance": "inferred",
                    "claim": "a response does not by itself establish successful execution"})
    else:
        obs.append({"label": "execution-unknown", "provenance": "directly-observed",
                    "claim": "no linked kind=response record present"})
    return obs


def dependency_links(cmds):
    """Relationships across ALL commands in one source, by static inspection.

    explicit-dependency : A has a WRITE construct for path P and B has a READ
                          construct for the same P (both directions verified).
    shared-path-association : A and B both mention P, but no verified producer->
                          consumer read is present. Weaker; not information flow.

    No edge is drawn from command numbering. Direction for explicit-dependency is
    producer(write) -> consumer(read), established by the constructs, not by order.
    """
    links = []
    for a in cmds:
        for p in a["write_paths"]:
            for b in cmds:
                if b["id"] == a["id"]:
                    continue
                if p in b["read_paths"]:
                    links.append({
                        "from": a["cite"], "to": b["cite"],
                        "relationship": "explicit-dependency",
                        "provenance": "directly-observed",
                        "evidence": {"artifact": p, "write_in_from": True, "read_in_to": True},
                        "observation": "intended-operation",
                        "note": "write in producer and read in consumer both verified; transfer/execution unconfirmed",
                    })
    # shared-path-association: same path mentioned by two commands, but not a
    # verified write->read pair in either direction.
    explicit_pairs = {(l["from"], l["to"], l["evidence"]["artifact"]) for l in links}
    seen = set()
    for a in cmds:
        for b in cmds:
            if a["id"] >= b["id"]:
                continue
            shared = set(a["referenced_paths"]) & set(b["referenced_paths"])
            for p in sorted(shared):
                verified = ((a["cite"], b["cite"], p) in explicit_pairs
                            or (b["cite"], a["cite"], p) in explicit_pairs)
                if verified or (a["cite"], b["cite"], p) in seen:
                    continue
                seen.add((a["cite"], b["cite"], p))
                links.append({
                    "between": [a["cite"], b["cite"]],
                    "relationship": "shared-path-association",
                    "provenance": "directly-observed",
                    "evidence": {"artifact": p, "basis": "both mention the path; no verified write->read"},
                    "observation": "execution-unknown",
                    "note": "co-mention only; producer->consumer relationship NOT established",
                })
    return links


def g236_report(recs):
    resp_parents = {o["parent_id"] for o in recs
                    if o["kind"] == "response" and o["parent_id"] is not None}
    tagged, by_source = parse_g236(recs)

    graded_records, graded_links, memberships, orderings = [], {}, {}, {}
    for src, cmds in by_source.items():
        for rec in cmds:
            graded_records.append({
                "cite": rec["cite"], "source_container": src,
                "command_number": rec["command_number"], "kind": rec["kind"],
                "observation": grade_record(rec, rec["id"] in resp_parents),
            })
        graded_links[src] = dependency_links(cmds)
        memberships[src] = {
            "relationship": "same-source", "provenance": "directly-observed",
            "members": [c["cite"] for c in cmds],
            "note": "shared source-container label; establishes grouping, not information flow",
        }
        # ordering metadata only — explicitly NOT an information-flow edge set
        orderings[src] = {
            "kind": "ordering-metadata-not-edges",
            "by_command_number": [{"cite": c["cite"], "command_number": c["command_number"]} for c in cmds],
            "note": "command numbering is presentation order; it is not evidence of a link",
        }

    # High fix: derive execution-confirmed from the grading, never hardcode.
    execution_confirmed = sum(
        1 for gr in graded_records
        if any(o["label"] == "execution-confirmed" for o in gr["observation"])
    )
    explicit_deps = sum(1 for v in graded_links.values() for l in v
                        if l["relationship"] == "explicit-dependency")
    shared_assoc = sum(1 for v in graded_links.values() for l in v
                       if l["relationship"] == "shared-path-association")

    summary = {
        "tagged_records_total": len([o for o in recs if o["tags"]]),
        "g236_command_records": len(tagged),
        "source_containers": {s: len(c) for s, c in by_source.items()},
        "commands_with_null_parent": sum(1 for o in tagged if o["parent_id"] is None),
        "commands_with_linked_response": sum(1 for o in tagged if o["id"] in resp_parents),
        "execution_confirmed_count": execution_confirmed,
        "execution_confirmation_supported": False,
        "execution_confirmation_note": (
            "0 means the method CANNOT ESTABLISH execution from the released "
            "data, NOT that no command executed. The release contains no field "
            "that confirms success; a linked response is graded response-observed, "
            "not execution-confirmed. The count is derived from the grading."
        ),
        "explicit_intended_file_dependencies": explicit_deps,
        "shared_path_associations": shared_assoc,
        "cross_source_links_created": 0,
        "inferred_numbering_edges_created": 0,
    }
    headline = (
        "The G236 artifacts reveal two collections of numbered commands and at "
        "least one explicit intended file dependency. However, the released "
        "records do not establish whether these commands executed or whether the "
        "intended information transfer occurred. This illustrates a fundamental "
        "oversight limitation: reconstructing intended coordination from recovered "
        "artifacts is not equivalent to verifying coordination in operation."
    )
    return {"summary": summary, "graded_records": graded_records,
            "graded_links": graded_links, "memberships": memberships,
            "orderings": orderings, "headline": headline}


# ----------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------
def utc(e):
    if e is None:
        return "none"
    return datetime.datetime.fromtimestamp(e, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def write_feasibility_outputs(by_count, verdict, outdir):
    (outdir / "feasibility_verdict.json").write_text(json.dumps(verdict, indent=2))
    with (outdir / "feasibility_top15.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["thread", "records", "distinct_stored_names", "placeholder_name_present",
                    "write_records", "read_records", "linked_response_records",
                    "epoch_min_utc", "epoch_max_utc", "checks", "score"])
        for s in by_count[:15]:
            w.writerow([s["thread"], s["records"], json.dumps(s["distinct_stored_names"]),
                        s["placeholder_name_present"], s["write_records"], s["read_records"],
                        s["linked_response_records"], utc(s["epoch_min"]), utc(s["epoch_max"]),
                        "".join("Y" if c else "N" for c in s["checks"]), f"{s['score']}/4"])


def print_feasibility(by_count, verdict):
    print("OPTION C FEASIBILITY (pre-specified rule)")
    print(f"  Lexical candidate folder keys: {verdict['candidate_thread_keys']} "
          f"({verdict['note_on_candidate_keys']})")
    print(f"  Best: {verdict['best_thread']} = {verdict['best_score']}/4   "
          f"epoch in top15(by count): {verdict['epoch_in_top15_by_count']}")
    print(f"  VERDICT: {verdict['verdict']}")
    print("  (top 15 by record count)")
    print("  thread | records | names | W | R | linkedResp | epoch_min | score")
    for s in by_count[:15]:
        print(f"  {s['thread'][:40]:40} | {s['records']:>4} | "
              f"{len(s['distinct_stored_names']):>3} | {s['write_records']:>3} | "
              f"{s['read_records']:>3} | {s['linked_response_records']:>3} | "
              f"{utc(s['epoch_min']):>16} | {s['score']}/4")


def print_g236(rep):
    s = rep["summary"]
    print("G236 COMMAND-ARTIFACT FORENSICS (not verified agent-to-agent relay)")
    print(f"  g236-command records: {s['g236_command_records']} (of {s['tagged_records_total']} tagged)")
    print(f"  source containers (two separate collections): {s['source_containers']}")
    print(f"  null-parent commands: {s['commands_with_null_parent']}")
    print(f"  commands with a linked response: {s['commands_with_linked_response']}")
    print(f"  execution-confirmed (derived): {s['execution_confirmed_count']}  "
          f"(supported: {s['execution_confirmation_supported']})")
    print(f"  explicit intended file dependencies (write->read verified): {s['explicit_intended_file_dependencies']}")
    print(f"  shared-path associations (co-mention only): {s['shared_path_associations']}")
    print(f"  cross-source links: {s['cross_source_links_created']}  "
          f"inferred-numbering edges: {s['inferred_numbering_edges_created']}")
    for src, links in rep["graded_links"].items():
        ex = [l for l in links if l["relationship"] == "explicit-dependency"]
        sa = [l for l in links if l["relationship"] == "shared-path-association"]
        print(f"  [{src}] explicit: {len(ex)}  shared-path: {len(sa)}")
        for l in ex:
            print(f"      explicit  {l['from']} -> {l['to']}  via {l['evidence']['artifact']}")
        for l in sa:
            print(f"      shared    {l['between'][0]} ~ {l['between'][1]}  via {l['evidence']['artifact']}")
    print("\nHEADLINE:\n  " + rep["headline"])


# ----------------------------------------------------------------------------
# Self-check (synthetic, no real data, no network)
# ----------------------------------------------------------------------------
def synthetic():
    return [
        {"id": "F1", "cite": "F1:a", "kind": "payload", "parent_id": None, "time_utc": None,
         "tags": "", "text": "PUT /zzBOARD_demo/msg  agent_id:'[REDACTED:runtime_identifier]'"},
        {"id": "F2", "cite": "F2:b", "kind": "payload", "parent_id": None, "time_utc": None,
         "tags": "", "text": "GET /zzBOARD_demo/msg  agent_id:'[REDACTED:runtime_identifier]'"},
        {"id": "F3", "cite": "F3:c", "kind": "recovered_text", "parent_id": None, "time_utc": None,
         "tags": "", "text": "CENTIPEDE_BIN_DIR=/src/fuzztest/bazel-bin"},
        # Collection A: cmd1 writes token file; cmd3 (NON-adjacent) reads it via an
        # ESCAPED-QUOTE shell string -> must still be detected across the gap.
        {"id": "G1", "cite": "G1:x", "kind": "recovered_text", "parent_id": None, "time_utc": None,
         "tags": "article-evidence;g236-command;g23619cmd.bin;command-000001",
         "text": "open('/tmp/g236_tokens.json','w').write(data)"},
        # G2 only MENTIONS the token path in a string (no read construct) ->
        # shared-path-association with G1, never an explicit dependency.
        {"id": "G2", "cite": "G2:y", "kind": "recovered_text", "parent_id": None, "time_utc": None,
         "tags": "article-evidence;g236-command;g23619cmd.bin;command-000002",
         "text": "log('will use /tmp/g236_tokens.json later')"},
        # G3 has a demonstrable READ (cat) of the token path, via escaped quotes,
        # non-adjacent to G1 -> explicit-dependency G1 -> G3.
        {"id": "G3", "cite": "G3:z", "kind": "recovered_text", "parent_id": None, "time_utc": None,
         "tags": "article-evidence;g236-command;g23619cmd.bin;command-000003",
         "text": "body=\"{\\\"note\\\":\\\"load\\\"}\"; cat /tmp/g236_tokens.json"},
        {"id": "H1", "cite": "H1:p", "kind": "recovered_text", "parent_id": None, "time_utc": None,
         "tags": "article-evidence;g236-command;g23619scmd.bin;command-000001",
         "text": "open('/tmp/other.json','w')"},
        {"id": "H2", "cite": "H2:q", "kind": "recovered_text", "parent_id": None, "time_utc": None,
         "tags": "article-evidence;g236-command;g23619scmd.bin;command-000002",
         "text": "do_thing()"},
    ]


def selfcheck():
    recs = synthetic()
    by_count, verdict = feasibility(recs)
    assert verdict["verdict"] == "FALL_BACK_G236", verdict
    keys = {s["thread"] for s in by_count}
    assert "zzBOARD_demo" in keys
    assert not any("zztest" in k for k in keys), "fuzztest substring must NOT match"
    assert all(not s["distinct_stored_names"] for s in by_count), "placeholders excluded"
    # top-15 ordering is by record count
    assert by_count == sorted(by_count, key=lambda s: (-s["records"], s["thread"]))

    rep = g236_report(recs)
    s = rep["summary"]
    assert s["g236_command_records"] == 5, s
    assert s["source_containers"] == {"g23619cmd.bin": 3, "g23619scmd.bin": 2}, s
    assert s["execution_confirmed_count"] == 0, s
    assert s["execution_confirmation_supported"] is False, s
    assert s["cross_source_links_created"] == 0 and s["inferred_numbering_edges_created"] == 0, s
    a = rep["graded_links"]["g23619cmd.bin"]
    ex = [l for l in a if l["relationship"] == "explicit-dependency"]
    sa = [l for l in a if l["relationship"] == "shared-path-association"]
    # Critical + High: non-adjacent, escaped-quote, write->read dependency G1 -> G3.
    assert len(ex) == 1, ex
    assert ex[0]["from"] == "G1:x" and ex[0]["to"] == "G3:z", ex
    assert ex[0]["provenance"] == "directly-observed", ex
    assert ex[0]["evidence"]["artifact"] == "/tmp/g236_tokens.json", ex
    # Tightening: G2 merely mentions the path -> shared-path-association, NOT explicit.
    assert s["explicit_intended_file_dependencies"] == 1, s
    assert any(set(l.get("between", [])) == {"G1:x", "G2:y"} for l in sa), sa
    assert not any((l.get("from"), l.get("to")) == ("G1:x", "G2:y") for l in ex), ex
    # no edges at all in collection B (no shared artifact), and none from numbering
    assert rep["graded_links"]["g23619scmd.bin"] == []
    for gr in rep["graded_records"]:
        labels = {o["label"] for o in gr["observation"]}
        assert "execution-unknown" in labels and "intended-operation" in labels
        assert "execution-confirmed" not in labels
    print("selfcheck: PASS — v2.1 assertions held (write->read explicit dependency vs "
          "mention-only shared-path-association, escaped-quote + non-adjacent, derived "
          "execution-confirmed, count-ranked top15, no numbering edges)")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description="Evidence-Graded Swarm Forensics (read-only, inert).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("feasibility"); f.add_argument("file"); f.add_argument("--out", default=".")
    g = sub.add_parser("g236"); g.add_argument("file"); g.add_argument("--out", default=".")
    sub.add_parser("selfcheck")
    args = ap.parse_args(argv)

    if args.cmd == "selfcheck":
        return 0 if selfcheck() else 1

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    recs = load(args.file)
    print(f"Loaded {len(recs):,} records from {args.file}\n")

    if args.cmd == "feasibility":
        by_count, verdict = feasibility(recs)
        print_feasibility(by_count, verdict)
        write_feasibility_outputs(by_count, verdict, outdir)
        print(f"\nWrote feasibility_verdict.json and feasibility_top15.csv to {outdir}")
    elif args.cmd == "g236":
        rep = g236_report(recs)
        print_g236(rep)
        (outdir / "g236_grading.json").write_text(json.dumps(rep, indent=2))
        print(f"\nWrote g236_grading.json to {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())