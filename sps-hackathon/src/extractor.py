import json
import logging
import os
import re
from typing import Any, Dict, Optional

import anthropic

logger = logging.getLogger(__name__)

CLAUDE_MODEL = "claude-sonnet-4-6"
TEMPERATURE = 0
MAX_TOKENS = 2000

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


def _repair(data: Dict[str, Any], label: str) -> Dict[str, Any]:
    added = [f for f in SCHEMA_FIELDS if f not in data]
    for field in added:
        data[field] = []
    if added:
        logger.warning(f"[extractor/{label}] repaired missing fields: {added}")
    return data


def extract_specification(
    raw_text: str,
    system_prompt: str,
    user_prompt_template: str,
    label: str = "",
) -> Optional[Dict[str, Any]]:
    user_prompt = user_prompt_template.format(raw_generator_output=raw_text)

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    try:
        logger.info(f"[extractor/{label}] calling Claude ({CLAUDE_MODEL})...")
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = response.content[0].text
        logger.info(f"[extractor/{label}] received {len(text)} chars")
    except Exception as exc:
        logger.error(f"[extractor/{label}] API call failed: {exc}")
        return None

    data = _parse_json(text)
    if data is None:
        logger.error(f"[extractor/{label}] could not parse JSON from response: {text[:300]}")
        return None

    if not isinstance(data, dict):
        logger.error(f"[extractor/{label}] parsed value is {type(data).__name__}, expected dict")
        return None

    return _repair(data, label)
