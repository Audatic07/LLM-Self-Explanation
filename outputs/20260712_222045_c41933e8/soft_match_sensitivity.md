# W6 Semantic Soft-Matching Sensitivity

**Run:** `outputs\20260712_222045_c41933e8`  |  **Instances:** 450
**Embedder:** en_core_web_lg==3.8.0 (static 300d vectors, 684830 keys/342918 vectors)  |  **τ (primary):** 0.8  |  **ε:** 0.1  |  **MC draws:** 1000 (seed 42)
**Vocab reconstruction match rate:** 99.8%

> Sensitivity analysis only (ECS_ROBUSTNESS_PLAN §5). Soft-matching credits cross-token cosine ≥ τ via 1-to-1 bipartite matching; the MC null accounts for the fact that soft-matching lifts chance agreement too. This BOUNDS how much of the rationale-pair depression is lexical, and is never the headline metric.

## Per-pair-type AJ (hard vs soft, τ=0.80)

| Pair | Kind | Hard AJ | Soft AJ | Δ (soft−hard) | n |
|---|---|---|---|---|---|
| H–R | E-R | +0.495 | +0.488 | -0.007 | 385 |
| RO–R | E-R | +0.492 | +0.493 | +0.001 | 407 |
| H–CF | E-P | +0.633 | +0.642 | +0.009 | 166 |
| RO–CF | E-P | +0.614 | +0.619 | +0.005 | 190 |
| R–CF | R-P | +0.433 | +0.433 | -0.001 | 154 |
| H–RO | E-E (ref) | +0.574 | +0.573 | -0.001 | 436 |

## Lexical-share of the E-P ↔ R-pair gap

- Hard: E-P pairs +0.623 vs R-pairs +0.474 → **gap +0.150**
- Soft (τ=0.80): E-P +0.630 vs R-pairs +0.471 → **gap +0.159**
- Soft-matching closes **-0.009** of the gap → **lexical share ≈ -6.2%** of the R-pair depression is attributable to lexical variation; the remainder is evidential disagreement.

## Complete-case ECS-adj: hard vs soft

| τ | Hard ECS-adj | Soft ECS-adj | n |
|---|---|---|---|
| 0.70 | +0.5062 | +0.5118 | 153 |
| 0.80 ← primary | +0.5062 | +0.5145 | 153 |
| 0.90 | +0.5062 | +0.5061 | 153 |
