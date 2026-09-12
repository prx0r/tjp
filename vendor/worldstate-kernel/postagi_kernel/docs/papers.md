# Paper-to-kernel registry

The kernel distinguishes **exact published transformations**, **paper-compatible adapters**, and **project extensions**. This prevents an implementation stub from being mislabeled as a reproduction.

| Work | Kernel module | Status | What is reproduced |
|---|---|---|---|
| Fenoaltea et al. (2026), *Anticipating Innovation Using Large Language Models*, arXiv:2605.04875 | `methods/techtoken.py` | Exact aggregation, model adapter | Context-specific IPC cosine similarities and the paper's **top 1% mean** context-similarity aggregation. The proprietary/paper-scale fine-tuned transformer is not retrained here. |
| Ma (2025), *Technological Obsolescence*, RFS / NBER w29504 | `methods/obsolescence.py` | Exact formula | Fixed external technology base at `t-w`; external citations to that fixed base at `t-w` and `t`; `-[ln(Cit_t)-ln(Cit_t-w)]`. |
| Sternfeld et al. (2025), *Monitoring Transformative Technological Convergence...*, arXiv:2510.25370 | `methods/convergence.py` | Core graph math | q-gram + soft-cardinality Dice noun stapling, threshold 0.85, Louvain resolution 0.85, eigenvector centrality, and temporal Jaccard convergence. |
| Yang (2023), *Predictive Patentomics*, arXiv:2307.01202 | `methods/patentomics.py` | Paper-compatible model | LLM/patent embeddings + structural variables; acceptance classification and patent-value regression with temporal split. Exact ada-002 historical embeddings/data are external. |
| Ye et al. (2024), *MIRAI*, arXiv:2407.01231 | `methods/mirai.py` | Interface + deterministic baseline | Historical structured-event retrieval contract and time-aware forecast interface. Full ReAct/LLM agent is available from the pinned original repo. |
| Chang et al. (2025), *Learning Production Functions for Supply Chains with GNNs*, arXiv:2407.18772 | `methods/supplychain.py` | Interface + project primitive | Attention-normalized production weights and inventory conservation interface. Full SC-TGN/SC-GraphMixer implementation is pinned to the authors' repo. |
| Xia et al. (2026), *Agentic Trading*, arXiv:2605.19337 | `backtest.py` | Protocol response | Explicit time ordering, forward-return semantics, universe per rebalance, costs, turnover, and reproducibility metadata. |
| Lopez-Lira & Tang (2026 JFE / arXiv:2304.07619) | architectural constraint | Design response | Treats obvious LLM-readable textual alpha as decaying with model adoption; the project therefore emphasizes multi-hop causal propagation rather than headline sentiment. |

Primary links:
- https://arxiv.org/abs/2605.04875
- https://doi.org/10.1093/rfs/hhaf059
- https://arxiv.org/abs/2510.25370
- https://arxiv.org/abs/2307.01202
- https://arxiv.org/abs/2407.01231
- https://arxiv.org/abs/2407.18772
- https://arxiv.org/abs/2605.19337
- https://arxiv.org/abs/2304.07619
