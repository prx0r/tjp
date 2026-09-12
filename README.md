# tjp — thesis desk webapp

One desk over three inputs: phone-agent blueprint rubric/scorer, worldstate kernel backtester,
memo thesis sections. Structure copied from BEAR (src package + static dashboard + tests).

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
python3 -m pytest -q
tjp inventory
tjp serve  # → :8123, dashboard/ served alongside
```

Vendor dirs are pristine reference. thesisdesk.zip (3rd ZIP) still pending — docs/theses fills in on arrival.
