"""Deterministic UK phone-number candidate feature/scoring helpers.

No network calls. Feed this module real Telnyx candidate objects after hard-gate filtering.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import re
from collections import Counter

def digits(s: str) -> str:
    return re.sub(r"\D", "", s)

def uk_national_digits(e164: str) -> str:
    d = digits(e164)
    if d.startswith("44"):
        return "0" + d[2:]
    return d

def entropy_score(s: str) -> float:
    """0..1 where lower raw entropy -> higher memorability contribution."""
    if not s:
        return 0.0
    c = Counter(s)
    n = len(s)
    h = -sum((v/n)*math.log2(v/n) for v in c.values())
    max_h = math.log2(min(10, n)) if n > 1 else 1
    return max(0.0, 1.0 - h/max_h) if max_h else 1.0

def longest_run(s: str) -> int:
    if not s:
        return 0
    best = cur = 1
    for a,b in zip(s, s[1:]):
        cur = cur + 1 if a == b else 1
        best = max(best, cur)
    return best

def adjacent_equal_count(s: str) -> int:
    return sum(a == b for a,b in zip(s, s[1:]))

def palindrome_ratio(s: str) -> float:
    if not s:
        return 0.0
    return sum(a == b for a,b in zip(s, reversed(s))) / len(s)

def sequence_run(s: str) -> int:
    if not s:
        return 0
    best = cur = 1
    for a,b in zip(s, s[1:]):
        if (int(b)-int(a)) in (1,-1):
            cur += 1
            best = max(best, cur)
        else:
            cur = 1
    return best

def repeated_block_score(s: str) -> float:
    """Detect ABAB, ABCABC etc. Returns 0..1."""
    n = len(s)
    best = 0.0
    for size in range(1, n//2 + 1):
        for start in range(0, n - 2*size + 1):
            a = s[start:start+size]
            b = s[start+size:start+2*size]
            if a == b:
                best = max(best, min(1.0, (2*size)/max(4,n)))
    return best

def pair_structure_score(s: str) -> float:
    """Rewards strings naturally chunkable into identical-digit pairs: 88 22 44."""
    if len(s) < 4:
        return 0.0
    pairs = [s[i:i+2] for i in range(0, len(s)-1, 2)]
    identical = sum(len(p)==2 and p[0]==p[1] for p in pairs)
    return identical / max(1, len(pairs))

def memorability_features(number: str, tail_len: int = 6) -> dict:
    s = uk_national_digits(number)
    tail = s[-tail_len:] if len(s) >= tail_len else s
    return {
        "tail": tail,
        "longest_run": longest_run(tail),
        "adjacent_equal_count": adjacent_equal_count(tail),
        "palindrome_ratio": palindrome_ratio(tail),
        "sequence_run": sequence_run(tail),
        "repeated_block_score": repeated_block_score(tail),
        "pair_structure_score": pair_structure_score(tail),
        "low_entropy_score": entropy_score(tail),
        "unique_digit_count": len(set(tail)),
    }

def memorability_score(number: str) -> float:
    f = memorability_features(number)
    n = max(1, len(f["tail"]))
    raw = (
        0.18 * min(1, f["adjacent_equal_count"]/3)
        + 0.16 * min(1, max(0,f["longest_run"]-1)/3)
        + 0.18 * f["repeated_block_score"]
        + 0.18 * f["pair_structure_score"]
        + 0.10 * f["palindrome_ratio"]
        + 0.08 * min(1, max(0,f["sequence_run"]-1)/3)
        + 0.12 * f["low_entropy_score"]
    )
    return round(100*raw, 2)

def estimated_chunk_count(number: str) -> int:
    """Crude speech proxy. Repeated pairs/blocks reduce effective chunk count."""
    tail = memorability_features(number)["tail"]
    if not tail:
        return 99
    # Greedy chunks: identical pair, repeated 2/3 digit blocks, otherwise digit.
    i, chunks = 0, 0
    while i < len(tail):
        if i+4 <= len(tail) and tail[i:i+2] == tail[i+2:i+4]:
            chunks += 1; i += 4; continue
        if i+2 <= len(tail) and tail[i] == tail[i+1]:
            chunks += 1; i += 2; continue
        chunks += 1; i += 1
    return chunks

def spoken_score(number: str) -> float:
    tail = memorability_features(number)["tail"]
    if not tail:
        return 0.0
    chunks = estimated_chunk_count(number)
    repeats = adjacent_equal_count(tail)
    block = repeated_block_score(tail)
    score = 100 - max(0, chunks-2)*12 + min(15, repeats*4) + block*15
    return round(max(0,min(100,score)),2)

def total_candidate_score(*, business_fit: float, capability_ops: float,
                          number: str, economics: float, future_fit: float) -> dict:
    """Inputs except number are 0..100. Returns weighted 0..100."""
    m = memorability_score(number)
    s = spoken_score(number)
    components = {
        "business_fit": business_fit,
        "capability_ops": capability_ops,
        "memorability": m,
        "spoken_usability": s,
        "economics": economics,
        "future_fit": future_fit,
    }
    weights = {
        "business_fit": .30,
        "capability_ops": .20,
        "memorability": .20,
        "spoken_usability": .15,
        "economics": .10,
        "future_fit": .05,
    }
    total = sum(components[k]*weights[k] for k in weights)
    return {"score": round(total,2), "components": components, "features": memorability_features(number)}
