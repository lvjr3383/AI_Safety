"""Anthropic Messages API runtime: a manual tool-use loop over four sandboxed tools.

A manual loop (rather than the SDK tool runner) so that every request, response, usage record and tool
result is logged in order, and so the harness can stop on refusal / max_tokens instead of retrying silently.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EXPERIMENT, BudgetGuard, tree_hashes, usage_cost
from sandbox import TOOL_SCHEMAS, Workspace

def _dump(obj):
    if hasattr(obj, "model_dump"): return obj.model_dump(mode="json")
    if isinstance(obj, (list, tuple)): return [_dump(o) for o in obj]
    if isinstance(obj, dict): return {k: _dump(v) for k, v in obj.items()}
    return obj

def _usage(u) -> dict:
    u = _dump(u) or {}
    return {k: (u.get(k) or 0) for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")}

class AnthropicAPIRuntime:
    name = "anthropic_api"

    def __init__(self, client, guard: BudgetGuard, run_id: str, cfg=None, pilot=None, model=None):
        self.cfg = cfg or EXPERIMENT["runtimes"]["anthropic_api"]; self.pilot = pilot or EXPERIMENT["pilot"]
        self.client, self.guard, self.run_id = client, guard, run_id
        self.model = model or self.cfg["model"]
        if self.model not in EXPERIMENT["pricing_usd_per_mtok"]: raise ValueError(f"no pricing for {self.model}")

    def _worst_case(self, messages) -> float:
        # crude upper bound: ~3 chars per token for the whole context, uncached, plus a full max_tokens reply
        chars = sum(len(str(_dump(m))) for m in messages) + 8000
        pr = EXPERIMENT["pricing_usd_per_mtok"][self.model]
        return (chars / 3 * pr["input"] + self.cfg["max_tokens"] * pr["output"]) / 1e6

    def run(self, ws: Path, prompt: str, system: str, rec) -> dict:
        tools = Workspace(ws, self.pilot["python_timeout_s"], self.pilot["max_tool_output_chars"])
        messages = [{"role": "user", "content": prompt}]
        params = {"model": self.model, "max_tokens": self.cfg["max_tokens"], "system": system, "tools": TOOL_SCHEMAS,
                  "thinking": self.cfg["thinking"], "output_config": {"effort": self.cfg["effort"]}}
        if self.cfg.get("prompt_caching"): params["cache_control"] = {"type": "ephemeral"}
        rec.raw({"type": "request_params", "params": params})
        totals, cost, served = {}, 0.0, set()
        for turn in range(self.pilot["max_agent_turns"]):
            self.guard.check(self._worst_case(messages))
            rec.raw({"type": "request", "turn": turn, "n_messages": len(messages)})
            resp = self.client.messages.create(messages=messages, **params)
            served.add(getattr(resp, "model", None) or "unreported")
            u = _usage(resp.usage); c = usage_cost(self.model, u); cost += c
            self.guard.record(self.run_id, self.model, u, c)
            for k, v in u.items(): totals[k] = totals.get(k, 0) + v
            rec.raw({"type": "response", "turn": turn, "response": _dump(resp), "cost_usd": c})
            for b in resp.content:
                if b.type == "text": rec.norm("assistant_text", text=b.text, turn=turn)
                elif b.type == "thinking": rec.norm("thinking", text=getattr(b, "thinking", "") or "", turn=turn)
                elif b.type == "tool_use": rec.norm("tool_call", name=b.name, input=_dump(b.input), id=b.id, turn=turn)
            done = {"usage": totals, "cost_usd": cost, "turns": turn + 1, "stop_reason": resp.stop_reason, "served_models": sorted(served)}
            if resp.stop_reason == "end_turn": return {**done, "status": "completed"}
            if resp.stop_reason in ("refusal", "max_tokens"):
                return {**done, "status": resp.stop_reason, "stop_details": _dump(getattr(resp, "stop_details", None))}
            if resp.stop_reason != "tool_use": return {**done, "status": f"unexpected_stop:{resp.stop_reason}"}
            messages.append({"role": "assistant", "content": resp.content})
            results = []
            for b in resp.content:
                if b.type != "tool_use": continue
                out, err = tools.call(b.name, _dump(b.input))
                rec.norm("tool_result", name=b.name, id=b.id, output=out, is_error=err, turn=turn)
                rec.raw({"type": "tool_execution", "turn": turn, "id": b.id, "name": b.name, "input": _dump(b.input),
                         "output": out, "is_error": err, "workspace_sha256": tree_hashes(ws)})
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": out, **({"is_error": True} if err else {})})
            messages.append({"role": "user", "content": results})
        return {"usage": totals, "cost_usd": cost, "turns": self.pilot["max_agent_turns"], "status": "turn_limit", "served_models": sorted(served)}
