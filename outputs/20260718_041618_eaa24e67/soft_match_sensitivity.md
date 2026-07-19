# W6 Semantic Soft-Matching Sensitivity

**Run:** `outputs\20260718_041618_eaa24e67`  |  **Instances:** 2400
**Embedder:** en_core_web_lg==3.8.0 (static 300d vectors, 684830 keys/342918 vectors)  |  **τ (primary):** 0.8  |  **ε:** 0.1  |  **MC draws:** 1000 (seed 42)
**Vocab reconstruction match rate:** 100.0%

> Sensitivity analysis only (ECS_ROBUSTNESS_PLAN §5). Soft-matching credits cross-token cosine ≥ τ via 1-to-1 bipartite matching; the MC null accounts for the fact that soft-matching lifts chance agreement too. This BOUNDS how much of the rationale-pair depression is lexical, and is never the headline metric.

## Per-pair-type AJ (hard vs soft, τ=0.80)

| Pair | Kind | Hard AJ | Soft AJ | Δ (soft−hard) | n |
|---|---|---|---|---|---|
| H–R | E-R | +0.495 | +0.492 | -0.003 | 1878 |
| RO–R | E-R | +0.424 | +0.422 | -0.002 | 2245 |
| H–CF | E-P | +0.555 | +0.556 | +0.001 | 1151 |
| RO–CF | E-P | +0.653 | +0.655 | +0.002 | 1334 |
| R–CF | R-P | +0.291 | +0.289 | -0.002 | 1180 |
| H–RO | E-E (ref) | +0.596 | +0.593 | -0.003 | 1970 |

## Lexical-share of the E-P ↔ R-pair gap

- Hard: E-P pairs +0.604 vs R-pairs +0.403 → **gap +0.200**
- Soft (τ=0.80): E-P +0.606 vs R-pairs +0.401 → **gap +0.204**
- Soft-matching closes **-0.004** of the gap → **lexical share ≈ -2.0%** of the R-pair depression is attributable to lexical variation; the remainder is evidential disagreement.

## Complete-case ECS-adj: hard vs soft

| τ | Hard ECS-adj | Soft ECS-adj | n |
|---|---|---|---|
| 0.70 | +0.4320 | +0.4242 | 1153 |
| 0.80 ← primary | +0.4320 | +0.4320 | 1153 |
| 0.90 | +0.4320 | +0.4319 | 1153 |
