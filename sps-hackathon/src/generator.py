import logging
import os
import time
from typing import Dict, Optional

import anthropic
from groq import Groq
from openai import OpenAI

logger = logging.getLogger(__name__)

CLAUDE_MODEL = "claude-sonnet-4-6"
GPT4O_MODEL = "gpt-4o"
LLAMA_MODEL = "llama-3.3-70b-versatile"
TEMPERATURE = 0
MAX_TOKENS = 1000
RETRY_DELAY = 5


def _call_claude(client: anthropic.Anthropic, system: str, user: str) -> str:
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text


def _call_gpt4o(client: OpenAI, system: str, user: str) -> str:
    response = client.chat.completions.create(
        model=GPT4O_MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content


def _call_llama(client: Groq, system: str, user: str) -> str:
    response = client.chat.completions.create(
        model=LLAMA_MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content


def _call_with_retry(fn, name: str, *args) -> Optional[str]:
    for attempt in (1, 2):
        try:
            logger.info(f"[generator/{name}] attempt {attempt}")
            result = fn(*args)
            logger.info(f"[generator/{name}] success — {len(result)} chars")
            return result
        except Exception as exc:
            logger.warning(f"[generator/{name}] attempt {attempt} failed: {exc}")
            if attempt == 1:
                logger.info(f"[generator/{name}] retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
    logger.error(f"[generator/{name}] both attempts failed — returning None")
    return None


def generate_specifications(
    requirement_text: str,
    system_prompt: str,
    user_prompt_template: str,
) -> Dict[str, Optional[str]]:
    user_prompt = user_prompt_template.format(requirement_text=requirement_text)

    claude_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

    results: Dict[str, Optional[str]] = {}
    results["claude"] = _call_with_retry(_call_claude, "claude", claude_client, system_prompt, user_prompt)
    results["gpt4o"] = _call_with_retry(_call_gpt4o, "gpt4o", openai_client, system_prompt, user_prompt)
    results["llama"] = _call_with_retry(_call_llama, "llama", groq_client, system_prompt, user_prompt)

    succeeded = sum(v is not None for v in results.values())
    logger.info(f"[generator] {succeeded}/3 models succeeded")
    return results
