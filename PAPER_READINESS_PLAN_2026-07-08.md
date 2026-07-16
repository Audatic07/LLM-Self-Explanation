# Paper-Readiness Plan — 2026-07-08

> **AUDIT UPDATE (2026-07-10).** `RESEARCH_AUDIT_2026-07-10.md` supersedes this document's
> claim-caveat map on six points: (F1) T3/numbers.json now carry the complete-case primary
> p's (regenerate assets; the a2 family is a labelled companion); (F3) the cross-model
> direction claim must quote `paired_contrast_aj_matched` (sst2-only separation at N=25);
> (F9) the consistency ladder is a point-estimate ordering with one CI-separated rung at
> N=25; (F11) confidence is descriptive-only and the prompt's anti-hedge line is removed;
> (F2/F12) erasure runs with an occurrence-matched control and an optional unknown-escape
> arm (both need the production re-run); (§G) the pre-registration adds a per-dataset
> co-primary family and pre-declares nova-ag_news underpowered. The audit's §7 limitations
> paragraph is the drop-in for the paper. The launch runbook below otherwise stands; add
> `scripts/run_weighted_null_sensitivity.py` to the post-run offline steps.
>
> **STRONG-ACCEPT MOVES (2026-07-13).** `STRONG_ACCEPT_MOVES_SPEC_2026-07-13.md`
> (pre-registered as plan §H) adds: disattenuated agreement (T9,
> `scripts/run_disattenuated_agreement.py` + per-model ablation ceilings), the CAD-IMDb
> fourth dataset arm (cells 9->12), and the counterfactual-simulatability bridge
> (`scripts/run_simulatability.py`, family (c)).

**Purpose:** the single document that takes the study from "pre-200-run fixes landed" to
"the 200-run's outputs are directly draftable into the paper." It consolidates: (1) the
executed P0.4 smoke results (all three PASS, run live on Bedrock today), (2) the
literature-verified dispositions of the ML-review findings
(`ML_REVIEW_prompts_methods_2026-07-08.md` v2), (3) the exact launch runbook, and (4) the
mapping from run artifacts to paper claims, with the caveat language each claim must carry.

**Inputs:** `PRE_200RUN_FIX_PLAN_2026-07-08.md` (all P0/P1/P2 items implemented 2026-07-08;
604 tests green), `ECS_ROBUSTNESS_PLAN_2026-07-05.md` + its 2026-07-08 amendment (§A–F),
ML review v2. Pilot of record: `outputs/20260707_223054_6c9bce68` (N=225).

---

## 1. P0.4 smoke results (executed live 2026-07-08) — GATE: **ALL PASS**

### 1.1 H long-input smoke — PASS (+ a finding)

206-word curated MNLI instance (`data/processed/mnli_curated.jsonl` max), all 3 models,
budget `12×206+200 = 2672` tokens. Evidence: `outputs/smoke_h_long_20260708/`.

| Model | Truncated | Salience entries (base/retest) | Parse | Retest Jaccard (T=0, identical prompt) |
|---|---|---|---|---|
| nova-pro | No | 205 / 204 | OK | **0.907** |
| qwen3-235b | No | 196 / 211 | OK | **0.822** |
| deepseek-v3 | No | 196 / 196 | OK | **0.907** |

The feared failure mode (malformed/truncated JSON on ~200-item salience lists →
length-correlated MNAR) does **not** occur; the length-proportional budget is sufficient
(max observed completion 1684 < 2672). **Finding:** at temperature 0 with byte-identical
prompts, **no model reproduced its own evidence set** (retest J 0.82–0.91, n=1 instance/model)
— consistent with batch-variant/MoE inference nondeterminism (Thinking Machines 2025
measured 80 distinct T=0 completions in 1,000 on Qwen3-235B). This single-handedly justifies
the R1 self-consistency ceiling (see §2).

### 1.2 Erasure smoke — PASS (first-ever execution of the fixed instrument)

6-record subset (2 per model, sst2+mnli mix), `--trials 3`, both operators. Evidence:
`outputs/smoke_erasure_20260708/`. Every record re-classified by its OWN model; CC3/CC4,
per-strategy, and random-control flips all computed (no None-storms); held-out CF
verification exercised on 4 records (all cross-model flips confirmed); Holm machinery ran
(p=None below the N=6 gate, as designed). Pre-registered family (b)'s instrument now has
post-P0.3 execution evidence.

### 1.3 Ablation smoke — PASS (first end-to-end completion of the fixed script)

`--sample-size 2` (3 datasets × 2 instances, nova-pro). Evidence:
`outputs/20260708_150744/ablations/` (`ablation_results.json` + robustness plot rendered —
the P0.2-fixed save-before-plot order held). Also validated the NEW self-consistency
instrument (§2): `self_consistency_aj_*` fields populate correctly (n=2 values are noise, as
expected from a smoke; the 50-instance run is the measurement).

---

## 2. New instrument landed today: the self-consistency ceiling (review R1)

`scripts/run_ablations.py::compute_self_consistency_aj` — same-strategy AJ(base, alt) over a
support-closed instance vocabulary, persisted per strategy in `ablation_results.json`
(`self_consistency_aj_mean/n/values`, `n_degenerate`, `n_missing`); 5 unit tests in
`tests/test_ablation_self_consistency.py`. Zero extra API cost (the paraphrase ablation
already collects both elicitations).

**Why it is the paper's denominator:** cross-strategy ECS-adj (+0.44 complete-case) is
interpretable only against how much ONE strategy agrees with itself under trivial
re-elicitation. The pilot per-pair AJ profile already sketches the ladder the paper should
report:

| Rung | Agreement (pilot AJ) |
|---|---|
| Same prompt, same model, T=0 retest (H, smoke, raw J, n=1/model) | ~0.82–0.91 |
| Same paradigm, different method (H–RO; excluded from ECS) | **+0.64** |
| Extraction ↔ perturbation (H–CF / RO–CF) | +0.64 / +0.52 |
| Extraction ↔ rationalization (H–R / RO–R) | +0.45 / +0.48 |
| Rationalization ↔ perturbation (R–CF) | **+0.29** |

Agreement decays monotonically with paradigm distance — that is the paper's central figure
(see §6). The 50-instance ablation fills in the paraphrase-ceiling rung per strategy.

---

## 3. Review-item dispositions (literature-verified; see ML review v2 for citations)

| Item | Disposition | When | Blocks launch? |
|---|---|---|---|
| **R1** test–retest ceiling | Instrument **implemented + smoked**; measure at 50-inst scale via the ablation arm; report ECS-adj as fraction of ceiling. Optional: identical-prompt retest arm (~200 calls) to split decoding noise from paraphrase brittleness | with post-run ablation | **No** |
| **R2** label-anchor / post-hoc rationalization | Framing: state "consistency of label-conditioned rationalizations" as a first-class limitation (Turpin 2023; Wiegreffe 2021); optional no-label control on a subset if budget allows | paper draft (+optional arm) | No |
| **R3** CF flip-set ≠ attribution support-set | Framing: present E-P/R-P as **attribution↔intervention divergence** (Mothilal et al. 2021 necessity/sufficiency), with R–CF +0.29 and CF quantization (median set 2; 36% ≤1 token) as the measured datapoints | paper draft | No |
| **R4** gold-rationale anchor (**corrected: e-SNLI = SNLI only, NOT MNLI**) | Recommended annex: ~50-instance SNLI side-arm × 3 models (~1.3k calls) scored against e-SNLI highlights; else state plainly no gold anchor exists for the three datasets | post-200-run annex | No |
| **R5** R-pair depression / W6 | **Gate FIRED** (R-pairs +0.46 vs +0.58 CF-pairs / +0.64 H–RO): run the pre-registered soft-match sensitivity (pinned local embedder, cosine τ=0.8, plan §5) offline on the 200-run evidence; bounds lexical-vs-evidential share of the E-R/R-P gap | post-run, offline | No |
| **R6** confidence RQ dead at T=0 | Demote to a one-line null ("non-informative under greedy decoding, consistent with Xiong et al. 2024"); keep τ-b table in appendix only | paper draft | No |
| **R7** single-cue datasets | Report ECS-adj difficulty strata (length strata from P1.2 + vocab-size association); harder/longer task (ERASER Movies — would also serve R4b) is future work | paper draft / future | No |
| **R8** CF-MNAR selection | Lead with availability-vs-complete dual reporting (P0.1 structure); state selection direction explicitly | paper draft | No |

**Do-not-do list (deliberate):** do NOT change any elicitation prompt (R5's "uncap R" idea
is future-work — the prompt manifest freeze and pilot comparability outweigh it); do NOT
adopt soft-matching into the primary metric (sensitivity only, per plan §5); do NOT
reinterpret the raw cross-model contrast (AJ scale is the headline per P0.2).

---

## 4. Remaining pre-launch checklist (in order)

1. **Commit** the working tree (fix-plan implementation + smokes evidence + this plan +
   review v2). Suite green: 609 expected (604 + 5 self-consistency tests). *(Only step
   requiring the user; nothing else is uncommitted-state-dependent.)*
2. Working tree clean → launch snapshot will record `git_dirty: false`.
3. Credentials: `AWS_BEARER_TOKEN_BEDROCK` + `AWS_REGION=eu-north-1` are in gitignored
   `.env` (verified live today on all 3 models). **Never commit `.env`; rotate the key after
   the campaign.**
4. Re-verify config: `sample_size: 200` ×3 datasets ×3 models (already set); prompts frozen
   (manifest hashing is per-run).

## 5. Execution runbook (after §4)

| # | Step | Command | Est. calls / wall-clock |
|---|---|---|---|
| 1 | Main collection | `python scripts/run_experiment.py` | ~16k / 4–6h (pilot retry rate 16.8%) |
| 2 | If interrupted | `python scripts/resume_experiment.py <run_dir_name>` | — |
| 3 | Erasure pass (family (b)) | `python scripts/run_validity_tests.py --results-dir outputs/<run>` | ~30–35k / ~9h |
| 4 | Ablation + self-consistency ceiling | `python scripts/run_ablations.py` (50/dataset, nova-pro) | ~1.4k / ~1h |
| 5 | Offline: W6 soft-match sensitivity (R5; τ=0.8 pre-registered) | new offline script over `<run>/instance_results.jsonl` | 0 API |
| 6 | Offline: verify report tables render from real data (complete-case (a) primary, (a2) sensitivity, AJ cross-model, free-CF AJ, ECS-adj strata) | inspect `outputs/<run>/report.md` | 0 API |
| 7 | Paper assets | `python scripts/generate_paper_assets.py` (per `PAPER_DATA_VIZ_PLAN_2026-07-07.md`) | 0 API |
| 8 | (Annex, optional) SNLI/e-SNLI side-arm (R4a) | curate 50 SNLI + run | ~1.3k |

Ordering rationale: erasure before ablation (it is the pre-registered family (b) and the
long pole); the W6 and ceiling analyses are offline and can run during erasure.

## 6. Paper drafting map (artifact → claim → required caveat)

| Paper element | Source artifact | Claim it supports | Mandatory caveat (from review) |
|---|---|---|---|
| **Headline:** complete-case ECS-adj per cell + family (a) Holm p | `report.md` "COMPLETE CASES (PRIMARY)" table | Cross-paradigm agreement exceeds chance given set-size geometry | Label-conditioned rationalizations (R2); complete-case is CF-selected (R8); negative cells ≠ below-chance magnitude (P1.4 floor note) |
| **Denominator:** self-consistency ceiling per strategy | `ablations/ablation_results.json` `self_consistency_aj_*` | ECS-adj as a fraction of the paraphrase-stability ceiling; T=0 retest J 0.82–0.91 shows single-draw noise | n and per-strategy missingness; one model for the ceiling arm |
| **Central figure:** the consistency ladder (retest → H–RO → E-P → E-R → R-P) | §2 table recomputed on 200-run + smoke | Agreement decays with paradigm distance | R–CF rung is attribution↔intervention divergence (R3), partly lexical pending W6 (R5) |
| Cross-model contrast (AJ headline; raw demoted) | `cross_model_agreement.json` + report §Cross-Model | Same-strategy cross-model agreement vs within-model cross-paradigm — task-prior direction, stated only as strongly as AJ CIs allow | Raw version overstates ~2× (P0.2); expect CI tightening at N=200 |
| MNAR robustness | free-CF AJ row (complete +0.40 at pilot) + availability/complete dual tables | Conclusions survive removing the minimal-edit gate | Free-CF still flip-gated (R8) |
| Erasure axis (family (b)) | `aggregate_erasure.json` per model per operator | Stated-vs-revealed sensitivity: CC-erasure vs random control | Second consistency axis, NOT faithfulness ground truth; operator choice reported both ways |
| Lexical-variation bound | W6 soft-match output (post-run) | Share of E-R/R-P gap attributable to synonymy | Sensitivity only; τ=0.8 pre-registered |
| Confidence (appendix, one line) | report τ-b table | Null: verbalized confidence non-informative at T=0 (109/225 = 0.95) | Consistent with Xiong et al. 2024; not a calibration finding |
| Related work | ML review v2 §Related-work | Position against Parcalabescu & Frank 2024; arXiv:2407.14487; 2502.18156; 2506.07523 | — |

**Framing sentence the paper should lead with** (synthesizes R1–R3 honestly): *"We measure
the consistency of an LLM's label-conditioned self-explanations across three explanation
paradigms, relative to (i) chance and ceiling given each pair's evidence-set geometry and
(ii) the model's own re-elicitation stability — and find agreement decays with paradigm
distance, with the attribution↔intervention gap the largest and partly definitional."*

## 7. What this plan does NOT claim (carried forward + extended)

- The 200-run results are not pre-ordained: three complete-case cells will land at N≈16–24
  and stay wide; CF-driven MNAR remains the structural limitation, mitigated — not
  eliminated — by the free-CF AJ sensitivity and dual reporting.
- The self-consistency ceiling from the ablation arm is a *paraphrase* ceiling on one model;
  the identical-prompt retest datapoint is n=1 instance per model until the optional retest
  arm runs.
- No claim of acceptance anywhere. The claim is: every headline number will be reproducible
  from raw artifacts, tested on its own estimand's population, read against a measured
  noise ceiling, and accompanied by the caveat a competent reviewer would otherwise write
  themselves.
