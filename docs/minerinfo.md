# Minerinfo — compute arbitrage router (2026-09-12, saved word for word)

Not "a mining rig" but a **compute arbitrage router**: highest expected return per dollar across
CPU/GPU/RAM/bandwidth/inference, renting cheapest compatible resource into best-paying workload.

```text
COMPUTE SOURCES (cheap CPU/GPU/RAM/inference API/idle) → NORMALIZED CAPACITY ($/CPU-h, $/GPU-h,
$/VRAM-h, $/1M tokens, $/TFLOP-h, interruptibility, bandwidth, latency) → WORKLOAD ADAPTERS
(XMR/Pearl/QUAN/Bittensor/Akash/batch/inference resale) → BENCHMARK+PROFIT MODEL (gross − compute −
bandwidth − fees − failure − switching) → ROUTER START/STOP/SWITCH
```

## Non-local rig

Control plane ≠ compute plane. VPS orchestrator, workers expose id/provider/cpu/gpu/vram/ram/
price/spot/network/images/status; controller deploys Docker. Hetzner + Salad 4090 + rented 3090 +
laptop + Akash = one virtual rig.

## Cheap GPU (Salad, interruptible, per-second)

4090 ~$0.16/h, 3090 ~$0.09/h ($2.16/day), 4080 ~$0.11/h, 5070 Ti ~$0.10/h, 5060 Ti 16GB ~$0.07/h,
from ~$0.04/h ([Salad][1]). Workload gross >$2.16/day before overhead = interesting. Join against
miner-profitability DB + live cloud prices.

## Pearl vLLM miner + caveat

Official repo now ships vLLM miner + pearl-gateway bridge ([GitHub][2]): GPU → vLLM → model compute →
miner/gateway → reward. BUT June 2026 study argued deployed cuPOW was commodity matrix compute, not
useful inference ([arXiv][3]). Distinguish thesis from implementation; benchmark the vLLM miner independently.

## Bittensor = AI mining, clearest version

Subnets pay for inference/embeddings/training/search — validators score output, emissions follow quality
([Bittensor][4]). Arbitrage: buy intelligence $X → subnet rewards >$X. Moat = routing (easy→cheap local,
medium→cheap hosted, hard→frontier), not hardware. EV/task = reward×pass_prob − inference − compute.
Cheap 61%-pass model can beat 94% frontier economically. LLM mining economics.

## Three earning modes

A. Sell raw compute (Akash providers bid CPU/RAM/GPU ([Akash][5]); io.net workers earn rentals+rewards ([Worker][6])).
B. Cryptographic mining (Pearl/QUAN/XMR). C. Intelligent work (Bittensor-style scored answers) — investigate most.

## Exclusivity

io.net removes other containers and blocks mixed workloads ([Support][7]). Router needs exclusive adapters
(io_net/pearl exclusive_gpu true; some subnets/API false). Orchestrator owns the worker.

## Inference sources as machines

DeepSeek/OpenRouter/Gemini/Mimo/Workers AI/cheap Qwen/local vLLM normalized to
{input/output cost, latency, quality, rate limit, context}. Miner flow: difficulty → reward →
cheapest passing model → submit → observe score → update. More scalable than sourcing GPUs.

## Adapters (v1, tiny)

sources/{salad,vast,runpod,hetzner,local,inference_api}.py + workloads/{xmr,pearl,quantus,bittensor,akash,custom}.py
+ core/{benchmark,economics,scheduler,worker}.py. Source: list_capacity/price/launch/stop/health.
Workload: requirements/benchmark/expected_revenue/launch/stop. edge = revenue − cost − risk. Highest wins.

## Benchmark cache (empirical, rebenched continuously)

3090: Pearl $2.72/d, QUAN $1.93/d, TSC $3.14/d, Bittensor SNx $5.22/d, inference $4.10/d.
EPYC 32c: XMR $0.81/d, CPU task $1.34/d. DeepSeek subnet X $7.80 per $1 API. Qwen $11.20 per $1.
RTX 5060 QUAN: 232 MH/s @96W ≈ $1.19/d rev, ~$0.95 profit.

## Thesis

Compute Yield Router over CPU/GPU/storage/intelligence → PoW/AI/marketplaces/agents/inference/batch.
Most asymmetric: intelligence→token (understand validator better than other miners) — the Bittensor game.
Miner = worker with externally-denominated reward.

[1]: https://app.salad.io/pricing
[2]: https://github.com/pearl-research-labs/pearl
[3]: https://arxiv.org/abs/2606.04819
[4]: https://www.bittensor.com/docs/guides/mining
[5]: https://akash.network/providers/
[6]: https://worker.io.net/
[7]: https://support.io.net/en/support/solutions/articles/156000093904-io-worker-automatically-deleting-other-docker-containers
