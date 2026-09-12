"""TechToken-compatible context-similarity kernel.

Fenoaltea et al. (2026) define context similarity (CS) between two IPC
technologies from context-specific IPC embeddings. For TechToken embeddings,
CS is the average cosine similarity among the top 1% most-similar embedding
pairs across a chosen time window. This module implements that published
aggregation exactly; model fine-tuning is delegated to an embedding backend.
"""
from __future__ import annotations
import numpy as np


def _normalize(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x[None, :]
    norm = np.linalg.norm(x, axis=1, keepdims=True)
    return x / np.clip(norm, 1e-12, None)


def pairwise_cosine(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return _normalize(a) @ _normalize(b).T


def context_similarity(a: np.ndarray, b: np.ndarray, top_fraction: float = 0.01) -> float:
    """Average of the top `top_fraction` pairwise cosine similarities.

    The paper uses top 1% (0.01) for context-specific TechToken IPC vectors.
    At least one pair is always retained.
    """
    if not 0 < top_fraction <= 1:
        raise ValueError("top_fraction must be in (0,1]")
    sims = pairwise_cosine(a, b).ravel()
    if sims.size == 0:
        raise ValueError("empty embedding set")
    k = max(1, int(np.ceil(sims.size * top_fraction)))
    # partition avoids O(n log n) full sorting on paper-scale windows
    top = np.partition(sims, sims.size - k)[-k:]
    return float(top.mean())


def innovation_lead_signal(history: list[tuple[int, float]], min_slope: float = 0.0) -> dict:
    """Simple operationalization of rising CS before first combination.

    The exact TechToken paper evaluates new-combination prediction from CS.
    This helper estimates a robust linear slope for a pre-combination history;
    it does not claim to reproduce their trained transformer.
    """
    if len(history) < 2:
        return {"slope": 0.0, "latest": history[-1][1] if history else 0.0, "emerging": False}
    years = np.array([x for x, _ in history], dtype=float)
    vals = np.array([y for _, y in history], dtype=float)
    slope = float(np.polyfit(years - years.mean(), vals, 1)[0])
    return {"slope": slope, "latest": float(vals[-1]), "emerging": bool(slope > min_slope)}
