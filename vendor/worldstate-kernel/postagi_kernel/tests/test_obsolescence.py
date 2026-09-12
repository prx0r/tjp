from postagi_kernel.methods.obsolescence import technological_obsolescence, firm_obsolescence

def test_decline_is_positive():
    assert technological_obsolescence(100,50) > 0
    assert technological_obsolescence(50,100) < 0

def test_fixed_base_and_external_only():
    backward=[
      {"citing_firm":"A","citing_year":2020,"cited_patent":"p1","cited_owner":"B"},
      {"citing_firm":"A","citing_year":2020,"cited_patent":"p2","cited_owner":"A"},
    ]
    forward=[]
    forward += [{"citing_firm":"X","citing_year":2020,"cited_patent":"p1"} for _ in range(4)]
    forward += [{"citing_firm":"X","citing_year":2025,"cited_patent":"p1"} for _ in range(2)]
    forward += [{"citing_firm":"A","citing_year":2025,"cited_patent":"p1"} for _ in range(9)]
    out=firm_obsolescence("A",2025,5,backward,forward)
    assert out["base_size"]==1 and out["citations_start"]==4 and out["citations_end"]==2
    assert out["obsolescence"]>0
