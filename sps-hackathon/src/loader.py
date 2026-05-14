import json
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {"id", "tier", "requirement", "gold_notes"}


def load_requirements(path: str) -> List[Dict[str, Any]]:
    data_path = Path(path)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    with open(data_path) as f:
        data = json.load(f)

    items: List[Dict[str, Any]] = data if isinstance(data, list) else data["requirements"]

    valid = []
    for item in items:
        missing = REQUIRED_FIELDS - set(item.keys())
        if missing:
            logger.warning(f"Entry {item.get('id', '?')} missing fields {missing} — skipping")
            continue
        valid.append(item)

    logger.info(f"Loaded {len(valid)}/{len(items)} valid requirements from {path}")
    return valid
