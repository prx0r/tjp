"""Desk index: what lives where. Built 2026-09-12 from 2 of 3 ZIPs (thesisdesk.zip pending)."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

def inventory() -> dict:
    out = {"blueprint": [], "kernel": [], "theses": []}
    bp = ROOT / "vendor" / "phone-blueprint"
    if bp.exists():
        out["blueprint"] = sorted(str(p.relative_to(ROOT)) for p in bp.rglob("*") if p.is_file())
    wk = ROOT / "vendor" / "worldstate-kernel"
    if wk.exists():
        out["kernel"] = sorted(str(p.relative_to(ROOT)) for p in wk.rglob("*") if p.is_file())
    th = ROOT / "docs" / "theses"
    if th.exists():
        out["theses"] = sorted(str(p.relative_to(ROOT)) for p in th.rglob("*.md"))
    return out
