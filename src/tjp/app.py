"""tjp API: desk inventory + health. Vendor engines stay library-only behind these routes."""
from fastapi import FastAPI
from .desk import inventory

app = FastAPI(title="tjp thesis desk")


@app.get("/api/health")
def health() -> dict:
    return {"ok": True}


@app.get("/api/inventory")
def inventory_route() -> dict:
    inv = inventory()
    return {k: len(v) for k, v in inv.items()}


@app.get("/api/inventory/files")
def inventory_files() -> dict:
    return inventory()


@app.get("/api/theses")
def theses() -> list:
    import json
    from pathlib import Path

    out = []
    for f in sorted((Path(__file__).resolve().parent.parent.parent / "docs" / "agitheses").glob("*.json")):
        if f.name == "schema.json":
            continue
        d = json.loads(f.read_text())
        out.append({"id": d["id"], "subject": d["subject"], "kind": d["kind"], "theses": d["theses"]})
    return out


@app.post("/api/positions")
def add_position(thesis_id: str, thesis_n: int, action: str, note: str = "") -> dict:
    from .positions import log_position

    return log_position(thesis_id, thesis_n, action, note)


@app.get("/api/positions/{thesis_id}")
def get_positions(thesis_id: str) -> list:
    from .positions import positions_for

    return positions_for(thesis_id)


@app.post("/api/vault/{op}")
def vault_op(op: str, amount: float) -> dict:
    from . import vault

    fn = {"deposit": vault.deposit, "lock": vault.lock, "withdraw": vault.withdraw}.get(op)
    if not fn or amount <= 0:
        return {"error": "op must be deposit|lock|withdraw with amount > 0 (paper only)"}
    return fn(amount)


@app.get("/api/vault/balance")
def vault_balance() -> dict:
    from . import vault

    return vault.balance()


@app.get("/api/trades")
def trades() -> list:
    import json
    from pathlib import Path

    base = Path(__file__).resolve().parent.parent.parent
    d = json.loads((base / "vendor" / "thesisdesk" / "data" / "trades.json").read_text())
    return d.get("trades", [])


@app.get("/api/gold")
def gold() -> list:
    import json
    from pathlib import Path

    from .gold import score

    base = Path(__file__).resolve().parent.parent.parent
    out = []
    for f in sorted((base / "docs" / "gold").glob("*.json")):
        a = json.loads(f.read_text())
        out.append({"trade_id": a["trade_id"], "seed": a["band_seed"], "rationale": a["rationale"], **score(a["factors"])})
    return out
