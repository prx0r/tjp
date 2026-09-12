"""Inventory / production-function abstraction inspired by Chang et al. (2025).

The paper's SC-TGN/SC-GraphMixer learns hidden input->output production
functions using attention plus an inventory module. This lightweight kernel
implements the inventory-conservation interface and attention-normalized
input weights; the full paper code is pinned in external/manifest.json.
"""
from __future__ import annotations
import numpy as np


def attention_production_weights(raw_attention: np.ndarray) -> np.ndarray:
    x = np.asarray(raw_attention, float)
    x = x - x.max(axis=-1, keepdims=True)
    e = np.exp(x)
    return e / np.clip(e.sum(axis=-1, keepdims=True), 1e-12, None)


def inventory_transition(inventory: np.ndarray, inputs: np.ndarray, outputs: np.ndarray) -> np.ndarray:
    nxt = np.asarray(inventory, float) + np.asarray(inputs, float) - np.asarray(outputs, float)
    return nxt


def inventory_violation_loss(inventory_next: np.ndarray) -> float:
    """Penalty for impossible negative inventory states."""
    neg = np.minimum(np.asarray(inventory_next, float), 0.0)
    return float(np.square(neg).mean())


def bottleneck_score(input_criticality: np.ndarray, supplier_concentration: np.ndarray,
                     lead_time_z: np.ndarray, substitution_difficulty: np.ndarray) -> np.ndarray:
    """Cross-sectional physical bottleneck score used by the world-state graph.

    This is a project extension, not a formula claimed from Chang et al.
    """
    arrs = [np.asarray(x, float) for x in (input_criticality, supplier_concentration, lead_time_z, substitution_difficulty)]
    return np.mean(np.vstack(arrs), axis=0)
