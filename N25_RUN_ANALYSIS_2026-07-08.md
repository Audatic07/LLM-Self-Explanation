# N=25 End-to-End Run — Full Analysis (2026-07-08)

> **AUDIT CORRECTIONS (2026-07-10, RESEARCH_AUDIT_2026-07-10.md).** All numbers below were
> independently recomputed bit-exact (audit V1–V4); the following READINGS are corrected:
> 1. **Per-cell significance (F1):** the paper assets quoted the available-component (a2)
>    family's p-values as if they were the primary test. The pre-registered COMPLETE-CASE
>    family's true N=25 picture: significant after Holm in deepseek-sst2 (.0006),
>    nova-sst2 (.016), qwen-sst2 (.016), deepseek-ag_news (.026); NOT significant in
>    deepseek-mnli (.060) and qwen-mnli (.079); untestable (n<6) in the other 3 cells.
>    `generate_paper_assets.py` is fixed; regenerate assets before quoting T3/numbers.json.
> 2. **"Decays monotonically with paradigm distance" (F9):** at N=25 only the top-vs-bottom
>    rung is CI-separated (E-P − R-P = +0.208 [+0.056,+0.361]); E-P vs E-R and E-R vs R-P are
>    not. Present the ladder as a point-estimate ordering until N=200.
> 3. **W6 (F7/F8):** the original artifact used a 34×-pruned vector table (antonyms at
>    cosine 1.0) and a correlated MC null (±0.03 seed swing). Regenerated with
>    en_core_web_lg + decorrelated 1000-draw null: CF-pairs gain from soft matching
>    (+0.02), R-pairs stay flat — lexical share of the E-P↔R gap is −0.12/−0.09/+0.01 at
>    τ=0.7/0.8/0.9. The §"evidential, not lexical" conclusion STRENGTHENS.
> 4. **Cross-model contrast (F3):** "cross-model exceeds within-model in all 3 datasets"
>    holds only under mixed composition; the strategy-matched contrast is CI-separated in
>    sst2 only (+0.230 [+0.042,+0.448]). Quote `paired_contrast_aj_matched`.
> 5. **Erasure (F2):** the type-matched random control gave CC3 a +14.5% destroyed-token
>    advantage (ag_news/mnli); the gap survives the no-advantage subsample under both
>    operators (mask +0.098 p=4e-4; delete +0.133 p=1e-4), so the finding stands; the
>    occurrence-matched control is now default for future runs.
> 6. **Confidence (F11/R6):** descriptively reported only; the unsourced anti-hedge line was
>    removed from the prompt post-N=25.

**What this document is.** A complete read of everything the study produces end-to-end, run at
N=25 per model×dataset cell as a full-pipeline rehearsal of the 200-run: main collection →
erasure validity pass → ablation + self-consistency ceiling → W6 soft-match sensitivity →
paper assets (figures + tables + headline numbers). It also records the code that was
implemented this session to close the last open item in `PAPER_READINESS_PLAN_2026-07-08.md`.

**One-line verdict.** The pipeline ran clean end-to-end on live Bedrock and every headline the
paper needs is present, reproducible from raw artifacts, and pointing the same direction as the
N=225 pilot: cross-paradigm agreement is **above chance-and-ceiling** (complete-case ECS-adj
pooled **+0.487**, positive in all 9 cells), it **decays monotonically with paradigm distance**,
the consensus evidence is **causally load-bearing** (erasure family (b) significant for all
3 models × both operators), and the depressed rationale-pair agreement is **evidential, not
lexical** (W6 soft-match closes ≈0% of the gap at τ=0.8). N=25 is under-powered in the
CF-scarce cells exactly as predicted; nothing here is a blocker.

---

## 0. Provenance

| Item | Value |
|---|---|
| Main run dir | `outputs/20260708_191145_0fe76508` (run id `0fe76508`, seed 42) |
| Ablation dir | `outputs/20260708_220033/ablations/` |
| Scale | 25 instances × 3 datasets × 3 models = **225 instances** (via `--sample-size 25`; production config left at 200) |
| Models | nova-pro, qwen3-235b, deepseek-v3 (Bedrock eu-north-1, bearer-token auth) |
| Collection cost | 2,346 API requests, 14.1% throttle-retry rate, 11.87 s/instance avg (pilot was 16.8%) |
| Code branch | `w6-softmatch-n25` (4 commits this session) |
| Test suite | **620 passed** (609 prior + 11 new soft-match) |
| Config | `sample_size` overridden on the CLI only; normalization v3.0 (lemmatized shared token space); ECS-adj ε=0.10; erasure trials=5, operators mask+delete; ablation subset=25, nova-pro |

**Note on the collection exit code.** The `run_experiment.py` process completed all 225
instances and wrote every artifact; a non-zero shell exit came only from a `tee` redirect to a
non-writable path (in a pipe the exit status is `tee`'s). The experiment itself succeeded — 225
lines in `instance_results.jsonl`, full `report.md`, `aggregate_metrics.json`,
`cross_model_agreement.json`.

---

## 1. What was implemented this session

The pre-plan claimed all P0/P1/P2 items landed; an audit confirmed that and found **one unbuilt
runbook item** plus two pipeline defects surfaced by actually running everything.

### 1.1 W6 semantic soft-matching sensitivity — the last unbuilt item (review R5)

`PAPER_READINESS_PLAN §5 step 5` listed a "new offline script" for the W6 soft-match
sensitivity that did not exist. Built:

- **`src/metrics/soft_match.py`** — `SoftMatcher`: soft-Jaccard via **maximum-weight bipartite
  matching** (`scipy.optimize.linear_sum_assignment`) over a **pinned offline GloVe embedder**
  (`en_core_web_md==3.8.0`, 300-d static vectors), crediting a matched pair its cosine **only
  above the pre-registered τ = 0.8**; a **Monte-Carlo chance null** (soft-matching lifts chance
  agreement too, so the exact hypergeometric form is intractable — the plan permits MC with a
  reported SE for a sensitivity); the same ceiling `J_max = min/max` (bipartite matching is
  1-to-1) and the same paradigm-balanced ECS-adj aggregation as the primary metric. The embedder
  is injectable, so the estimator is testable without spaCy, and it **provably reduces to the
  hard metric** when nothing soft-matches.
- **`scripts/run_soft_match_sensitivity.py`** — offline CLI (0 API) over a run's
  `instance_results.jsonl`; reconstructs the instance vocabulary via the exact production path
  (validated against the stored `vocab_size`) and writes `soft_match_sensitivity.{json,md}`.
- **`tests/test_soft_match.py`** — 11 unit tests (reduction property, τ gating, 1-to-1 bound,
  null monotonicity, degeneracy guard, aggregation equivalence).

### 1.2 Two pipeline defects found by running it

- **Test-suite collection break (blocking).** An unrelated `scripts` package in site-packages
  shadowed the repo's `scripts/` during pytest import (PEP 420: a regular package elsewhere on
  `sys.path` beats a namespace-portion directory), so `test_ablation_self_consistency.py`'s
  `from scripts.run_ablations import …` failed. Fixed by adding **`scripts/__init__.py`** (scripts
  still run in script mode; unaffected).
- **F8 figure never rendered.** `generate_paper_assets.py::fig_F8` required a pre-flattened
  `Variation/ECS_delta` frame, but `run_ablations.py` writes
  `{dataset}_prompt → {strategy}_alt → {deltas:[…]}` — so F8 was **silently skipped on every real
  ablation output**. Fixed to parse the native schema (kept the flat-frame fast path).

All three changes are committed on `w6-softmatch-n25`.

---

## 2. Main collection — the headline agreement result

### 2.1 Coverage (and the structural MNAR that shapes everything downstream)

| Strategy | Valid / Total | Rate |
|---|---|---|
| Highlighting (H) | 223/225 | 99% |
| Rationale (R) | 216/225 | 96% |
| Counterfactual (CF) | 89/225 | **40%** |
| Rank Ordering (RO) | 221/225 | 98% |

CF validity is 40% (pilot: 43%) — the minimal-edit-gate MNAR is the study's defining structural
limitation (review R8). It is why the **complete-case** population (all 4 strategies valid) is
only 83/225, and why the CF-heavy multiclass cells (mnli, ag_news) land below the N=6 test gate.
The design's answer to this is dual reporting (complete-case primary + available-component
sensitivity) plus the free-CF AJ robustness check (§2.4).

### 2.2 Primary estimand — complete-case ECS-adj, per cell (pre-registered test (a))

Chance- and ceiling-adjusted, paradigm-balanced ECS-adj over instances with all three paradigm
components defined; one-sided sign-flip permutation, Holm-corrected across the run's cells.

| Model | Dataset | N (complete) | Mean ECS-adj | p (Holm) |
|---|---|---|---|---|
| nova-pro | sst2 | 8 | **+0.6133** | 0.0009 |
| qwen3-235b | sst2 | 13 | **+0.4603** | 0.0104 |
| deepseek-v3 | sst2 | 17 | **+0.6708** | 0.0009 |
| deepseek-v3 | mnli | 8 | **+0.4357** | 0.0009 |
| qwen3-235b | mnli | 6 | +0.3182 | 0.0009 |
| deepseek-v3 | ag_news | 7 | +0.3715 | 0.0009 |
| nova-pro | mnli | 3 | +0.3328 | below N=6 gate |
| qwen3-235b | ag_news | 4 | +0.2753 | below N=6 gate |
| nova-pro | ag_news | 2 | +0.3528 | below N=6 gate |

- **Pooled complete-case: +0.4867 (n=68)** — recomputed directly from raw `ecs_adj_complete`
  instances, matches the report and `numbers.json` exactly.
- **All 9 cells positive** (+0.28 to +0.67); every cell that clears the N=6 gate is Holm-
  significant. The three cells that fall below the gate (nova mnli, qwen ag_news, nova ag_news)
  are exactly the ones the fix-plan projected would be thin at N=25 — reported as estimates, not
  tested. **This is the expected, honest N=25 outcome.**

### 2.3 Available-component sensitivity (test family a2)

The same test on the larger available-component population (any elicitable paradigm pairs):
per-cell N=23–25, means **+0.16 to +0.24**, all Holm p ≈ 0.0009–0.0012 — uniformly significant.
Pooled available-component mean **+0.4923 (n=215)**. This is the "above-chance agreement across
whichever paradigm pairs were elicitable" statement; it is deliberately **not** the headline
(the headline is the complete-case estimand, which matches its own test population).

### 2.4 MNAR robustness — free-CF ECS-adj (P0.3, primary scale)

Substituting the unconstrained free-CF rewrite (`cf_contrast_tokens`, far higher validity than
the minimal-edit gate) for CF's evidence and re-scoring with the AJ estimator:

- **complete-case +0.4394 (N=129)**, available-component **+0.4292 (N=185)** — both positive,
  and complete-case is essentially unchanged from the minimal-CF +0.4867. **The primary
  conclusion survives removing the minimal-edit gate**, which is the whole point: the agreement
  is not an artifact of selecting only easy-to-flip instances. (Legacy flat-ECS free-CF form
  also reported: 0.3583, N=185.)

### 2.5 The consistency ladder — the paper's central figure (paradigm-distance decay)

Per-pair adjusted-Jaccard means (from the W6 hard column, which recomputes AJ on the exact null):

| Rung | Pair(s) | Mean AJ | n |
|---|---|---|---|
| Same-paradigm reference (excluded from ECS) | H–RO | **+0.611** | 216 |
| Extraction ↔ perturbation (E-P) | H–CF, RO–CF | +0.591 | 70 / 84 |
| Extraction ↔ rationalization (E-R) | H–R, RO–R | +0.457 / +0.498 | 199 |
| Rationalization ↔ perturbation (R-P) | R–CF | **+0.382** | 65 |

Agreement decays monotonically as the paradigms get further apart, and the **R–CF rung is the
lowest** — the attribution↔intervention gap (review R3: necessity vs sufficiency, Mothilal et
al. 2021). This is a structural property, not a model failure, and its *size* is the finding.

### 2.6 Cross-model contrast (task prior vs privileged self-knowledge) — on the fair AJ scale

Paired within-instance Δ = (cross-model same-strategy AJ) − (within-model cross-paradigm
ECS-adj), bootstrapped:

| Dataset | Mean Δ (AJ) | 95% CI |
|---|---|---|
| ag_news | +0.1218 | [+0.0197, +0.2260] |
| mnli | +0.1178 | [+0.0028, +0.2490] |
| sst2 | +0.1689 | [+0.0016, +0.3563] |

Cross-model same-strategy agreement exceeds within-model cross-paradigm agreement in **all three
datasets, CI entirely above 0** — evidence for a **generic task prior shared across models** over
model-specific privileged self-knowledge. This is reported on the P0.2-corrected AJ scale; the
raw-Jaccard companion (retained, demoted) overstates the gap ~2×. sst2's lower CI bound
(+0.0016) is barely above 0 — expected to tighten decisively at N=200.

### 2.7 Confound checks (P1.2 strata) and the dead confidence variable (R6)

- **Brevity confound removed by the adjustment.** Under raw ECS, short inputs score highest
  (0.4198 short vs 0.3648 long) — the classic brevity artifact. Under **ECS-adj the gradient
  reverses**: short +0.4246 < medium +0.5175 < long +0.5734. Same for vocabulary: normal-vocab
  +0.5264 > short-vocab +0.4776 under ECS-adj (raw ECS had it backwards). The adjustment does
  exactly what it was designed to do.
- **Confidence is non-informative at T=0 (R6):** 109/225 answers are exactly 0.95 (48%); top-5
  values (0.95/0.98/0.85/1.0/0.9) cover the sample. This replicates the pilot and Xiong et al.
  (2024). It stays a one-line appendix null, not a calibration finding.

---

## 3. Erasure validity pass — the second consistency axis (pre-registered family (b))

Each record re-classified by **its own model**; erasing the top-3 consensus tokens (CC3) is
compared against erasing same-size **random** token sets; one-sided sign-flip, Holm-corrected
across operators; per-model is the primary reporting unit. Artifact:
`outputs/20260708_191145_0fe76508/aggregate_erasure.json`.

| Model | n | CC3 flip (mask/del) | Random | CC3−random gap (mask/del) | p (Holm) | Held-out CF verify |
|---|---|---|---|---|---|---|
| deepseek-v3 | 75 | 0.22 / 0.23 | 0.09 | +0.135 / +0.145 | 0.0018 | 93% (37/40) |
| nova-pro | 75 | 0.27 / 0.23 | 0.11 | +0.159 / +0.139 | 0.0024 | 100% (21/21) |
| qwen3-235b | 75 | 0.21 / 0.23 | 0.12 | +0.094 / +0.115 | 0.0234 | 96% (27/28) |

**Reading:** erasing the consensus evidence flips the prediction **significantly more than random
erasure of the same size, for all three models and both operators** (all Holm-significant). The
stated cross-paradigm consensus is **causally load-bearing**, not decorative. The held-out CF
verification (a *different* model re-checks each CF flip) confirms 93–100% of flips — the
perturbation construct is robust to judge choice. Both operators (mask and delete) agree in
direction, so the ICE-2026 "operator choice flips conclusions" risk does not bite here.

This is framed as a **second consistency axis (stated-vs-revealed input sensitivity), explicitly
not a faithfulness ground truth** — the `_notes` field in the artifact says so.

---

## 4. Ablation + the self-consistency ceiling (review R1 — the denominator)

Artifact: `outputs/20260708_220033/ablations/ablation_results.json` (+ `robustness_analysis.png`,
per-dataset `prompt_ablation_*.json`). One model (nova-pro), 25 instances/dataset, each strategy
elicited under a second (paraphrased) prompt wording.

### 4.1 Prompt-paraphrase robustness (is the ECS metric stable to rewording?)

Per-instance ECS deltas (baseline vs `*_alt` wording) are centred near 0 — the metric is robust
to prompt rewording — **except highlighting on MNLI** (mean Δ +0.184; every other cell |Δ| ≤
0.09). Highlighting a ~200-item salience list on long MNLI inputs is the one paraphrase-brittle
spot, which the self-consistency ceiling independently confirms below.

### 4.2 The self-consistency ceiling — ECS-adj's missing denominator (R1)

Same-strategy AJ between the base and paraphrased elicitations, per strategy (the paraphrase-
stability ceiling against which cross-strategy ECS-adj must be read):

| Strategy | Self-consistency AJ (pooled) | Per-dataset (sst2 / mnli / ag_news) |
|---|---|---|
| R (rationale) | **+0.821** | 0.693 / 0.888 / 0.882 |
| RO (rank order) | +0.465 | 0.681 / 0.177 / 0.536 |
| H (highlighting) | +0.211 | 0.550 / **−0.279** / 0.362 |
| CF (counterfactual) | +0.088 | 0.327 / −0.118 / 0.055 |

**This is the single most important interpretive result for the paper**, and it is nuanced:

- **R is highly self-consistent (+0.82).** So R-*pairs* at +0.44–0.46 (E-R) are genuinely **below
  R's own re-elicitation stability** → the extraction↔rationalization gap is a **real divergence
  between paradigms**, not R being noisy. This is the "interesting result" branch of R1.
- **H and CF have low, noisy ceilings (+0.21, +0.09; negative on MNLI).** Highlighting and
  counterfactuals barely reproduce themselves under a reworded prompt. Cross-strategy agreement
  involving H/CF must therefore be read as *comparable to or above* their own within-strategy
  paraphrase stability — a caution the paper must state, not bury. It also localizes *where* the
  elicitation noise lives (graded-salience and minimal-edit outputs), consistent with the T=0
  retest finding (H retest J 0.82–0.91 in the 07-08 smoke) and MoE nondeterminism.
- **N=25 caveat:** these ceilings rest on 5–24 paired instances (CF as low as n=5); they are
  estimates with wide sampling error. The 50-instance production ablation will stabilize them.

**Bottom line for R1:** the ceiling instrument works and populates cleanly; the paper should
report ECS-adj *next to* the per-strategy ceiling and state the R-pair result as a fraction of R's
achievable ceiling (genuinely divergent) while flagging that H/CF ceilings are too noisy at this
N to anchor firmly.

---

## 5. W6 semantic soft-matching sensitivity (review R5) — is the R-pair gap lexical?

Artifact: `outputs/20260708_191145_0fe76508/soft_match_sensitivity.{json,md}`. Embedder
`en_core_web_md==3.8.0`, τ=0.8, ε=0.10, 200 MC draws, seed 42. **Vocabulary reconstruction match
rate: 100.0%** (the curated N=25 set reconstructs the stored vocab exactly — a strong cross-check;
the hard complete-case ECS-adj it recomputes is +0.4867, matching §2.2).

| Pair | Kind | Hard AJ | Soft AJ (τ=0.8) | Δ (soft−hard) | n |
|---|---|---|---|---|---|
| H–R | E-R | +0.457 | +0.430 | −0.028 | 199 |
| RO–R | E-R | +0.498 | +0.480 | −0.019 | 199 |
| H–CF | E-P | +0.616 | +0.608 | −0.008 | 70 |
| RO–CF | E-P | +0.565 | +0.537 | −0.028 | 84 |
| R–CF | R-P | +0.382 | +0.363 | −0.019 | 65 |
| H–RO | E-E (ref) | +0.611 | +0.607 | −0.004 | 216 |

**Lexical-share of the E-P↔R-pair gap:** hard gap +0.145 (E-P +0.591 vs R-pairs +0.446); soft gap
+0.149. Soft-matching **closes −0.004** of the gap → **lexical share ≈ −2.5%**. Because the
Monte-Carlo null correctly rises under soft-matching, crediting synonyms at τ=0.8 does **not**
lift R-pairs toward the E-P pairs — if anything it slightly widens the gap.

**Interpretation:** the depressed rationale-pair agreement is **evidential, not an artifact of
"terrible"≠"awful" lexical variation**. This is the honest, and stronger, outcome for the paper —
it defends R3 (the attribution↔intervention divergence is real) against the obvious "your exact-
token Jaccard just penalizes synonyms" objection. Complete-case ECS-adj is essentially invariant
to soft-matching (+0.4867 hard → +0.4744 soft at τ=0.8; τ-sweep 0.7/0.8/0.9 all within 0.002),
confirming the primary metric is not lexically fragile. (The pilot showed the same direction,
−25.8%; the smaller N=25 gap makes the share near-zero but same sign.) The sensitivity is
reported as a bound only — never the headline — per plan §5.

---

## 6. Visualizations & paper assets

`scripts/generate_paper_assets.py` produced, from the frozen run + ablation dirs, into
`outputs/20260708_191145_0fe76508/paper/`:

**Figures (PDF + PNG, 300 dpi, colourblind palette) — all 8 render, no skips:**

| Fig | Content | Source |
|---|---|---|
| F1 | Pairwise heatmap — ECS-adj components (primary) vs legacy Jaccard, per cell | instances |
| F2 | ECS-adj distributions, dataset × model facets (complete-case dark) | instances |
| F3 | AJ geometry-stability curves (the justification figure: AJ stable across set-size geometry) | simulation JSON |
| F4 | Erasure gap — CC3 vs random flip rate per model/operator | `aggregate_erasure.json` |
| F5 | CF validity ↔ agreement trade-off | aggregate |
| F6 | Cross-model vs within-model contrast (AJ) | `cross_model_agreement.json` |
| F7 | Confidence ↔ ECS grid (the R6 null, visualized) | instances |
| F8 | Ablation robustness — per-strategy paraphrase ECS-delta boxplots (`robustness_analysis.{pdf,png}`) | `ablation_results.json` |

**Tables (LaTeX booktabs):** T2 coverage, T3 primary (complete-case ECS-adj + Holm), T4 paradigm
components, T5 erasure, T6 cross-model, T8 confidence. (T1/T7/T9/T10 are guarded and skip when
their specific inputs are absent — none were needed here.)

**`numbers.json`** — every headline number keyed for `\input` into the LaTeX text: overall
complete/available ECS-adj, the three paradigm-component means (E-R +0.486, E-P +0.578, R-P
+0.382 — the ladder again), legacy comparators, and all 9 per-cell means with Holm p-values.

**Plus, in the run dir:** `soft_match_sensitivity.{json,md}` (W6, §5) and
`aggregate_erasure.json` (§3). The ablation dir also carries its own `robustness_analysis` plot.

---

## 7. How N=25 relates to the pilot and the 200-run

- **Directionally identical to the N=225 pilot** on every headline: complete-case ECS-adj +0.487
  (pilot +0.44), all cells positive, cross-model>within-model in all datasets, ladder monotone,
  erasure significant, confidence dead, brevity confound reversed under ECS-adj.
- **Under-powered exactly where predicted:** 3 complete-case cells fall below the N=6 gate
  (CF-scarce multiclass cells). The available-component test is fully significant, and the
  free-CF sensitivity confirms the conclusion is not a selection artifact.
- **What N=200 buys:** ~2.8× narrower CIs (every below-gate cell clears N=6; sst2's cross-model
  lower bound moves well off 0), and self-consistency ceilings that rest on 50 rather than 5–24
  paired instances (CF and H-on-MNLI ceilings in particular need the extra N to be trustworthy).

---

## 8. Caveats carried into the paper (review R1–R8, as realized in this run)

| # | Issue | Status in this run |
|---|---|---|
| R1 | Self-consistency ceiling | **Measured.** R ceiling +0.82 (R-pairs genuinely below it); H/CF ceilings low+noisy at N=25 → report next to ECS-adj, flag H/CF noise |
| R2 | Label-anchor / post-hoc rationalization | Framing only; state "consistency of label-conditioned rationalizations" as a first-class limitation |
| R3 | CF ≠ attribution support-set | **Supported by data:** R–CF is the lowest rung (+0.382); frame as attribution↔intervention divergence |
| R4 | No gold-rationale anchor | Not addressed here (post-run SNLI/e-SNLI annex, optional); state absence plainly |
| R5 | R-pair depression lexical? | **Measured null:** lexical share ≈ −2.5% at τ=0.8 → the gap is evidential, not synonymy |
| R6 | Confidence dead at T=0 | **Reproduced:** 109/225 = 0.95 → one-line appendix null |
| R7 | Easy single-cue datasets | Difficulty strata reported (length/vocab); harder task is future work |
| R8 | CF-MNAR selection | 40% CF validity; dual reporting + free-CF AJ sensitivity (+0.4394) mitigate; state selection direction |

**What this run does not claim:** it is N=25, so three cells stay wide and the ceilings are
noisy; CF-MNAR is mitigated, not eliminated; no claim of acceptance anywhere. The claim is that
every headline number here is reproducible from raw artifacts, tested on its own estimand's
population, read against a measured noise ceiling, and shipped with the caveat a competent
reviewer would otherwise write themselves.

---

## 9. Reproduce

```bash
# 1. main collection (N=25 subset; production config stays at 200)
python scripts/run_experiment.py --sample-size 25
#    -> outputs/<ts>_<id>/  (instance_results.jsonl, report.md, aggregate_metrics.json, ...)

# 2. erasure validity pass (family (b)); writes into the run dir
python scripts/run_validity_tests.py --results-dir outputs/<run>

# 3. ablation + self-consistency ceiling (nova-pro); writes a new outputs/<ts>/ablations/ dir
python scripts/run_ablations.py --sample-size 25

# 4. W6 soft-match sensitivity (offline, 0 API); writes into the run dir
python scripts/run_soft_match_sensitivity.py --results-dir outputs/<run>

# 5. paper assets (figures F1–F8, tables, numbers.json)
python scripts/generate_paper_assets.py outputs/<run> \
    --ablation-dir outputs/<ablation_ts>/ablations --out outputs/<run>/paper
```

Requires `AWS_BEARER_TOKEN_BEDROCK` + `AWS_REGION=eu-north-1` in a gitignored `.env`, and
(for W6 only) `python -m spacy download en_core_web_md`. Full test suite: `python -m pytest -q`
→ 620 passed.
