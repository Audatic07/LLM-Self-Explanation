# W6 Semantic Soft-Matching Sensitivity

**Run:** `outputs\20260708_191145_0fe76508`  |  **Instances:** 225
**Embedder:** en_core_web_lg==3.8.0 (static 300d vectors, 684830 keys/342918 vectors)  |  **τ (primary):** 0.8  |  **ε:** 0.1  |  **MC draws:** 1000 (seed 42)
**Vocab reconstruction match rate:** 100.0%

> Sensitivity analysis only (ECS_ROBUSTNESS_PLAN §5). Soft-matching credits cross-token cosine ≥ τ via 1-to-1 bipartite matching; the MC null accounts for the fact that soft-matching lifts chance agreement too. This BOUNDS how much of the rationale-pair depression is lexical, and is never the headline metric.

## Per-pair-type AJ (hard vs soft, τ=0.80)

| Pair | Kind | Hard AJ | Soft AJ | Δ (soft−hard) | n |
|---|---|---|---|---|---|
| H–R | E-R | +0.457 | +0.452 | -0.006 | 201 |
| RO–R | E-R | +0.498 | +0.491 | -0.007 | 202 |
| H–CF | E-P | +0.616 | +0.641 | +0.025 | 69 |
| RO–CF | E-P | +0.565 | +0.574 | +0.008 | 84 |
| R–CF | R-P | +0.382 | +0.407 | +0.024 | 69 |
| H–RO | E-E (ref) | +0.611 | +0.612 | +0.001 | 216 |

## Lexical-share of the E-P ↔ R-pair gap

- Hard: E-P pairs +0.591 vs R-pairs +0.446 → **gap +0.145**
- Soft (τ=0.80): E-P +0.607 vs R-pairs +0.450 → **gap +0.158**
- Soft-matching closes **-0.013** of the gap → **lexical share ≈ -8.9%** of the R-pair depression is attributable to lexical variation; the remainder is evidential disagreement.

## Complete-case ECS-adj: hard vs soft

| τ | Hard ECS-adj | Soft ECS-adj | n |
|---|---|---|---|
| 0.70 | +0.4867 | +0.5082 | 68 |
| 0.80 ← primary | +0.4867 | +0.5029 | 68 |
| 0.90 | +0.4867 | +0.4862 | 68 |
