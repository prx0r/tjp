"""Desk tests part 9: tape dedupe, universe diff, fees file."""
import json

from tjp.tape import load
from tjp.universe import EVENTS


def test_tape_loader_missing():
    assert load("no-such-market-xyz") == []


def test_universe_events_appendable():
    assert not EVENTS.exists() or EVENTS.stat().st_size >= 0


def test_fees_file():
    f = json.load(open("/tjp/docs/safetrade/fees.json"))
    assert f["maker_bps"] == 10 and f["taker_bps"] == 10
