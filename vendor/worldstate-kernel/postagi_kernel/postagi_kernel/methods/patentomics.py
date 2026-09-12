"""Predictive Patentomics-compatible supervised models.

Yang (2023) combines LLM text embeddings with structural patent variables to
predict grant success and patent value. This module preserves that separation,
with leakage-safe temporal splits and small sklearn MLPs for reproducibility.
It intentionally does not claim to reproduce proprietary ada-002 embeddings.
"""
from __future__ import annotations
import numpy as np
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score, r2_score


def combine_embedding_structural(embeddings: np.ndarray, structural: np.ndarray) -> np.ndarray:
    e, s = np.asarray(embeddings, float), np.asarray(structural, float)
    if e.shape[0] != s.shape[0]:
        raise ValueError("row mismatch")
    return np.hstack([e, s])


def temporal_split(years: np.ndarray, train_through: int, test_year: int):
    years = np.asarray(years)
    return years <= train_through, years == test_year


def fit_acceptance_model(X: np.ndarray, y: np.ndarray, random_state: int = 7):
    model = make_pipeline(
        StandardScaler(),
        MLPClassifier(hidden_layer_sizes=(64, 16), activation="relu", max_iter=700,
                      early_stopping=True, random_state=random_state)
    )
    return model.fit(X, y)


def fit_value_model(X: np.ndarray, y: np.ndarray, random_state: int = 7):
    model = make_pipeline(
        StandardScaler(),
        MLPRegressor(hidden_layer_sizes=(64, 16), activation="relu", max_iter=700,
                     early_stopping=True, random_state=random_state)
    )
    return model.fit(X, y)


def evaluate_acceptance(model, X, y) -> dict:
    p = model.predict_proba(X)[:,1]
    return {"auc": float(roc_auc_score(y, p)), "mean_pred": float(p.mean())}


def evaluate_value(model, X, y) -> dict:
    pred = model.predict(X)
    return {"r2": float(r2_score(y, pred)), "mean_pred": float(np.mean(pred))}
