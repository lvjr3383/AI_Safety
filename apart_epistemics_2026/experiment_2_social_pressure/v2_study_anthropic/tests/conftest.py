import sys
from pathlib import Path
VA = Path(__file__).resolve().parents[1]
for p in (VA / "src", VA.parent / "v2_study/src", VA.parent / "src"): sys.path.insert(0, str(p))
