"""Desk tests part 7: killfeed binaries."""
from tjp.killfeed import k_score, verdict, set_state


def test_weights_and_criticals(tmp_path, monkeypatch):
    import tjp.killfeed as kf

    monkeypatch.setattr(kf, "_STORE", tmp_path / "k.json")
    assert k_score({k: "TRUE" for k in ("NEED", "GAP", "LAG", "WTP", "SUB")}) == 100.0
    v = set_state("hbm", "NEED", "TRUE", "t")
    for c in ("GAP", "LAG", "WTP", "SUB"):
        set_state("hbm", c, "TRUE", "t")
    assert verdict("hbm")["band"] == "SCARCITY RENT ACTIVE"
    assert set_state("hbm", "LAG", "FALSE", "samsung qualified early")["band"] == "LATE — DO NOT ADD"
    assert set_state("hbm", "GAP", "FALSE", "supply exceeds demand")["band"] == "KILL"
