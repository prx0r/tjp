from postagi_kernel.models import Scenario,Company
from postagi_kernel.scoring import world_divergence_score

def test_positive_exposure_positive_divergence():
    s=[Scenario("x","x",1,.8,.4)]
    c=Company("X","X","x",exposures={"x":1})
    v,_=world_divergence_score(c,s)
    assert v>0
