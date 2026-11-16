"""Shared helpers for Experiment 2 v2 (Apart AI x Epistemics sprint, Nov 13-15 2026)."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path

V2 = Path(__file__).resolve().parents[1]; EXP = V2.parent
CONFIG = V2 / "config"
def load(p): return json.loads(Path(p).read_text())
def sha(s: str) -> str: return hashlib.sha256(s.encode("utf-8")).hexdigest()

PROMPTS = load(CONFIG / "prompts_v2.json")
STUDY = load(CONFIG / "study.json")
FAULT = {"not_in_wrong": 0, "mixed": 1, "in_wrong": 2}

def system_prompt(condition: str, prompts=PROMPTS) -> str:
    c = prompts["conditions"][condition]
    return prompts["system_template"].format(system_base=prompts["system_base"], framing=prompts["framing"][c["framing"]],
                                             intervention=prompts["intervention"][c["intervention"]])

def user_turn1(post: str, prompts=PROMPTS) -> str: return prompts["user_turn1_template"].format(post=post)
def redacted_turn1(row_id: int, post: str, prompts=PROMPTS) -> str:
    return prompts["user_turn1_template"].format(post=f"[ELEPHANT AITA-YTA post omitted: row_id={row_id}, sha256={sha(post)}]")
def rebuttal(turn: int, prompts=PROMPTS) -> str:
    """Fixed rebuttal: identical for every case, model and condition; independent of the model's first verdict."""
    return prompts["rebuttal_1" if turn == 2 else "rebuttal_2"]

def conv_id(seed, row_id, cond, model, rep, stage="main") -> str:
    return sha(f"{seed}:v2:{stage}:{row_id}:{cond}:{model}:{rep}")[:12]
def conv_seed(cid: str) -> int:
    """int32-safe (Google AI Studio rejects seeds outside int32)."""
    return int(cid[:8], 16) & 0x7FFFFFFF

_VERDICT_RE = re.compile(r"verdict\s*[:\-]\s*\**\s*\[?\s*(.+)", re.I)
_NUM = r"\s*[:\-]\s*\**\s*\[?\s*(\d{1,2})(?:\s*/\s*10)?"
_CONF_RE = re.compile(r"confidence" + _NUM, re.I)
_BLAME_RE = re.compile(r"blame" + _NUM, re.I)

def parse_verdict(text):
    """Same rules as the frozen pilot parser (src/common.py), copied so the v2 protocol is self-contained."""
    if not text: return "unparsed"
    m = list(_VERDICT_RE.finditer(text))
    if not m: return "unparsed"
    v = re.sub(r"[\*\]\[_`]", "", m[-1].group(1).lower()).strip()
    if v.count("/") >= 1 and "mixed" in v and "in the wrong" in v: return "unparsed"
    if re.search(r"\bnot in the wrong\b|n['\u2019]?t in the wrong\b|\bnta\b", v): return "not_in_wrong"
    if re.search(r"\bin the wrong\b|\byta\b", v): return "in_wrong"
    if re.search(r"\bmixed\b|\besh\b", v): return "mixed"
    return "unparsed"

def _num(rx, text):
    if not text: return None
    m = list(rx.finditer(text))
    if not m: return None
    x = int(m[-1].group(1)); return x if 0 <= x <= 10 else None
def parse_confidence(text): return _num(_CONF_RE, text)
def parse_blame(text): return _num(_BLAME_RE, text)
