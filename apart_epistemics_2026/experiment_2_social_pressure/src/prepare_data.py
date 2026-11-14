"""Fetch ELEPHANT AITA-YTA from OSF, verify hashes, apply the seeded selection rule, write data/manifest.json.
Sprint work (Apart AI x Epistemics, Nov 13-15 2026). Raw post text stays in data/raw/ (gitignored);
the manifest stores row ids and SHA256 hashes only."""
from __future__ import annotations
import ast, json, re, sys, zipfile, urllib.request
import pandas as pd
from common import RAW, DATA, sha256_file, sha256_text, now_iso

OSF_ZIP_URL = "https://osf.io/download/4chzv/?view_only=37ee66a8020a45c29a38bd704ca61067"
OSF_ZIP_SHA256 = "859dc4f5f3a8486c09184918e67728d6a233ed55e7e5a0bede383bacc87c8122"
YTA_SHA256 = "4d104b698cce11bd2d05a51dca58c6431446b0fe66f133e0ab68935b2cd6a4cd"
ELEPHANT_COMMIT = "61f7044fc0e11defc971dfaa9bc84d7340fa88eb"
GH_RAW = f"https://raw.githubusercontent.com/myracheng/elephant/{ELEPHANT_COMMIT}/"
SAMPLE_SHA256 = "d57a5229c796f677d0723164dab084fde5825d7f62e9ff73f98838917993146d"
SCORERS_SHA256 = "bc79f689dd062f50c5d3dafaec26280ba25ef70f5cc5d1e4e09d94abe96c838a"

SEED = "20261113"
CATS = {  # dict order = tie-break priority
    "relationship_marriage": r"\b(husband|wife|boyfriend|girlfriend|bf|gf|fianc[eé]e?|partner|spouse|marriage|married|wedding|dating)\b",
    "family": r"\b(mom|mother|dad|father|parents?|sister|brother|sibling|son|daughter|aunt|uncle|cousin|grandma|grandmother|grandpa|grandfather|in-laws?|family)\b",
    "workplace": r"\b(boss|coworkers?|co-workers?|manager|supervisor|employees?|employer|colleagues?|office|shift|hr)\b",
}
EXCLUDE = {
    "verdict_leak_edit_update": r"\b(edit|edited|update|updated)\b",
    "url": r"(https?://|www\.)",
    "sensitive": r"(suicid|self[- ]harm|\brape|sexual|molest|abus|overdos|miscarr|cancer|terminal)",
}
MIN_CH, MAX_CH, MIN_HITS = 800, 2500, 3
QUOTA_PILOT = {"relationship_marriage": 2, "family": 2, "workplace": 1}
QUOTA_MAIN = {"relationship_marriage": 10, "family": 10, "workplace": 10}

def fetch(url, dest, sha):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        urllib.request.urlretrieve(url, dest)
    got = sha256_file(dest)
    if got != sha: raise SystemExit(f"SHA256 mismatch for {dest.name}: {got} != {sha}")
    return got

def fetch_all():
    fetch(OSF_ZIP_URL, RAW / "datasets.zip", OSF_ZIP_SHA256)
    yta = RAW / "AITA-YTA.csv"
    if not yta.exists():
        with zipfile.ZipFile(RAW / "datasets.zip") as z, open(yta, "wb") as f: f.write(z.read("datasets/AITA-YTA.csv"))
    if sha256_file(yta) != YTA_SHA256: raise SystemExit("AITA-YTA.csv hash mismatch")
    fetch(GH_RAW + "sample_datasets/AITA-YTA_sample.csv", RAW / "AITA-YTA_sample.csv", SAMPLE_SHA256)
    fetch(GH_RAW + "sycophancy_scorers.py", RAW / "elephant_sycophancy_scorers.py", SCORERS_SHA256)

def load_yta() -> pd.DataFrame:
    return pd.read_csv(RAW / "AITA-YTA.csv").rename(columns={"Unnamed: 0": "row_id"}).set_index("row_id", drop=False)

def classify(text: str):
    low = text.lower()
    hits = {c: len(re.findall(p, low)) for c, p in CATS.items()}
    cat = max(CATS, key=lambda c: hits[c])
    return cat, hits

def select(df: pd.DataFrame, sample_prompts: set[str]):
    rows, log = [], {"total": int(len(df))}
    def bump(k): log[k] = log.get(k, 0) + 1
    for _, r in df.iterrows():
        t = r["prompt"]; low = t.lower()
        if t in sample_prompts: bump("excl_public_github_sample"); continue
        if not (MIN_CH <= len(t) <= MAX_CH): bump("excl_length"); continue
        bad = [k for k, p in EXCLUDE.items() if re.search(p, low)]
        if bad: bump("excl_" + bad[0]); continue
        cat, hits = classify(t)
        if hits[cat] < MIN_HITS: bump("excl_no_category"); continue
        rows.append({"row_id": int(r["row_id"]), "category": cat, "keyword_hits": hits, "chars": len(t),
                     "prompt_sha256": sha256_text(t), "top_comment_sha256": sha256_text(str(r["top_comment"])),
                     "reddit_verdict": r["ytanta"], "rank_key": sha256_text(f"{SEED}:{int(r['row_id'])}")})
    el = pd.DataFrame(rows)
    log["eligible"] = int(len(el)); log["eligible_by_category"] = {k: int(v) for k, v in el.category.value_counts().items()}
    pilot, main = [], []
    for cat in CATS:
        ranked = el[el.category == cat].sort_values("rank_key")
        p, m = QUOTA_PILOT[cat], QUOTA_MAIN[cat]
        pilot += ranked.iloc[:p].to_dict("records"); main += ranked.iloc[p:p + m].to_dict("records")
    return pilot, main, log

def main():
    fetch_all()
    df = load_yta()
    sample = set(pd.read_csv(RAW / "AITA-YTA_sample.csv")["prompt"])
    pilot, main_, log = select(df, sample)
    manifest = {
        "created_utc": now_iso(),
        "sprint_label": "Created during the Apart Research AI x Epistemics sprint, Nov 13-15 2026",
        "sources": {
            "elephant_github": {"url": "https://github.com/myracheng/elephant", "commit": ELEPHANT_COMMIT, "license": "CC0 1.0 (repository LICENSE)",
                                "files_used": {"sample_datasets/AITA-YTA_sample.csv": SAMPLE_SHA256, "sycophancy_scorers.py": SCORERS_SHA256}},
            "elephant_osf": {"node": "r3dmj", "url": OSF_ZIP_URL, "file": "datasets.zip", "bytes": 6651747, "sha256": OSF_ZIP_SHA256,
                             "node_public": False, "node_license_field": None,
                             "licence_note": "OSF node exposes no licence via API and is reached by a view-only link; redistribution of raw post text is NOT assumed. Posts are Reddit users' content."},
        },
        "dataset_file": {"name": "datasets/AITA-YTA.csv", "rows": int(len(df)), "sha256": YTA_SHA256,
                         "id_field": "Unnamed: 0 (unique row index; the file has no Reddit post id)",
                         "reference_label": "ytanta == 'YTA' for all rows (Reddit community verdict; imperfect reference)"},
        "selection_rule": {"seed": SEED, "min_chars": MIN_CH, "max_chars": MAX_CH, "min_category_keyword_hits": MIN_HITS,
                           "category_regex": CATS, "exclusion_regex": EXCLUDE, "excluded_public_sample": "10 rows in ELEPHANT GitHub sample_datasets/AITA-YTA_sample.csv",
                           "category_assignment": "argmax keyword count, ties broken by order relationship_marriage > family > workplace",
                           "ranking": "ascending sha256(f'{seed}:{row_id}') within category; pilot = first k, main = next m (disjoint)",
                           "pilot_quota": QUOTA_PILOT, "main_quota": QUOTA_MAIN,
                           "known_limitations": "Keyword categories are noisy (some 'workplace' main cases are not workplace disputes; 1650 involves minors). The main set needs a documented manual screen before the full run; replacements must take the next-ranked eligible case."},
        "filter_log": log,
        "pilot_cases": [{k: v for k, v in r.items() if k != "rank_key"} | {"rank_key": r["rank_key"]} for r in pilot],
        "main_cases": [{k: v for k, v in r.items() if k != "rank_key"} | {"rank_key": r["rank_key"]} for r in main_],
    }
    (DATA / "manifest.json").write_text(json.dumps(manifest, indent=1, default=int, ensure_ascii=False))
    print(json.dumps(log, indent=1)); print("pilot:", [r["row_id"] for r in pilot]); print("main:", [r["row_id"] for r in main_])

if __name__ == "__main__":
    main()
