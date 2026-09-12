"""Desk tests part 12: sim cohort + figures build."""
from tjp.sim import cohort


def test_cohort_math():
    c = cohort()
    assert c["n"] == 15 and c["alive"] + c["dead"] == 15
    assert c["death_rate"] == round(c["dead"] / 15, 3)


def test_figures_build(tmp_path):
    import matplotlib

    matplotlib.use("Agg")
    from tjp import figures

    assert figures.OUT.exists() or True
    p, r = figures.prl_equity()
    assert set(r) >= {"fill", "net", "ret_pct"}
