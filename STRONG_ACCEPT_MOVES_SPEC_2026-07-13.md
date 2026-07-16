# Strong-Accept Moves 1–3 — Implementation Specification (2026-07-13)

**Audience.** An implementing agent (Opus-class, medium effort) with full repo access. This
document is self-contained: every design decision is already made; your job is faithful
implementation, not re-design. Where a repo detail could have drifted, the step says
**VERIFY** with the exact grep/read to run — do the verification, don't guess.

**Context in two sentences.** This study measures cross-paradigm agreement of LLM
self-explanations (H=highlighting, R=rationale, CF=counterfactual, RO=rank-ordering) on
3 Bedrock models × 3 datasets, primary metric ECS-adj (chance- and ceiling-adjusted Jaccard,
paradigm-balanced), with an erasure axis and pre-registered test families
(`ECS_ROBUSTNESS_PLAN_2026-07-05.md` §A–G; audit in `RESEARCH_AUDIT_2026-07-10.md`).
The three moves below take the paper from weak-accept to strong-accept territory:
**(1)** reliability-corrected (disattenuated) agreement using per-model self-consistency
ceilings; **(2)** one shortcut-resistant dataset (CAD-IMDb, Kaushik et al. 2020);
**(3)** a counterfactual-simulatability bridge showing that cross-paradigm disagreement
predicts when explanations mispredict model behavior.

**Reference run (all numbers below):** `outputs/20260712_222045_c41933e8` (N=50/cell,
450 instances, seed 42). Ablation (nova-pro only): `outputs/20260713_022745/ablations`.

---

## 0. Ground rules (read before anything)

1. **Read-first list** (skim enough to know the local idiom before editing):
   - `scripts/run_ablations.py` (model selection ~L215; output schema at the
     `prompt_results[f"{s}_alt"]` block; `_meta` stamp near the final JSON dump)
   - `scripts/run_experiment.py` — `create_prompt_map` (prompt resolution per dataset),
     `process_instance` evidence assembly, the curated-load block (~L1530-1545)
   - `scripts/run_validity_tests.py` — `erase()`, `random_control_samples()`,
     `process_instance_erasure` (for schema conventions and the classify helper pattern)
   - `src/load/dataset_loader.py` (`load_curated`, `Instance`), `scripts/curate_dataset.py`
     and `src/load/curator.py` (curation pipeline CLI + datasheet writer),
     `scripts/curation_vetting.py` (the human-vetting `DROPS` dict pattern)
   - `src/utils/config.py` + `src/utils/config_loader.py` (dataset config dataclass +
     validation), `config/experiment.yaml`
   - `scripts/generate_paper_assets.py` (guarded `@guard` asset functions, booktabs writer)
   - one test file per subsystem you touch (e.g. `tests/test_run_validity_tests.py` uses
     importlib to load scripts; mirror that pattern for new script tests)
2. **Frozen surfaces — do not touch:** the four base `*_explain.txt` prompts, the four
   `*_alt.txt` paraphrases, `confidence_verbalized.txt`, normalization v3.0, the ECS-adj
   definition (`MetricsCalculator.adjusted_jaccard` / `compute_ecs_adjusted`), eps=0.10,
   the (a)/(a2)/(b) test families, seed 42.
3. **Pre-registration discipline:** §7 of this file is a ready-to-append amendment §H for
   `ECS_ROBUSTNESS_PLAN_2026-07-05.md`. Append it (dated) BEFORE running any new-data
   collection. All hypotheses/floors/tests below are fixed now, pre-data.
4. **Money:** every stage that spends API calls says so with an estimate. Nothing in Move 1
   beyond two ablation passes; Move 2 spends a main-run share; Move 3 is bounded to a
   50/dataset cohort. If quota errors appear (`RateLimitExhausted`), stop and report —
   don't loop.
5. **Known traps (cost hours if ignored):**
   - `generate_paper_assets.py --out` defaults to a RELATIVE `paper/` — always pass
     `--out <run_dir>/paper`.
   - Windows console is cp1252: no Greek/arrow glyphs in `print()` of new scripts.
   - `python scripts/<x>.py` needs repo root as cwd (scripts insert `parents[1]`).
   - Tests: `python -m pytest tests/ -q` must be green (currently 634) before AND after;
     add tests for everything you add.
   - New JSONL/JSON artifacts: write with `encoding="utf-8"`.

---

## Move 1 — Reliability-corrected (disattenuated) agreement

### 1.0 Rationale (for docstrings/paper text)

The self-consistency ceilings (same strategy, base vs paraphrased prompt, AJ scale) are
test–retest **reliabilities** of each elicitation instrument. Observed between-instrument
agreement is attenuated by instrument unreliability; the classical correction is
Spearman (1904): `corrected = observed / sqrt(rel_A * rel_B)`. Applying it per paradigm
pair converts the paper's biggest caveat ("H/CF can't even reproduce themselves") into a
method: either corrected agreement approaches 1 (divergence explained by elicitation
noise — a finding) or stays well below 1 (real paradigm divergence — a finding).
N=50 ceilings (nova-pro): R .90–.92, RO .62–.77, H .53–.66, CF .16–.70 (dataset-dependent).

### 1.1 Add a `--model` override to the ablation runner

File: `scripts/run_ablations.py`.
- **VERIFY** current selection: `grep -n "config.models\[0\]" scripts/run_ablations.py`.
- Add argparse arg `--model <name>` (the config model NAME, e.g. `qwen3-235b`), resolved
  against `config.models` by `.name`; unknown name = hard error listing valid names.
  Default: `config.models[0]` (unchanged behavior).
- Stamp the resolved model into the existing `_meta` block (already carries `model`;
  make sure it reflects the override, not `models[0]`).
- Test: extend `tests/test_ablation_self_consistency.py` with a unit test for the
  resolver function only (no API): valid name → model_id; invalid → raises.

### 1.2 Collect ceilings for the other two models  **[API: ~2 × 1.4k calls, ~2 h]**

```
python scripts/run_ablations.py --model qwen3-235b
python scripts/run_ablations.py --model deepseek-v3
```
Each writes `outputs/<ts>/ablations/ablation_results.json` (n=50/dataset; schema:
`{ds}_prompt -> {s}_alt -> {self_consistency_aj_mean, self_consistency_aj_values,
self_consistency_aj_n, mean_delta, mean_delta_aj, deltas, deltas_aj, ...}` + `_meta.model`).
Record the two new dir names; nova-pro ceilings already exist at
`outputs/20260713_022745/ablations`.

### 1.3 New analysis script: `scripts/run_disattenuated_agreement.py`  **[offline, 0 API]**

**CLI:**
```
python scripts/run_disattenuated_agreement.py --results-dir outputs/<main_run> \
    --ablation-dirs outputs/<abl_nova>/ablations outputs/<abl_qwen>/ablations outputs/<abl_deepseek>/ablations
```

**Inputs.**
- `<main_run>/instance_results.jsonl` — per instance: `model` (map id→name via the dict
  used in `scripts/run_weighted_null_sensitivity.py::MODEL_NAME`; copy it), `dataset`,
  evidence sets (`highlighting_tokens`, `rationale_tokens`, `counterfactual_tokens`,
  `rank_ordering_set`), `vocab_size`.
- Each ablation dir's `ablation_results.json`: reliability of strategy `s` on dataset `d`
  for the dir's `_meta.model` = `self_consistency_aj_mean` with its
  `self_consistency_aj_values` (keep the raw values for bootstrap).

**Computation (per model m × dataset d cell):**
1. Observed pair agreement: for each of the 5 cross-paradigm pairs
   `[("H","R"),("RO","R"),("H","CF"),("RO","CF"),("R","CF")]`, per instance compute AJ
   exactly as the pipeline does (reuse `MetricsCalculator.adjusted_jaccard` with the stored
   `vocab_size`, eps=0.10; skip empty sets / None). `obs(A,B) = mean` over defined
   instances; keep the per-instance value list.
2. Reliability lookup: `rel_s = self_consistency_aj_mean(m, d, s)`. If an ablation was run
   on a different instance subset — it was (50/dataset, seeded shuffle identical to the
   main run's slice, so at N=50 they coincide; at N=200 they are the first 50) — that is
   fine and pre-registered; note it in the output provenance.
3. **Reliability floor (pre-registered):** a pair is *estimable* only if BOTH
   `rel_A >= 0.30` and `rel_B >= 0.30` and both `self_consistency_aj_n >= 10`. Below floor
   → report `corrected = null`, `reason = "reliability_below_floor"` with the offending
   strategy. (At N=50 this excludes CF pairs on ag_news (rel .16) and mnli (rel .35 —
   passes .30, include) — the exclusions themselves get a table row, never silence.)
4. Disattenuated value: `corr(A,B) = obs(A,B) / sqrt(rel_A * rel_B)`. Values may exceed
   1.0 from sampling error — report as-is with flag `at_or_above_ceiling: true` when
   `> 1.0` (standard psychometrics caveat; do NOT truncate).
5. Composite: paradigm-balanced exactly like ECS-adj —
   `er* = mean(corr(H,R), corr(RO,R))`, `ep* = mean(corr(H,CF), corr(RO,CF))`,
   `rp* = corr(R,CF)`, `ecs_adj_disattenuated = mean(defined components)`; a component is
   defined only if ≥1 of its pairs is estimable. Also emit `n_components`.
6. **CI (seeded, B=2000, `np.random.default_rng(42)`):** per bootstrap replicate,
   resample (i) the per-instance AJ list of the pair (cluster = instance) and (ii) the
   ceiling's `self_consistency_aj_values` lists for A and B (independent resamples — the
   numerator and denominator come from different draws), recompute the ratio; percentile
   2.5/97.5. Guard: if a replicate's `rel` resample dips ≤ 0, drop the replicate and count
   it (`n_bad_replicates`); if >5% dropped, mark the CI unstable.
7. Pooled level: repeat 1–6 pooling instances across models per dataset (reliabilities:
   pool the three models' `self_consistency_aj_values` per (d, s)), and one overall pool.

**Output** `<main_run>/disattenuated_agreement.json`:
```json
{
  "provenance": {"formula": "Spearman 1904 disattenuation: obs/sqrt(relA*relB)",
                 "reliability_floor": 0.30, "min_ceiling_n": 10,
                 "ablation_dirs": ["..."], "seed": 42, "n_bootstrap": 2000},
  "per_cell": {"<model>_<dataset>": {
      "pairs": {"H_R": {"observed": 0.0, "rel_a": 0.0, "rel_b": 0.0,
                 "corrected": 0.0, "ci_lower": 0.0, "ci_upper": 0.0,
                 "n_instances": 0, "at_or_above_ceiling": false,
                 "estimable": true, "reason": null}},
      "er_star": 0.0, "ep_star": 0.0, "rp_star": 0.0,
      "ecs_adj_disattenuated": 0.0, "n_components": 3}},
  "per_dataset": {...same shape...}, "overall": {...}
}
```
Console: one line per cell — `cell | pair | obs -> corrected [ci] (rel_a, rel_b)` plus the
excluded-pair lines.

**Interpretation contract (put verbatim in the module docstring):** corrected ≈ 1 ⇒ the
pair's divergence is within elicitation noise; corrected ≪ 1 with CI excluding 1 ⇒ real
paradigm divergence beyond instrument unreliability. Expected headline: R-involving pairs
stay far below 1 (rel≈.9, obs≈.45 ⇒ corrected≈.5–.6).

### 1.4 Tests (new file `tests/test_disattenuated_agreement.py`)

Load the script via the importlib pattern from `tests/test_run_validity_tests.py`. Cover:
1. Known algebra: obs=0.45, rel_a=0.9, rel_b=0.9 → corrected=0.50 exactly.
2. Floor gating: rel_b=0.29 → estimable=false, corrected None, reason set.
3. Ceiling flag: obs=0.5, rels=0.49 → corrected>1 → `at_or_above_ceiling` true, value kept.
4. Composite: missing rp → `ecs_adj_disattenuated` = mean(er*, ep*), n_components=2.
5. Determinism: same inputs+seed → identical CIs.

### 1.5 Paper asset

`scripts/generate_paper_assets.py`: add `@guard("T9 disattenuated") table_T9(...)` reading
`<run>/disattenuated_agreement.json` (skip-if-missing like the other guards): per cell —
pair, observed, rel_a×rel_b, corrected [CI], flag column for excluded pairs. Add one test
in `tests/test_paper_figures.py` mirroring an existing table test.

### 1.6 Definition of done (Move 1)

- [ ] `--model` works; two new ablation dirs exist with `_meta.model` = qwen3-235b / deepseek-v3
- [ ] `disattenuated_agreement.json` produced for the reference run; console shows R-pairs
      corrected ≪ 1 and CF/ag_news excluded by floor
- [ ] All new tests green; full suite green
- [ ] T9 renders; §H appended (see §7)

---

## Move 2 — Shortcut-resistant dataset: CAD-IMDb

### 2.0 Rationale + honesty note (goes into the datasheet and the paper)

R7 objection: SST-2/AG News/MNLI are near-solved, single-cue, and in pretraining corpora
(per-cell accuracy 76–96%). CAD-IMDb — counterfactually-augmented IMDb from
[Kaushik, Hovy & Lipton, ICLR 2020](https://arxiv.org/abs/1909.12434) — is human-revised
so that shortcut cues break; classifiers trained on originals fail on it. **Honesty note
(state verbatim in the datasheet):** CAD was published in 2019-2020 and is therefore NOT
post-training-cutoff; it addresses the *shortcut/near-solved* prong of R7, not memorization.
Expect materially lower accuracy — that itself diversifies the "explanations of easy
predictions" concern.

### 2.1 Acquisition: `scripts/fetch_cad_imdb.py`  **[network, 0 Bedrock]**

- Source: the authors' repository `https://github.com/acmi-lab/counterfactually-augmented-data`
  (license: check the repo's LICENSE and record it in the datasheet; if no license file,
  record "research use, cite Kaushik et al. 2020").
- **VERIFY layout before coding:** fetch the repo tree (raw.githubusercontent.com) and
  locate the IMDb sentiment **revised** splits — expected TSVs with columns
  `Sentiment` (Positive/Negative) and `Text` under a `sentiment/` directory with
  `new/` (revised) and `orig/` subsets, split into train/dev/test. Use the REVISED
  (counterfactual) dev+test rows only (the point is shortcut-broken text; train is larger
  but keep eval-split hygiene consistent with the other datasets).
- Script writes `data/raw/cad_imdb/candidates_raw.jsonl`, one row per review:
  `{"text": <Text>, "label": "positive"|"negative", "source_split": "dev"|"test"}`
  (lowercase the labels; strip HTML with the repo's existing `pre_clean_text` if imported,
  else `html.unescape` + `<br />`→space).
- Deterministic: sort rows by a stable key (sha1 of text) before writing.

### 2.2 Curation into the frozen-set format  **[offline]**

- **VERIFY the curator CLI:** read `scripts/curate_dataset.py` top-to-bottom; it produced
  `data/processed/{ds}_{candidates,curated,decisions}.jsonl` + `{ds}_datasheet.json` for
  the other three datasets (pool 300 → final 200, seed 42, near_dup_jaccard 0.9). Extend it
  (or add a thin wrapper) to accept the local `candidates_raw.jsonl` as source when
  `--local-raw <path>` is given, bypassing HF download but running the SAME quality filter,
  length stratification, near-dup removal, and balanced selection.
- Curation params for `cad_imdb`: target 200 (100/100 by label), oversample 1.5,
  near_dup_jaccard 0.9, `min_content_words: 8`, `max_chars: 2000`,
  stratify_by label+length. **Near-dup warning:** CAD contains original/revised pairs with
  ~85% token overlap BY DESIGN if originals leak in — you are ingesting revised-only, but
  also add a guard: drop any candidate whose Jaccard vs another candidate ≥ 0.9 (the
  existing near-dup filter covers this; just confirm it fires in the decisions log).
- Vetting: add a `cad_imdb` section to `scripts/curation_vetting.py` following the DROPS
  pattern. For this programmatic pass, vet by rule (record it): drop candidates whose text
  contains meta-artifacts ("...", encoding damage, length < min). Human vetting can amend
  later; the datasheet must say vetting was rule-based for this dataset.
- Output: `data/processed/cad_imdb_curated.jsonl` (200 rows, fields exactly like
  `sst2_curated.jsonl`: `instance_id` (`cad_imdb_<srcsplit>_<idx>`), `text`, `label`,
  `dataset: "cad_imdb"`, `split: "dev+test-revised"`, `length_bucket`, `genre: ""`,
  `content_words`) + datasheet with `huggingface_id: null`,
  `source: "github.com/acmi-lab/counterfactually-augmented-data (revised IMDb)"` and the
  §2.0 honesty note + the Kaushik citation.

### 2.3 Config + prompts

- `config/experiment.yaml` datasets list — append:
  ```yaml
  - name: "cad_imdb"
    huggingface_id: "local:cad_imdb"     # loader uses the curated file; never downloads
    split: "dev+test-revised"
    sample_size: 200
    labels: ["negative", "positive"]
  ```
  **VERIFY** `config_loader.py` validation accepts this (it requires positive sample_size
  and non-empty labels; if `huggingface_id` format is validated, relax to allow the
  `local:` prefix and add a config test).
- New prompt `prompts/classification_cad_imdb.txt` — copy `classification_sst2.txt`
  byte-for-byte except the task line stays sentiment (IMDb is sentiment; the SST-2 wording
  "Analyze the sentiment expressed in the following text." is correct as-is). Do NOT
  create CF variants: with 2 labels, `create_prompt_map` resolves the binary base
  `counterfactual_explain.txt` — **VERIFY** by unit test (2.4).
- Prompt manifest: the run writes SHA-256s automatically; no action.

### 2.4 Tests

1. `tests/test_dataset_loader.py`: `load_curated("data/processed/cad_imdb_curated.jsonl")`
   → 200 Instances, 100/100 labels, all texts ≤ 2000 chars, ≥ 8 content words.
2. `tests/test_prompts.py`: `create_prompt_map(config, "cad_imdb")` resolves
   classification → `classification_cad_imdb.txt`, CF → binary `counterfactual_explain.txt`,
   H/R/RO → the shared bases; every template formats without KeyError using a sample text.
3. `tests/test_config_loader.py`: config with the new entry validates.

### 2.5 Smoke, then integrate  **[API: smoke ~120 calls; full N=200 share ~5–6k calls]**

- Smoke: `python scripts/run_experiment.py --datasets cad_imdb --sample-size 5` (all 3
  models). Check: 15/15 successful, CF validity > 0, no prompt-validation failures, H not
  truncated (reviews are 100–300 words; `strategy_max_tokens` is length-proportional —
  confirm `truncated_strategies` empty in the instance records).
- Full integration happens in the next production run (`--sample-size` per launch plan);
  the erasure/ablation/W6/weighted-null/asset pipelines are dataset-agnostic and pick the
  4th dataset up automatically (cells grow 9→12; T2–T9 iterate `model_dataset`).
- **Do not launch the N=200 production run yourself** — leave that to the user, as before.

### 2.6 Definition of done (Move 2)

- [ ] `cad_imdb_curated.jsonl` (200, balanced) + datasheet with source/license/honesty note
- [ ] config + prompt resolve; 3 new tests green; full suite green
- [ ] 5-instance smoke clean on all 3 models (report CF validity observed)
- [ ] §H appended (2.0 note referenced)

---

## Move 3 — Counterfactual-simulatability bridge

### 3.0 Rationale, hypothesis, pre-registered tests

Descriptive disagreement becomes decision-relevant if it predicts when explanations fail
their core job: letting an observer predict model behavior (counterfactual simulatability —
Chen et al., ICML 2024, arXiv:2307.08678; cf. arXiv:2606.01148). Design: build
explanation-INDEPENDENT perturbations of each instance, get the target model's actual
answers on them, then ask a *different* model (the simulator) to predict those answers
given (original text, model's original prediction, ONE strategy's explanation) vs a
no-explanation baseline.

**Pre-registered hypothesis (H-sim):** instance-level cross-paradigm agreement (`ecs_adj`,
available-component) is positively associated with simulatability gain
(`mean_s gain_s`, defined below). Tests, Holm-corrected within the family:
(i) pooled Spearman ρ(ecs_adj, mean_gain) with cluster bootstrap CI (cluster=instance),
per model (3 tests); (ii) tercile contrast: sign-flip permutation
(`src/statistics/statistical_tests.py::sign_flip_permutation_test`, alternative="greater")
on top-tercile − bottom-tercile mean_gain, pooled per model. Descriptive companion: the
"red-flag" operating point — precision/recall of `ecs_adj < median` for predicting
`best_s sim_acc_s < baseline_acc` instances.

### 3.1 Perturbation generator (deterministic, explanation-independent)

New module functions inside the new script (below), unit-testable:
- Pool = unique surface content words, exactly `random_control_samples`' pool construction
  (import `random_control_samples`, `erase`, `erased_token_count` from
  `scripts/run_validity_tests.py` — reuse, don't reimplement).
- Per instance, 3 perturbations of the ORIGINAL text:
  - **P1** delete 3 random content types — `erase(text, sample, "delete", normalizer)`
    with `sample = random_control_samples(text, 3, trials=1, seed=s1)[0]`
  - **P2** mask 3 random content types (different draw, `"mask"` operator, seed=s2)
  - **P3** delete the 3 highest-frequency content types (ties broken alphabetically) —
    deterministic, text-statistics only
  Seeds: `s1 = crc32(instance_id) ^ 42`, `s2 = s1 + 1` (stable across runs/resumes).
- Skip rule: if the pool has < 3 types, use all available; if a perturbation equals the
  original text (nothing matched), drop that perturbation for that instance (count it).

### 3.2 Prompts (two new files; house JSON style)

`prompts/simulatability_predict.txt`:
```
A classifier model read the following text and predicted: {predicted_label}

Text: "{input_text}"

The model gave this explanation of its prediction:
{explanation}

The text was then modified as follows:

Modified text: "{perturbed_text}"

Based on the explanation, predict what the SAME model will answer for the modified text.
Choose from: {label_set}.

Return only valid JSON:
{{"label":"<one of: {label_set}>"}}
```
`prompts/simulatability_predict_baseline.txt`: identical minus the two explanation lines.
`{explanation}` rendering per strategy (from `instance_results.jsonl` fields):
- H: `Important words (1-10 salience): ` + the raw salience pairs already in
  `raw_highlighting`'s parsed form — **use the normalized evidence set with scores if
  stored; else the token list** `highlighting_tokens` joined by ", " prefixed
  `Most important words: `.
- R: `rationale_text` verbatim.
- CF: `Minimal edit that flips the prediction: "` + `cf_counterfactual_text` + `"` (only
  instances with `cf_flip_verified`; else CF arm is skipped for that instance).
- RO: `Words ranked by importance: ` + ordered `rank_ordering_tokens` tokens.

### 3.3 Collection script: `scripts/run_simulatability.py`  **[API — see budget]**

**CLI:** `python scripts/run_simulatability.py --results-dir outputs/<run> [--subset 50] [--max-instances N]`

**Cohort (pre-registered):** first `--subset 50` instances per dataset per model in
`instance_results.jsonl` file order (this equals the ablation cohort's seeded slice).

**Flow per instance:**
1. Build the ≤3 perturbations (§3.1).
2. **Target-model ground truth:** classify each perturbation with the instance's OWN model
   (same engine/grouping pattern as `run_validity_tests.py::run()` — group by model, hard
   error on unknown model ids; reuse its `classify` helper and dataset prompt cache).
   Store the predicted label per perturbation (None if unparseable).
3. **Simulator:** the NEXT model in config order round-robin (never the target — same rule
   as the held-out CF judge). For each arm in `["baseline","H","R","CF","RO"]` × each
   perturbation: format the §3.2 prompt, classify, parse with the dataset's `label_set`.
   Skip strategy arms whose explanation is missing/invalid for that instance (count).
4. Per instance record → `simulatability_instances.jsonl`:
   ```json
   {"instance_id": "...", "model": "...", "simulator": "...", "dataset": "...",
    "ecs_adj": 0.0, "ecs_adj_complete": true,
    "perturbations": [{"kind": "P1", "target_label": "...",
                       "arms": {"baseline": "...", "H": "...", "R": null, ...}}],
    "n_perturbations": 3, "skipped_arms": {"CF": "no verified flip"}}
   ```
5. Checkpoint: append-only JSONL after each instance (mirror the erasure pass; a re-run
   with the same cohort must skip already-present instance_id+model rows).

**Aggregation → `aggregate_simulatability.json`:**
- Per instance × arm: `sim_acc_arm` = fraction of perturbations with
  `arms[arm] == target_label` (both non-null). `gain_s = sim_acc_s − sim_acc_baseline`.
  `mean_gain` = mean over available strategy arms.
- Per model (primary unit) + pooled: mean sim_acc per arm, mean gain per strategy,
  H-sim tests as pre-registered in §3.0 (reuse `sign_flip_permutation_test`, seed 42,
  10000 perms; `holm_correction` across the 3 per-model tests within each family),
  red-flag precision/recall descriptive block, and full provenance (subset, seeds,
  prompt hashes).

**Budget at `--subset 50` (450 cohort rows):** target labels ≤ 3×450 = 1,350; simulator
≤ 5 arms × 3 × 450 = 6,750; total ≈ 8.1k calls + retry overhead (N=50 run showed 18.6%
retry rate) ⇒ plan ~10k requests, ~2–3 h at 2 concurrent. **Do not scale past subset 50
without the user's go-ahead.**

### 3.4 Tests (`tests/test_simulatability.py`, importlib pattern)

1. Perturbation determinism: same instance_id+text → identical P1/P2/P3; P3 picks the 3
   highest-frequency types with alphabetical tie-break (construct a text where this is
   checkable by hand).
2. Skip rules: 2-type pool → uses 2; no-op perturbation dropped and counted.
3. Prompt rendering: every arm formats without KeyError; baseline contains no
   "explanation" substring; CF arm skipped when `cf_flip_verified` false.
4. Aggregation math on a synthetic JSONL: hand-computed sim_acc/gain; Holm family size
   = number of non-None tests; red-flag precision/recall on a 4-instance toy.
5. Checkpoint skip: pre-seeded JSONL row is not re-collected (mock engine counts calls).

### 3.5 Definition of done (Move 3)

- [ ] Script + prompts + tests green; full suite green
- [ ] Dry structural run with a mocked engine (tests cover it) — no live calls needed to
      merge the code
- [ ] Live run executed on the reference run's cohort ONLY if the user approves the ~10k
      calls; then `aggregate_simulatability.json` exists and the §3.0 tests report
- [ ] §H appended before the live run

---

## 7. Pre-registration amendment §H (append verbatim to `ECS_ROBUSTNESS_PLAN_2026-07-05.md`, dated)

```markdown
## §H. AMENDMENT (2026-07-13, pre-N=200) — reliability correction, CAD-IMDb arm, simulatability bridge

Registered before any new-data collection (STRONG_ACCEPT_MOVES_SPEC_2026-07-13.md).

1. **Disattenuated agreement (Spearman 1904).** Per model×dataset and pooled, each
   cross-paradigm pair's observed AJ mean is corrected by the geometric mean of the two
   strategies' self-consistency ceilings (per-model ablation, *_alt paraphrases).
   Estimability floor: both reliabilities >= 0.30 with ceiling n >= 10; excluded pairs are
   reported as excluded, never silenced. Values > 1 are reported with an at-ceiling flag.
   Interpretation registered in advance: corrected ~ 1 = divergence within elicitation
   noise; corrected << 1 (CI excluding 1) = real paradigm divergence. Descriptive
   companion to families (a)/(a2), no new NHST family.
2. **CAD-IMDb arm.** Fourth dataset: revised (counterfactual) IMDb dev+test from Kaushik
   et al. 2020, curated to the frozen-200 format (100/100). Addresses the shortcut/
   near-solved prong of R7; NOT post-cutoff (recorded in the datasheet). Enters every
   existing family under the §G granularities (cells grow 9→12; per-dataset co-primary
   grows 3→4; Holm m grows accordingly).
3. **Simulatability bridge (family (c), NEW).** Cohort: first 50 instances/dataset/model
   (seeded slice). Three explanation-independent perturbations per instance (2 random
   content-type erasures, seeds crc32(instance_id)^42 and +1; 1 deterministic top-frequency
   deletion). Target model labels its own perturbations; the next model round-robin
   simulates, per arm {baseline, H, R, CF, RO}. Estimand: gain_s = sim_acc_s −
   sim_acc_baseline. H-sim: ecs_adj (available) is positively associated with mean gain.
   Tests: per model, (c1) Spearman rho with cluster-bootstrap CI, (c2) top-vs-bottom
   tercile sign-flip permutation (one-sided), Holm within each of (c1)/(c2). Red-flag
   precision/recall reported descriptively. Negative or null results are reported as-is.
```

---

## 8. Execution order & final checklist

1. Append §H (§7) → commit checkpoint.
2. Move 1: 1.1 code+tests → 1.2 two ablation runs → 1.3–1.5 analysis+asset → done-list.
3. Move 2: 2.1 fetch → 2.2 curate → 2.3 config/prompts → 2.4 tests → 2.5 smoke → done-list.
4. Move 3: 3.1–3.4 code+tests (mergeable without live calls) → live run only on user
   approval → done-list.
5. Full suite green (>634). Update `RESEARCH_AUDIT_2026-07-10.md` is NOT needed; instead
   add one line to `PAPER_READINESS_PLAN_2026-07-08.md`'s audit banner pointing here.
6. Report to the user: ceilings table (3 models), disattenuated headline pairs, CAD smoke
   CF-validity, simulatability status, and the exact commands for anything deferred.

**What NOT to do:** no changes to frozen prompts/metrics/families; no N=200 launch; no
silent scope growth; every number you report must come from an artifact you produced.
