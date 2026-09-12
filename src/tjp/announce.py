"""Announcement scraper: Zendesk section index (works) → article URLs.
Per-article pages are challenge-walled; timestamps come from safetrade.com homepage
snippets (hand-verified, see listings.json). Re-run index to catch NEW listings.
"""
from __future__ import annotations
import json
import re
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent / "docs" / "safetrade"
INDEX = "https://r.jina.ai/https://support.safetrade.com/hc/en-us/sections/360002787112-Announcements"


def _get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "tjp-desk/0.1"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


def scrape_index() -> dict:
    t = _get(INDEX)
    out = {}
    for m in re.finditer(r"\[(.+?has been listed[^\]]*)\]\((https://support\.safetrade\.com[^)]+)\)", t):
        title, url = m.groups()
        sym = re.search(r"\(\$([A-Z0-9]+)\)", title)
        out[sym.group(1) if sym else title[:20]] = {"title": title, "url": url}
    known = {}
    for l in json.loads((BASE / "listings.json").read_text()):
        known[l["asset"]] = l["announced"]
    for sym, announced in known.items():
        out.setdefault(sym, {}).update({"announced": announced})
    (BASE / "announcements.json").write_text(json.dumps(out, indent=1))
    return out
