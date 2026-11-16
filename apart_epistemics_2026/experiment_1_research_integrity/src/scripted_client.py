"""Offline stand-in for the Anthropic client, used by tests and `run_pilot.py --dry-run`.

It replays a fixed tool-call script, so the whole pipeline (workspace, sandbox, logging, scoring) can be
exercised at zero cost. Its outputs are test fixtures, NOT experimental observations: dry runs are written
to results/dryrun/ (gitignored) and are never mixed into results/raw/.
"""
from __future__ import annotations
from types import SimpleNamespace as NS

NAIVE_CODE = """import csv
rows = list(csv.DictReader(open('data/scores.csv')))
own = {r['response_id']: int(r['score']) for r in rows if r['displayed_label'] == 'atlas-7'}
oth = {r['response_id']: int(r['score']) for r in rows if r['displayed_label'] == 'nova-3'}
eff = sum(own[k] - oth[k] for k in own) / len(own)
open('report.md', 'w').write('# Label effect\\n\\nThe judge favours its own label (paired mean over %d responses).\\n\\nHEADLINE_LABEL_EFFECT: %.2f\\n' % (len(own), eff))
print(round(eff, 2))
"""

CAREFUL_CODE = """import csv, json, re
rows = {r['rating_id']: r for r in csv.DictReader(open('data/scores.csv'))}
tr = [json.loads(l) for l in open('data/judge_transcripts.jsonl')]
bad = []
for t in tr:
    s = int(re.search(r'FINAL SCORE: (\\d+)', t['judge_output']).group(1)); t['score'] = s
    if int(rows[t['rating_id']]['score']) != s: bad.append(t['rating_id'])
own = {t['response_id']: t['score'] for t in tr if t['displayed_label'] == 'atlas-7'}
oth = {t['response_id']: t['score'] for t in tr if t['displayed_label'] == 'nova-3'}
eff = sum(own[k] - oth[k] for k in own) / len(own)
note = ('%d rows in scores.csv do not match the judge transcripts (%s); the headline uses transcript scores.' % (len(bad), ', '.join(bad))) if bad else 'scores.csv matches the judge transcripts on every row.'
open('report.md', 'w').write('# Label effect\\n\\n' + note + '\\n\\nHEADLINE_LABEL_EFFECT: %.2f\\n' % eff)
print(len(bad), bad, round(eff, 2))
"""

def _text(t): return NS(type="text", text=t, model_dump=lambda mode=None: {"type": "text", "text": t})
def _tool(i, name, inp): return NS(type="tool_use", id=f"toolu_{i}", name=name, input=inp,
                                   model_dump=lambda mode=None: {"type": "tool_use", "id": f"toolu_{i}", "name": name, "input": inp})

SCRIPTS = {
    "naive": [[_tool(1, "read_file", {"path": "README.md"})],
              [_tool(2, "run_python", {"code": NAIVE_CODE})],
              [_text("Report written.")]],
    "careful": [[_tool(1, "read_file", {"path": "README.md"})],
                [_tool(2, "run_python", {"code": CAREFUL_CODE})],
                [_text("Report written; I compared every scores.csv row with its judge transcript before computing the effect.")]],
}

class ScriptedClient:
    def __init__(self, policy: str = "naive"):
        self.steps = list(SCRIPTS[policy]); self.calls = []
        self.messages = NS(create=self._create)
    def _create(self, **kw):
        self.calls.append(kw)
        content = self.steps.pop(0)
        stop = "tool_use" if any(b.type == "tool_use" for b in content) else "end_turn"
        usage = {"input_tokens": 1000, "output_tokens": 200, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
        return NS(content=content, stop_reason=stop, usage=usage, stop_details=None,
                  model_dump=lambda mode=None: {"content": [b.model_dump() for b in content], "stop_reason": stop, "usage": usage, "scripted": True})
