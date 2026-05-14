import hashlib
import json
import logging
import os
import random
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import anthropic

logger = logging.getLogger(__name__)

CLAUDE_MODEL = "claude-sonnet-4-6"
TEMPERATURE = 0
MAX_TOKENS = 1500

# FC behaviors sourced only from these three gold_notes fields
FC_SOURCE_FIELDS = ["security_constraints", "failure_modes", "assumptions"]

# Fixed model pool — label assignment shuffles this list
_MODELS = ["claude", "gpt4o", "llama"]


def _parse_json(text: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None


def _build_fc_behaviors(gold_notes: Dict[str, Any]) -> str:
    behaviors: List[str] = []
    for field in FC_SOURCE_FIELDS:
        behaviors.extend(gold_notes.get(field, []))
    if not behaviors:
        return "(none provided)"
    return "\n".join(f"- {b}" for b in behaviors)


def _assign_labels(requirement_id: str, seed: int) -> Dict[str, str]:
    key = hashlib.sha256(f"{seed}:{requirement_id}".encode()).hexdigest()
    rng = random.Random(key)
    pool = _MODELS[:]
    rng.shuffle(pool)
    return {"A": pool[0], "B": pool[1], "C": pool[2]}


def compare_specifications(
    requirement_id: str,
    requirement_text: str,
    gold_notes: Dict[str, Any],
    normalized_specs: Dict[str, Optional[Dict[str, Any]]],
    system_prompt: str,
    user_prompt_template: str,
    seed: int,
    label_maps_dir: Path,
) -> Optional[Dict[str, Any]]:
    label_map = _assign_labels(requirement_id, seed)

    # Write label map to disk BEFORE calling comparator — never passes model names to the model
    label_map_path = label_maps_dir / f"{requirement_id}_label_map.json"
    label_map_path.write_text(json.dumps(label_map, indent=2))
    logger.info(f"[comparator/{requirement_id}] label_map written: {label_map}")

    # Build per-label specs — None normalized becomes empty dict (treated as all-empty)
    spec = {
        label: normalized_specs.get(model) or {}
        for label, model in label_map.items()
    }

    user_prompt = user_prompt_template.format(
        requirement_id=requirement_id,
        requirement_text=requirement_text,
        fc_behaviors=_build_fc_behaviors(gold_notes),
        normalized_json_model_a=json.dumps(spec["A"], indent=2),
        normalized_json_model_b=json.dumps(spec["B"], indent=2),
        normalized_json_model_c=json.dumps(spec["C"], indent=2),
    )

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    try:
        logger.info(f"[comparator/{requirement_id}] calling Claude ({CLAUDE_MODEL})...")
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = response.content[0].text
        logger.info(f"[comparator/{requirement_id}] received {len(text)} chars")
    except Exception as exc:
        logger.error(f"[comparator/{requirement_id}] API call failed: {exc}")
        return None

    result = _parse_json(text)
    if result is None:
        logger.error(f"[comparator/{requirement_id}] could not parse JSON: {text[:300]}")
        return None

    # Recompute counts from field_results — the LLM's self-reported totals are unreliable
    field_results = result.get("field_results", {})
    recomputed_dc = sum(1 for v in field_results.values() if v.get("divergence"))
    recomputed_fc = sum(1 for v in field_results.values() if v.get("fc_flag"))
    recomputed_cats: Dict[str, int] = {}
    for v in field_results.values():
        cat = v.get("category")
        if cat:
            recomputed_cats[cat] = recomputed_cats.get(cat, 0) + 1

    if result.get("dc") != recomputed_dc:
        logger.warning(
            f"[comparator/{requirement_id}] dc mismatch: LLM={result.get('dc')} recomputed={recomputed_dc} — using recomputed"
        )
    if result.get("fc_count") != recomputed_fc:
        logger.warning(
            f"[comparator/{requirement_id}] fc_count mismatch: LLM={result.get('fc_count')} recomputed={recomputed_fc} — using recomputed"
        )

    result["dc"] = recomputed_dc
    result["fc_count"] = recomputed_fc
    result["category_counts"] = recomputed_cats
    result["label_map"] = label_map
    return result
