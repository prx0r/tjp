import numpy as np
from postagi_kernel.market_implied import infer_market_probabilities

def test_inverse_probability_recovers_signal():
    X=np.array([[1,0],[0,1],[1,1]],float); p=np.array([.2,.8]); y=X@p
    ph=infer_market_probabilities(X,y,ridge=1e-8,prior=p)
    assert np.max(np.abs(ph-p))<1e-4
