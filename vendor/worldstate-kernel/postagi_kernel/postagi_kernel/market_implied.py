"""Reverse-engineer market-implied scenario probabilities from priced signals."""
from __future__ import annotations
import numpy as np
from scipy.optimize import lsq_linear


def infer_market_probabilities(exposure_matrix: np.ndarray, priced_impacts: np.ndarray,
                               ridge: float=1e-3, prior: np.ndarray|None=None) -> np.ndarray:
    """Bounded ridge inverse problem: priced_impacts ~= X @ probabilities.

    This is a kernel primitive, not a claim that probabilities are uniquely
    identifiable from prices. Use multiple instruments/valuation residuals and
    inspect conditioning. Bounds enforce probability-like [0,1] outputs.
    """
    X=np.asarray(exposure_matrix,float); y=np.asarray(priced_impacts,float)
    if X.ndim!=2 or y.shape!=(X.shape[0],): raise ValueError("shape mismatch")
    k=X.shape[1]
    p0=np.full(k,.5) if prior is None else np.asarray(prior,float)
    A=np.vstack([X,np.sqrt(ridge)*np.eye(k)])
    b=np.concatenate([y,np.sqrt(ridge)*p0])
    res=lsq_linear(A,b,bounds=(0,1),lsmr_tol='auto')
    return res.x


def condition_number(exposure_matrix: np.ndarray) -> float:
    return float(np.linalg.cond(np.asarray(exposure_matrix,float)))
