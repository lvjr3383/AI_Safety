import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

SCHEMA_FIELDS = [
    "core_behavior",
    "inputs",
    "outputs",
    "assumptions",
    "failure_modes",
    "edge_cases",
    "security_constraints",
    "performance_constraints",
]

TIERS = ["clear", "moderately_underspecified", "adversarially_ambiguous"]


def compute_fod(normalized_specs: Dict[str, Optional[Dict[str, Any]]]) -> float:
    """Fields with at least one empty model output / 8."""
    models = [v if v is not None else {} for v in normalized_specs.values()]
    if not models:
        return 1.0
    empty_count = sum(
        1 for field in SCHEMA_FIELDS
        if any(not m.get(field) for m in models)
    )
    return round(empty_count / len(SCHEMA_FIELDS), 4)


def _tier_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_tier: Dict[str, List] = defaultdict(list)
    for r in results:
        by_tier[r["tier"]].append(r)

    out = {}
    for tier in TIERS:
        items = by_tier.get(tier, [])
        if not items:
            continue

        with_comparison = [r for r in items if r["comparison"] is not None]
        dc_values = [r["comparison"]["dc"] for r in with_comparison]
        fc_values = [r["comparison"].get("fc_count", 0) for r in with_comparison]

        # TDR — average DC per tier
        tdr = round(sum(dc_values) / len(dc_values), 4) if dc_values else 0.0

        # CD — sum of category_counts across all requirements in tier
        cd: Dict[str, int] = defaultdict(int)
        for r in with_comparison:
            for cat, cnt in r["comparison"].get("category_counts", {}).items():
                cd[cat] += cnt

        # FCR — fraction of requirements with fc_count > 0
        fcr = round(sum(1 for v in fc_values if v > 0) / len(items), 4)

        out[tier] = {
            "count": len(items),
            "with_comparison": len(with_comparison),
            "tdr": tdr,
            "cd": dict(cd),
            "fcr": fcr,
        }
    return out


def _markdown(
    results: List[Dict[str, Any]],
    tier_metrics: Dict[str, Any],
    run_id: str,
    excluded: List[str],
    seed: int,
) -> str:
    lines: List[str] = []
    lines.append("# Cross-Model Divergence Analysis Report")
    lines.append(f"\nRun ID: `{run_id}`  \nSeed: `{seed}`\n")

    lines.append("## Run Summary\n")
    lines.append(f"- Total processed: {len(results)}")
    lines.append(f"- Excluded (component failure): {len(excluded)}")
    if excluded:
        lines.append(f"- Excluded IDs: {', '.join(excluded)}")

    lines.append("\n## Per-Tier Metrics\n")
    for tier, m in tier_metrics.items():
        lines.append(f"### {tier} (n={m['count']})\n")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| TDR (mean DC) | {m['tdr']} |")
        lines.append(f"| FCR | {m['fcr']} |")
        cd_str = "  ".join(f"{k}:{v}" for k, v in sorted(m["cd"].items()) if v > 0) or "—"
        lines.append(f"| CD (category totals) | {cd_str} |")
        lines.append("")

    lines.append("## Per-Requirement Results\n")
    lines.append("| ID | Tier | Expected | DC | FC | FOD | Categories |")
    lines.append("|----|------|----------|----|----|-----|------------|")
    for r in results:
        c = r["comparison"]
        if c:
            cats = "  ".join(f"{k}:{v}" for k, v in c.get("category_counts", {}).items() if v > 0) or "—"
            lines.append(
                f"| {r['requirement_id']} | {r['tier']} | {r['expected_ambiguity']}"
                f" | {c['dc']} | {c.get('fc_count', 0)} | {r['fod']} | {cats} |"
            )
        else:
            lines.append(
                f"| {r['requirement_id']} | {r['tier']} | {r['expected_ambiguity']}"
                f" | — | — | {r['fod']} | (excluded) |"
            )

    lines.append("\n## Field-Level Divergence Detail\n")
    for r in results:
        if not r["comparison"]:
            continue
        req_preview = r["requirement_text"][:70]
        lines.append(f"### {r['requirement_id']} — {req_preview}\n")
        lines.append("| Field | Diverge | Category | FC | Note |")
        lines.append("|-------|---------|----------|----|------|")
        for field, fr in r["comparison"].get("field_results", {}).items():
            div = "yes" if fr.get("divergence") else "no"
            cat = fr.get("category") or "—"
            fc = "yes" if fr.get("fc_flag") else "no"
            note = (fr.get("note") or "")[:65]
            lines.append(f"| {field} | {div} | {cat} | {fc} | {note} |")
        lines.append("")

    return "\n".join(lines)


def generate_report(
    results: List[Dict[str, Any]],
    results_dir: Path,
    run_id: str,
    excluded: List[str],
    seed: int,
) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    tier_metrics = _tier_metrics(results)

    output = {
        "run_id": run_id,
        "seed": seed,
        "total_processed": len(results),
        "excluded": excluded,
        "tier_metrics": tier_metrics,
        "requirements": [
            {
                "requirement_id": r["requirement_id"],
                "requirement_text": r["requirement_text"],
                "tier": r["tier"],
                "expected_ambiguity": r["expected_ambiguity"],
                "fod": r["fod"],
                "dc": r["comparison"]["dc"] if r["comparison"] else None,
                "fc_count": r["comparison"].get("fc_count") if r["comparison"] else None,
                "category_counts": r["comparison"].get("category_counts") if r["comparison"] else None,
                "summary": r["comparison"].get("summary", "") if r["comparison"] else None,
            }
            for r in results
        ],
    }

    json_path = results_dir / f"{run_id}_results.json"
    json_path.write_text(json.dumps(output, indent=2))
    logger.info(f"Results JSON → {json_path}")

    md_path = results_dir / f"{run_id}_report.md"
    md_path.write_text(_markdown(results, tier_metrics, run_id, excluded, seed))
    logger.info(f"Markdown report → {md_path}")

    print(f"\nResults: {json_path}")
    print(f"Report:  {md_path}")
