from __future__ import annotations

# Make this helper runnable both after `pip install -e .` and directly from a
# source checkout via `python scripts/run_demo.py`.
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from postagi_kernel.demo import run_demo

if __name__ == "__main__":
    rankings, metrics = run_demo()
    print(rankings.to_string(index=False))
    print(metrics)
