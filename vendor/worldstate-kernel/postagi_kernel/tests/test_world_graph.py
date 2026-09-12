from postagi_kernel.world_graph import WorldGraph,CausalEdge

def test_signed_causal_propagation():
    g=WorldGraph();
    for n,t in [('agi','world_state'),('labor_cost','cost_curve'),('consulting','profit_pool'),('ACN','company')]: g.add_node(n,t)
    g.add_edge(CausalEdge('agi','labor_cost',-1,1,0))
    g.add_edge(CausalEdge('labor_cost','consulting',1,1,0))
    g.add_edge(CausalEdge('consulting','ACN',1,1,0))
    out=g.propagate({'agi':1})
    assert out['ACN']<0
