"""Graphs: listing timeline, alive/dead, today's movers, PRL intraday equity. Agg backend (no display)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import json  # noqa: E402
import glob  # noqa: E402
from pathlib import Path  # noqa: E402

OUT = Path(__file__).resolve().parent.parent.parent / "docs" / "safetrade" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def timeline():
    ls = json.load(open("/tjp/docs/safetrade/listings.json"))
    ds = sorted(l["announced"][:10] for l in ls if l["announced"])
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.eventplot([[i for i in range(len(ds))]], lineoffsets=1)
    ax.set_title(f"SafeTrade listings tracked ({len(ds)}) Jan-Sep 2026")
    ax.set_xlabel("listing sequence")
    fig.savefig(OUT / "timeline.png", dpi=80)
    plt.close(fig)
    return str(OUT / "timeline.png")


def alive_dead(alive: int, dead: int):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(["alive", "dead"], [alive, dead])
    ax.set_title(f"2026 listing cohort: {alive} alive / {dead} dead")
    fig.savefig(OUT / "alive_dead.png", dpi=80)
    plt.close(fig)
    return str(OUT / "alive_dead.png")


def movers():
    f = sorted(glob.glob("/tjp/docs/safetrade/snapshots/*.json"))[-1]
    rows = json.load(open(f))["rows"]
    u = [r for r in rows if r["pair"].endswith("/USDT")]
    top = sorted(u, key=lambda r: float(r["chg_24h"].strip("%+")), reverse=True)[:8]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh([r["pair"] for r in top], [float(r["chg_24h"].strip("%+")) for r in top])
    ax.set_title("Top USDT movers (snapshot)")
    fig.savefig(OUT / "movers.png", dpi=80)
    plt.close(fig)
    return str(OUT / "movers.png")


def prl_equity():
    from tjp.buyhold import buy_hold

    tape = [json.loads(line) for line in
            open("/tjp/docs/safetrade/tape/prlusdt.jsonl").read().splitlines() if line.strip()]
    px = [float(t["price"]) for t in reversed(tape)]
    r = buy_hold(px, entry_idx=0, size=1000.0)
    eq = [1000.0]
    qty = 1000.0 / px[1]
    for p in px[1:]:
        eq.append(qty * p)
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(eq)
    ax.set_title(f"PRL $1000 buy-hold, {len(px)} fills: {r['ret_pct']}% net")
    fig.savefig(OUT / "prl_equity.png", dpi=80)
    plt.close(fig)
    return str(OUT / "prl_equity.png"), r


if __name__ == "__main__":
    print(timeline())
    print(alive_dead(11, 4))
    print(movers())
    print(prl_equity())
