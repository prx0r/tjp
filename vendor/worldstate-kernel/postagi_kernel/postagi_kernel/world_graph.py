"""Typed causal graph for world-state -> cash-flow propagation."""
from __future__ import annotations
from dataclasses import dataclass
import networkx as nx

NODE_TYPES={"world_state","capability","cost_curve","behavior","demand","profit_pool","company","constraint"}

@dataclass(frozen=True)
class CausalEdge:
    source: str
    target: str
    elasticity: float
    confidence: float = 1.0
    delay_years: float = 0.0

class WorldGraph:
    def __init__(self):
        self.g=nx.DiGraph()

    def add_node(self,node_id:str,node_type:str,**attrs):
        if node_type not in NODE_TYPES: raise ValueError(f"unknown node type {node_type}")
        self.g.add_node(node_id,node_type=node_type,**attrs)

    def add_edge(self,edge:CausalEdge):
        if edge.source not in self.g or edge.target not in self.g: raise KeyError("add nodes before edges")
        self.g.add_edge(edge.source,edge.target,elasticity=float(edge.elasticity),confidence=float(edge.confidence),delay_years=float(edge.delay_years))

    def propagate(self,shocks:dict[str,float],horizon_years:float=5.0,damping:float=.92) -> dict[str,float]:
        """Propagate signed shocks through a DAG.

        Each edge multiplies source shock by elasticity, confidence, damping,
        and an exponential penalty for causal delay relative to horizon.
        Multiple independent paths add. Cycles are rejected because causal
        feedback requires a dynamic model rather than accidental recursion.
        """
        if not nx.is_directed_acyclic_graph(self.g):
            raise ValueError("world graph must be a DAG for static propagation")
        state={n:0.0 for n in self.g.nodes}
        for n,v in shocks.items():
            if n not in state: raise KeyError(n)
            state[n]+=float(v)
        for src in nx.topological_sort(self.g):
            for dst,ed in self.g[src].items():
                delay=max(ed.get("delay_years",0.0),0.0)
                if delay>horizon_years: continue
                time_weight=max(0.0,1.0-delay/max(horizon_years,1e-9))
                state[dst]+=state[src]*ed["elasticity"]*ed["confidence"]*damping*time_weight
        return state

    def company_exposures(self,scenario_shocks:dict[str,dict[str,float]],horizon_years:float=5.0) -> dict[str,dict[str,float]]:
        companies=[n for n,d in self.g.nodes(data=True) if d["node_type"]=="company"]
        out={c:{} for c in companies}
        for sid,shock in scenario_shocks.items():
            state=self.propagate(shock,horizon_years)
            for c in companies: out[c][sid]=state[c]
        return out
