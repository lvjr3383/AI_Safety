"""
Cross-Model Divergence Analysis for Ambiguity Risk Estimation
Apart Research Secure Program Synthesis Hackathon 2026

Usage:
    python src/orchestrator.py                          # full run
    python src/orchestrator.py --test                   # A01, B04, C10 only
    python src/orchestrator.py --ids C09,C10            # specific IDs, new run
    python src/orchestrator.py --ids C09,C10 --run_id 20260513_032108  # merge into existing run
"""

import argparse
import json
import logging
import os
import random
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))

from comparator import compare_specifications
from extractor import extract_specification
from generator import generate_specifications
from loader import load_requirements
from reporter import compute_fod, generate_report

PROMPT_FILES = [
    "generator_system.txt",
    "generator_user.txt",
    "extractor_system.txt",
    "extractor_user.txt",
    "comparator_system.txt",
    "comparator_user.txt",
]

TEST_IDS = {"A01", "B04", "C10"}


def _setup_logging(log_file: Path, append: bool = False) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, mode=mode),
        ],
    )


def _load_prompts(prompts_dir: Path) -> dict:
    missing = [f for f in PROMPT_FILES if not (prompts_dir / f).exists()]
    if missing:
        raise FileNotFoundError(f"Missing prompt files: {missing}")
    prompts = {f: (prompts_dir / f).read_text().strip() for f in PROMPT_FILES}
    logging.getLogger(__name__).info(f"Loaded {len(prompts)} prompt files from {prompts_dir}")
    return prompts


def _save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2))


def _load_existing_results(
    run_root: Path,
    all_requirements: list,
) -> tuple:
    """Reconstruct in-memory results list from comparator/normalized files in an existing run."""
    reqs_by_id = {r["id"]: r for r in all_requirements}
    results = []

    excluded_path = run_root / "excluded.json"
    excluded = json.loads(excluded_path.read_text()) if excluded_path.exists() else []

    for comp_file in sorted((run_root / "comparator").glob("*_comparison.json")):
        req_id = comp_file.stem.replace("_comparison", "")
        req = reqs_by_id.get(req_id)
        if not req:
            continue

        comparison = json.loads(comp_file.read_text())

        normalized_specs = {}
        for model in ("claude", "gpt4o", "llama"):
            norm_file = run_root / "normalized" / f"{req_id}_{model}.json"
            normalized_specs[model] = (
                json.loads(norm_file.read_text()) if norm_file.exists() else None
            )

        results.append({
            "requirement_id": req_id,
            "requirement_text": req["requirement"],
            "tier": req["tier"],
            "expected_ambiguity": req["expected_ambiguity"],
            "fod": compute_fod(normalized_specs),
            "comparison": comparison,
            "normalized_specs": normalized_specs,
        })

    logging.getLogger(__name__).info(
        f"Loaded {len(results)} existing results from {run_root}"
    )
    return results, excluded


def _process_requirements(
    requirements: list,
    total: int,
    offset: int,
    prompts: dict,
    seed: int,
    run_root: Path,
) -> tuple:
    """Run generate→extract→compare for a list of requirements. Returns (results, excluded)."""
    logger = logging.getLogger(__name__)
    results = []
    excluded = []

    for i, req in enumerate(requirements):
        req_id = req["id"]
        logger.info(f"{'─' * 56}")
        logger.info(f"[{offset + i + 1}/{total}] {req_id}: {req['requirement'][:60]}")
        errors = {}

        # ── Step 1: Generate ──────────────────────────────────────
        logger.info(f"[{req_id}] step 1: generate")
        raw_specs = generate_specifications(
            requirement_text=req["requirement"],
            system_prompt=prompts["generator_system.txt"],
            user_prompt_template=prompts["generator_user.txt"],
        )
        for model, text in raw_specs.items():
            if text is not None:
                (run_root / "raw" / f"{req_id}_{model}.txt").write_text(text)
            else:
                errors[f"generator_{model}"] = "returned None"

        # ── Step 2: Extract ───────────────────────────────────────
        logger.info(f"[{req_id}] step 2: extract")
        normalized_specs = {}
        for model, raw_text in raw_specs.items():
            if raw_text is None:
                normalized_specs[model] = None
                errors[f"extractor_{model}"] = "skipped — generator None"
                continue
            norm = extract_specification(
                raw_text=raw_text,
                system_prompt=prompts["extractor_system.txt"],
                user_prompt_template=prompts["extractor_user.txt"],
                label=f"{req_id}/{model}",
            )
            normalized_specs[model] = norm
            if norm is not None:
                _save_json(run_root / "normalized" / f"{req_id}_{model}.json", norm)
            else:
                errors[f"extractor_{model}"] = "returned None"

        # ── Step 3: Compare ───────────────────────────────────────
        logger.info(f"[{req_id}] step 3: compare")
        comparison = compare_specifications(
            requirement_id=req_id,
            requirement_text=req["requirement"],
            gold_notes=req["gold_notes"],
            normalized_specs=normalized_specs,
            system_prompt=prompts["comparator_system.txt"],
            user_prompt_template=prompts["comparator_user.txt"],
            seed=seed,
            label_maps_dir=run_root / "label_maps",
        )
        if comparison is not None:
            _save_json(run_root / "comparator" / f"{req_id}_comparison.json", comparison)
        else:
            errors["comparator"] = "returned None"

        if errors:
            _save_json(run_root / "errors" / f"{req_id}_errors.json", errors)
            logger.warning(f"[{req_id}] errors recorded: {list(errors.keys())}")

        if comparison is None:
            logger.warning(f"[{req_id}] excluded — comparator returned None")
            excluded.append(req_id)
            continue

        fod = compute_fod(normalized_specs)
        logger.info(
            f"[{req_id}] done — dc={comparison.get('dc')}  "
            f"fc={comparison.get('fc_count')}  fod={fod}"
        )
        results.append({
            "requirement_id": req_id,
            "requirement_text": req["requirement"],
            "tier": req["tier"],
            "expected_ambiguity": req["expected_ambiguity"],
            "fod": fod,
            "comparison": comparison,
            "normalized_specs": normalized_specs,
        })

    return results, excluded


def run_pipeline(
    requirements_path: str = "data/requirements_dataset.json",
    prompts_dir: str = "prompts",
    runs_dir: str = "runs",
    results_dir: str = "results",
    test_mode: bool = False,
    ids: set = None,
    run_id: str = None,
) -> None:
    load_dotenv()

    merge_mode = run_id is not None
    all_requirements = load_requirements(requirements_path)

    if merge_mode:
        run_root = Path(runs_dir) / run_id
        if not run_root.exists():
            raise FileNotFoundError(f"Run folder not found: {run_root}")
        seed = int((run_root / "seed.txt").read_text().strip())
        _setup_logging(run_root / "pipeline.log", append=True)
        logger = logging.getLogger(__name__)
        logger.info(f"=== MERGE into run {run_id}  ids={sorted(ids)} ===")
        logger.info(f"Seed (reused): {seed}")

        existing_results, existing_excluded = _load_existing_results(run_root, all_requirements)
        existing_ids = {r["requirement_id"] for r in existing_results}
    else:
        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        run_root = Path(runs_dir) / run_id
        _setup_logging(run_root / "pipeline.log", append=False)
        logger = logging.getLogger(__name__)
        seed = random.randint(0, 2**31 - 1)
        run_root.mkdir(parents=True, exist_ok=True)
        (run_root / "seed.txt").write_text(str(seed))
        logger.info(f"=== Run {run_id}  test_mode={test_mode} ===")
        logger.info(f"Seed: {seed} → {run_root / 'seed.txt'}")
        for sub in ("raw", "normalized", "label_maps", "comparator", "errors"):
            (run_root / sub).mkdir(parents=True, exist_ok=True)
        existing_results, existing_excluded = [], []
        existing_ids = set()

    prompts = _load_prompts(Path(prompts_dir))

    # Determine which requirements to process
    requirements = all_requirements
    if test_mode:
        requirements = [r for r in requirements if r["id"] in TEST_IDS]
    if ids:
        requirements = [r for r in requirements if r["id"] in ids]
    logger.info(f"Processing {len(requirements)} requirement(s): {[r['id'] for r in requirements]}")

    new_results, new_excluded = _process_requirements(
        requirements=requirements,
        total=len(existing_ids) + len(requirements),
        offset=len(existing_ids),
        prompts=prompts,
        seed=seed,
        run_root=run_root,
    )

    # Merge: existing + new, dropping newly-recovered IDs from excluded list
    newly_recovered = {r["requirement_id"] for r in new_results}
    merged_results = existing_results + new_results
    merged_excluded = [eid for eid in existing_excluded if eid not in newly_recovered] + new_excluded

    # Sort merged results by dataset order
    order = {r["id"]: i for i, r in enumerate(all_requirements)}
    merged_results.sort(key=lambda r: order.get(r["requirement_id"], 999))

    _save_json(run_root / "excluded.json", merged_excluded)
    if merged_excluded:
        logger.warning(f"Excluded requirements: {merged_excluded}")

    logger.info("Generating report...")
    generate_report(
        results=merged_results,
        results_dir=Path(results_dir),
        run_id=run_id,
        excluded=merged_excluded,
        seed=seed,
    )
    logger.info("Pipeline complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cross-Model Divergence Analysis Pipeline")
    parser.add_argument("--requirements", default="data/requirements_dataset.json")
    parser.add_argument("--prompts", default="prompts")
    parser.add_argument("--runs", default="runs")
    parser.add_argument("--results", default="results")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run only A01, B04, C10",
    )
    parser.add_argument(
        "--ids",
        default=None,
        help="Comma-separated requirement IDs to run (e.g. C09,C10)",
    )
    parser.add_argument(
        "--run_id",
        default=None,
        help="Existing run ID to merge results into (reads seed from that run)",
    )
    args = parser.parse_args()

    ids = set(args.ids.split(",")) if args.ids else None

    run_pipeline(
        requirements_path=args.requirements,
        prompts_dir=args.prompts,
        runs_dir=args.runs,
        results_dir=args.results,
        test_mode=args.test,
        ids=ids,
        run_id=args.run_id,
    )
