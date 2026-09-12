import numpy as np
from postagi_kernel.methods.techtoken import context_similarity

def test_top_one_percent_is_tail_mean():
    a=np.eye(2); b=np.eye(2)
    # four similarities [1,0,0,1], top 1% retains one of the 1s
    assert context_similarity(a,b,0.01) == 1.0

def test_all_pairs_mean():
    a=np.eye(2); b=np.eye(2)
    assert abs(context_similarity(a,b,1.0)-0.5)<1e-12
