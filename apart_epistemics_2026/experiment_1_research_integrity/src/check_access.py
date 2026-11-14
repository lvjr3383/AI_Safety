"""Free, inference-free check that the API key can see the configured model (GET /v1/models/{id}).
Logs the result to results/model_checks.jsonl. Prints nothing about the key itself."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EXPERIMENT, RESULTS, append_jsonl, load_api_key, now_iso

def main():
    import anthropic
    model = sys.argv[1] if len(sys.argv) > 1 else EXPERIMENT["runtimes"]["anthropic_api"]["model"]
    client = anthropic.Anthropic(api_key=load_api_key())
    try:
        m = client.models.retrieve(model)
        rec = {"ts": now_iso(), "requested": model, "ok": True, "id": m.id, "display_name": getattr(m, "display_name", None),
               "max_input_tokens": getattr(m, "max_input_tokens", None)}
    except anthropic.APIStatusError as e:
        rec = {"ts": now_iso(), "requested": model, "ok": False, "status": e.status_code, "error": type(e).__name__}
    append_jsonl(RESULTS / "model_checks.jsonl", rec)
    print(rec)
    sys.exit(0 if rec["ok"] and rec["id"] == model else 1)

if __name__ == "__main__":
    main()
