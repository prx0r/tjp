from postagi_kernel.scenario import bayesian_update
from postagi_kernel.models import Evidence

def test_positive_evidence_raises_probability():
    ev=[Evidence("e","2026-01-01","paper","s",1.0,.8)]
    assert bayesian_update(.5,ev)>.5
