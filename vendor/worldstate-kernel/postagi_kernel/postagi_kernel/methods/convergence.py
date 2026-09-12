"""Sternfeld et al. technological-convergence primitives.

Implements 3-gram similarity + soft-cardinality Dice noun stapling,
conservative 0.85 threshold, temporal topic Jaccard, and graph metrics.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations
from typing import Iterable
import networkx as nx


def qgrams(s: str, q: int = 3) -> Counter:
    s = f"  {s.lower().strip()}  "
    if len(s) < q:
        return Counter([s])
    return Counter(s[i:i+q] for i in range(len(s)-q+1))


def qgram_similarity(a: str, b: str, q: int = 3) -> float:
    """Normalized multiset q-gram overlap equivalent to 1-normalized L1.

    The paper writes this as 1 minus the aggregate q-gram count mismatch.
    We use the standard denominator sum(|Qa|+|Qb|), avoiding the zero/negative
    denominator typo that appears in some text extractions of Eq. (3).
    """
    A, B = qgrams(a, q), qgrams(b, q)
    keys = set(A) | set(B)
    denom = sum(A.values()) + sum(B.values())
    if denom == 0:
        return 1.0
    l1 = sum(abs(A[k] - B[k]) for k in keys)
    return max(0.0, min(1.0, 1.0 - l1 / denom))


def soft_cardinality(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    total = 0.0
    for ti in tokens:
        denom = sum(qgram_similarity(ti, tj) for tj in tokens)
        total += 1.0 / max(denom, 1e-12)
    return total


def soft_intersection_cardinality(a: list[str], b: list[str]) -> float:
    """Soft intersection induced from |A∪B| = |A|+|B|-|A∩B|."""
    ca, cb = soft_cardinality(a), soft_cardinality(b)
    cu = soft_cardinality(a + b)
    return max(0.0, ca + cb - cu)


def soft_dice(a: str, b: str) -> float:
    ta, tb = a.lower().split(), b.lower().split()
    ca, cb = soft_cardinality(ta), soft_cardinality(tb)
    if ca + cb == 0:
        return 1.0
    inter = soft_intersection_cardinality(ta, tb)
    return max(0.0, min(1.0, 2 * inter / (ca + cb)))


def should_staple(a: str, b: str, threshold: float = 0.85) -> bool:
    return soft_dice(a, b) >= threshold


def temporal_jaccard(topic_a_docs: set[str], topic_b_docs: set[str]) -> float:
    union = topic_a_docs | topic_b_docs
    return len(topic_a_docs & topic_b_docs) / len(union) if union else 0.0


def convergence_delta(series_a: dict[int, set[str]], series_b: dict[int, set[str]]) -> dict[int, float]:
    years = sorted(set(series_a) | set(series_b))
    return {y: temporal_jaccard(series_a.get(y,set()), series_b.get(y,set())) for y in years}


def topic_graph(triples: Iterable[dict]) -> nx.Graph:
    """Aggregate triples into weighted undirected topic graph."""
    g = nx.Graph()
    for tr in triples:
        a, b = tr["subject_topic"], tr["object_topic"]
        if a == b:
            continue
        if g.has_edge(a, b):
            g[a][b]["weight"] += 1
        else:
            g.add_edge(a, b, weight=1)
    return g


def graph_summary(g: nx.Graph) -> dict:
    if len(g) == 0:
        return {"communities": [], "eigenvector_centrality": {}}
    try:
        communities = list(nx.community.louvain_communities(g, weight="weight", resolution=0.85, seed=7))
    except Exception:
        communities = list(nx.community.greedy_modularity_communities(g, weight="weight"))
    try:
        centrality = nx.eigenvector_centrality_numpy(g, weight="weight")
    except Exception:
        centrality = nx.degree_centrality(g)
    return {
        "communities": [sorted(c) for c in communities],
        "eigenvector_centrality": {k: float(v) for k,v in centrality.items()},
    }
