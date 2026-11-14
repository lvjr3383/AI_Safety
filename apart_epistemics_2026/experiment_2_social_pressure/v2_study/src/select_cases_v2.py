"""Deterministic, fully automated selection of 30 NEW ELEPHANT AITA-YTA cases for Experiment 2 v2.
Apart AI x Epistemics sprint, Nov 13-15 2026 (written Nov 14). No manual screening.

Rules are applied in the order below; each excluded row is counted under the FIRST rule it fails.
Eligible rows are assigned a category by keyword counts and ranked by sha256(f"{SEED}:{row_id}");
the first 10 per category are selected. Output v2_study/config/manifest_v2.json stores row ids and
SHA-256 hashes only (never post text; ELEPHANT OSF licence unverified).
Usage: python v2_study/src/select_cases_v2.py"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

V2 = Path(__file__).resolve().parents[1]; EXP = V2.parent
sys.path.insert(0, str(EXP / "src"))

SEED = "exp2-v2-20261114"
YTA_SHA256 = "4d104b698cce11bd2d05a51dca58c6431446b0fe66f133e0ab68935b2cd6a4cd"   # same file as the pilot
MIN_CH, MAX_CH, MIN_HITS, PER_CATEGORY = 800, 2500, 3, 10
CATS = {  # same category regexes as the pilot (src/prepare_data.py); dict order = tie-break priority
    "relationship_marriage": r"\b(husband|wife|boyfriend|girlfriend|bf|gf|fianc[eé]e?|partner|spouse|marriage|married|wedding|dating)\b",
    "family": r"\b(mom|mother|dad|father|parents?|sister|brother|sibling|son|daughter|aunt|uncle|cousin|grandma|grandmother|grandpa|grandfather|in-laws?|family)\b",
    "workplace": r"\b(boss|coworkers?|co-workers?|manager|supervisor|employees?|employer|colleagues?|office|shift|hr)\b",
}
RULES = [  # (name, description) in application order
    ("pilot_case", "one of the 5 pilot cases (data/manifest.json pilot_cases)"),
    ("public_github_sample", "appears in ELEPHANT's public GitHub sample (10 rows)"),
    ("incomplete", "contains [deleted]/[removed], is shorter than 800 characters, or does not end in sentence-final punctuation"),
    ("excessively_long", "longer than 2500 characters"),
    ("verdict_leak_edit_update", "contains edit/update (often reveals the Reddit outcome)"),
    ("url", "contains a URL"),
    ("sensitive", "matches the sensitive-content regex (self-harm, sexual content, abuse, violence, death, serious illness, pregnancy loss, drugs, police)"),
    ("minor_involved", "states an age under 18 or uses teen/minor/toddler/infant/baby"),
    ("no_clear_category", "fewer than 3 keyword hits for its best category"),
]
INCOMPLETE_RE = r"\[(deleted|removed)\]"
END_RE = r"[.!?\"'\)\u201d\u2019]\s*$"
SENSITIVE_RE = (r"(suicid|self[- ]harm|kill (my|him|her|them)self|\brape|sexual|\bsex\b|molest|abus|assault|violen|\bhit (me|him|her)\b|punch|"
                r"\bgun\b|knife|weapon|overdos|\bdrugs?\b|cocaine|heroin|died|\bdeath\b|\bdead\b|funeral|passed away|cancer|terminal|"
                r"miscarr|abortion|police|arrest)")
MINOR_RE = r"(\b(1[0-7]|[1-9])\s*(yo|y/o|yrs?|years?[- ]old|[mf])\b|\(\s*(1[0-7]|[1-9])\s*[mf]?\s*\)|\b(teen|teens|teenager|teenage|minor|minors|toddler|infant|baby|babies)\b)"

def sha(s: str) -> str: return hashlib.sha256(s.encode("utf-8")).hexdigest()

def classify(text: str):
    low = text.lower(); hits = {c: len(re.findall(p, low)) for c, p in CATS.items()}
    return max(CATS, key=lambda c: hits[c]), hits

def first_failed_rule(text: str, row_id: int, pilot_ids: set, sample: set):
    low = text.lower()
    if row_id in pilot_ids: return "pilot_case"
    if text in sample: return "public_github_sample"
    if re.search(INCOMPLETE_RE, low) or len(text) < MIN_CH or not re.search(END_RE, text): return "incomplete"
    if len(text) > MAX_CH: return "excessively_long"
    if re.search(r"\b(edit|edited|update|updated)\b", low): return "verdict_leak_edit_update"
    if re.search(r"(https?://|www\.)", low): return "url"
    if re.search(SENSITIVE_RE, low): return "sensitive"
    if re.search(MINOR_RE, low): return "minor_involved"
    cat, hits = classify(text)
    if hits[cat] < MIN_HITS: return "no_clear_category"
    return None

def select(rows, pilot_ids, sample):
    """rows: iterable of (row_id, prompt, reddit_verdict). Returns (selected, counts)."""
    counts = {name: 0 for name, _ in RULES}; eligible = []
    for rid, text, verdict in rows:
        rule = first_failed_rule(text, int(rid), pilot_ids, sample)
        if rule: counts[rule] += 1; continue
        cat, hits = classify(text)
        eligible.append({"row_id": int(rid), "category": cat, "keyword_hits": hits, "chars": len(text), "prompt_sha256": sha(text),
                         "reddit_verdict": verdict, "rank_key": sha(f"{SEED}:{int(rid)}")})
    counts["eligible"] = len(eligible)
    counts["eligible_by_category"] = {c: sum(e["category"] == c for e in eligible) for c in CATS}
    sel = []
    for c in CATS:
        sel += sorted([e for e in eligible if e["category"] == c], key=lambda e: e["rank_key"])[:PER_CATEGORY]
    return sel, counts

def main():
    import pandas as pd
    from common import sha256_file
    raw = EXP / "data/raw"
    if sha256_file(raw / "AITA-YTA.csv") != YTA_SHA256: raise SystemExit("AITA-YTA.csv hash mismatch (run src/prepare_data.py)")
    df = pd.read_csv(raw / "AITA-YTA.csv").rename(columns={"Unnamed: 0": "row_id"})
    sample = set(pd.read_csv(raw / "AITA-YTA_sample.csv")["prompt"])
    pilot_ids = {c["row_id"] for c in json.loads((EXP / "data/manifest.json").read_text())["pilot_cases"]}
    sel, counts = select(zip(df.row_id, df.prompt, df.ytanta), pilot_ids, sample)
    assert len(sel) == 3 * PER_CATEGORY, len(sel)
    man = {"study": "Experiment 2 v2 (Apart AI x Epistemics sprint, Nov 13-15 2026)", "dataset": {"file": "datasets/AITA-YTA.csv (ELEPHANT, OSF)",
           "rows": int(len(df)), "sha256": YTA_SHA256, "reference_label": "ytanta == 'YTA' for every row"},
           "selection": {"seed": SEED, "rules_in_order": [{"name": n, "description": d} for n, d in RULES], "category_regex": CATS,
                         "sensitive_regex": SENSITIVE_RE, "minor_regex": MINOR_RE, "incomplete_regex": INCOMPLETE_RE, "end_regex": END_RE,
                         "min_chars": MIN_CH, "max_chars": MAX_CH, "min_keyword_hits": MIN_HITS, "per_category": PER_CATEGORY,
                         "ranking": "ascending sha256(f'{seed}:{row_id}') within category",
                         "limitations": "Keyword filters are deterministic and imperfect: they can miss sensitive content or exclude benign posts. No manual screening was done, by design."},
           "excluded_counts_first_failed_rule": counts, "cases": sel}
    (V2 / "config/manifest_v2.json").write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps(counts, indent=1)); print([(c["row_id"], c["category"], c["chars"]) for c in sel])

if __name__ == "__main__":
    main()
