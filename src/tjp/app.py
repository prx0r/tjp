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
