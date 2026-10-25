"""Print OpenRouter key usage/limit (never the key). Usage: python3 -I key_status.py <compute.env> [label]"""
import json, sys, urllib.request, datetime
key = None
for line in open(sys.argv[1]):
    if line.strip().startswith("OPENROUTER_API_KEY"):
        key = line.split("=", 1)[1].strip().strip('"').strip("'")
req = urllib.request.Request("https://openrouter.ai/api/v1/key", headers={"Authorization": f"Bearer {key}"})
d = json.load(urllib.request.urlopen(req, timeout=20))["data"]
safe = {k: d.get(k) for k in ("usage", "limit", "limit_remaining", "is_free_tier", "usage_daily")}
safe["checked_at"] = datetime.datetime.now().isoformat(); safe["label_arg"] = sys.argv[2] if len(sys.argv) > 2 else ""
print(json.dumps(safe))
