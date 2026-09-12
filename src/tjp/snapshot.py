"""Daily snapshot job: free CoinGecko simple/price → docs/snapshots/YYYY-MM-DD.json. Graceful on failure."""
from __future__ import annotations
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

COINS = ["monero", "zcash", "nillion", "dusk-network", "aleo", "quantum-resistant-ledger"]
OUT = Path(__file__).resolve().parent.parent.parent / "docs" / "snapshots"


def snapshot() -> dict:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=" + ",".join(COINS) + "&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "tjp-desk/0.1"})
        data = json.load(urllib.request.urlopen(req, timeout=25))
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}
    OUT.mkdir(parents=True, exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    (OUT / f"{day}.json").write_text(json.dumps({"ok": True, "ts": datetime.now(timezone.utc).isoformat(), "prices": data}, indent=1))
    return {"ok": True, "day": day, "coins": len(data)}


if __name__ == "__main__":
    print(json.dumps(snapshot(), indent=1))
