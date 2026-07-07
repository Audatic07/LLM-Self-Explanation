# Paper Data & Visualization Plan — 2026-07-07

**Companion to:** `CODEBASE_STATUS_2026-07-07.md` (its P0.1–P0.4 fixes and decisions D1–D3 are prerequisites; nothing here launches before they land).
**Principle:** the paper is generated from **one frozen run's artifacts only**. Every table and figure below names its exact source file so nothing is hand-transcribed. Nothing speculative is built — every item maps to a pre-registered analysis or a section the paper needs.

---

## Part A — Data generation run-book (the experiment itself)

All collection code already exists; this is sequencing, not new code (except A0 and the one script in Part B).

### A0. Pre-flight (no API cost)
1. Land P0.1–P0.4 + the P1 items marked "fix" — suite must stay green (590+).
2. Re-run the offline validation artifacts with corrected `vocab_size`:
   `python scripts/simulate_planted_agreement.py` (V-agnostic, expected still green) and a fresh pilot rescore over `outputs/20260703_124843_013dd120` — this is the recorded evidence for D1 (ECS-adj adoption).
3. Record D1 in `config/experiment.yaml` comments + spec corrigendum; swap the report headline to ECS-adj complete-case.
4. Flip the launch config (D2): `sample_size: 200` ×3, drop `-pilot`.
5. Commit everything; verify `git_dirty=false` will hold (remove/commit the stray `outputs/20260701_101716_690abdc7/`).

### A1. Smoke passes (the three quota-blocked checks; ~$0.10 total)
| Smoke | Command | Pass criterion |
|---|---|---|
| H long-input truncation | run the single 206-word MNLI curated instance ×3 models (temporary `--sample-size` run or a tiny script over that instance) | `truncated_strategies` empty in all 3 rows |
| Erasure | `python scripts/run_validity_tests.py --results-dir outputs/20260703_124843_013dd120 --max-instances 6 --trials 3` | `aggregate_erasure.json` written; per-model grouping visible; no unknown-model error |
| Ablation (post-fix) | `python scripts/run_ablations.py --sample-size 3` equivalent smoke | all four arms produce non-empty variant sets; combined JSON + plot both written |

### A2. Main run (the frozen run)
```
python scripts/run_experiment.py            # 200 × 3 datasets × 3 models, concurrent
# on interruption: python scripts/resume_experiment.py <run_dir>
```
Completion checklist for the run dir: `instance_results.jsonl` (1800 rows), `aggregate_metrics.json`, `instance_metrics.csv`, `report.md`, `prompt_manifest.json` (hashes match disk), `config_snapshot.yaml`, `environment_snapshot.json` (`git_dirty: false`), `cross_model_agreement.json`, `execution_summary.txt` (0 unexplained API failures).

### A3. Erasure pass — same day, same frozen code
```
python scripts/run_validity_tests.py --results-dir outputs/<run>
```
Produces `erasure_instances.jsonl` + `aggregate_erasure.json` (per-model primary, pooled descriptive, family (b) p-values). ~30–35k calls, ~9 h at pilot throughput — run overnight; it is resumable only by re-running, so verify quota headroom first (AWS console).

### A4. Ablation pass — post-main, one model, subset 50 (per pre-registration)
```
python scripts/run_ablations.py     # after P0.2 fix: curated subsets, 4 working arms
```

### A5. Freeze
Commit the run directory + code SHA together. This commit is the paper's single source of truth; every asset in Part B reads only from it.

---

## Part B — Analysis, tables, and figures (new code: one script + one module upgrade)

### B1. `scripts/generate_paper_assets.py` (new, ~300 lines, zero API)

One entry point: `python scripts/generate_paper_assets.py outputs/<run> [--erasure-dir …] [--ablation-dir …] --out paper/`
Creates `paper/tables/*.tex` (booktabs) + `paper/figures/*` (via B2) + `paper/numbers.json` (every headline number keyed, so the LaTeX text can `\input` them and nothing is retyped). This replaces the stub `scripts/generate_paper.py` / `PaperGenerator` as the deliverable for "paper generation" — the prose is written by hand; the *numbers and assets* are generated. (Decide whether to delete `src/paper/paper_generator.py` or leave it; it must not be the thing that produces paper numbers.)

**Tables** (source → output):

| # | Table | Source | Notes |
|---|---|---|---|
| T1 | Datasets & curation summary (N, label balance, length buckets, drops by reason) | `data/processed/*_datasheet.json` | Appendix |
| T2 | Coverage / validity per strategy, per model×dataset (+ complete-case count, CF single-shot vs coached) | `aggregate_metrics.json` (model_dataset rows) | "Method reliability is itself a finding" table |
| T3 | **Primary results:** ECS-adj complete-case per cell, N, sign-flip p (raw + Holm); available-component secondary with its N | `aggregate_metrics.json` | Suppress/asterisk cells below `min_n_for_test`; legacy ECS + lift as two "as previously defined" rows below |
| T4 | Paradigm components E–R / E–P / R–P per cell + degenerate-pair counts | `aggregate_metrics.json` | The "which paradigms agree" decomposition |
| T5 | **Erasure:** CC3 flip vs random control per model per operator, paired gap, family-(b) p (raw + Holm); CC4 + per-strategy rates descriptive | `aggregate_erasure.json` | Per-model primary; pooled row labeled descriptive |
| T6 | Cross-model same-strategy vs within-model cross-strategy: paired Δ per dataset with bootstrap CI + direction | `cross_model_agreement.json` | The zero-cost novelty analysis |
| T7 | CF validity–minimality: minimal vs free (validity, minimality, first-attempt vs coached) per model | `aggregate_metrics.json` | Framed as confirmatory replication of arXiv:2509.09396 |
| T8 | Confidence↔ECS: Spearman ρ [CI], Kendall τ-b, N per cell | `aggregate_metrics.json` | Estimate, not test |
| T9 | Prompt-paraphrase ablation: mean ECS delta per strategy arm, N | ablation dir JSONs | One robustness table |
| T10 | Free-CF sensitivity ECS vs primary (post-P0.4) + missingness rates | `aggregate_metrics.json` | MNAR robustness row |

### B2. `src/plots/visualization_generator.py` upgrade (targeted, not a rewrite)

Global changes (one commit): pull `dpi` from config (currently defaults to 72 — config says 300); set a colorblind-safe palette (`sns.color_palette("colorblind")`) and `font size ≥ 10pt` in shared rcParams; keep the existing PDF+PNG dual export. Then add exactly these figures:

| # | Figure (function to add) | Content | Source |
|---|---|---|---|
| F1 | `plot_pairwise_heatmap_by_cell` | 6 strategy pairs × 9 cells heatmap, one panel for AJ (primary) and one for Jaccard (legacy) | `instance_results.jsonl` |
| F2 | `plot_ecs_adj_distributions` | ECS-adj (complete-case) violin/box + jittered points, faceted dataset × model; available-component in lighter shade | `instance_results.jsonl` |
| F3 | `plot_aj_geometry_stability` | The **justification figure**: mean AJ vs raw-Jaccard-lift across set-size geometries at fixed planted agreement (the property-(c) curves) — shows why ECS-adj replaces the flat mean | `ECS_ADJ_SIMULATION_2026-07-06.json` (already contains the curves) |
| F4 | `plot_erasure_gap` | CC3-vs-random gap per model, grouped by operator (mask/delete), error bars from per-instance paired diffs; second panel: gap by ECS-lift tier (labeled descriptive) | `erasure_instances.jsonl` / `aggregate_erasure.json` |
| F5 | `plot_cf_tradeoff` | Validity rate vs mean edit ratio, minimal vs free CF, one marker per model — the 2509.09396 replication picture | `aggregate_metrics.json` |
| F6 | `plot_cross_model_contrast` | Forest plot of paired Δ (cross-model − within-model) per dataset with 95% CI, vertical zero line | `cross_model_agreement.json` |
| F7 | (keep existing) `plot_confidence_ecs_scatter` per cell grid | confidence vs ECS-adj, ρ/τ-b annotated | `instance_metrics.csv` |
| F8 | (keep existing) `plot_robustness_analysis` with the P0.2 column fix | ablation deltas | ablation dir |

Existing generic functions (`plot_agreement_heatmap`, `plot_ecs_distributions`, `plot_flip_rate_comparison`) are subsumed by F1/F2/F4 — retire or leave for the tests; do not use them in the paper.

**Test coverage:** one smoke test per new function on synthetic frames (mirrors `tests/test_visualization.py`'s existing pattern), asserting files exist and are non-trivial. No pixel assertions.

### B3. Statistical outputs already produced — nothing new to build

For the record, the paper's inferential content is exactly: family (a′) ECS-adj > 0 per cell (Holm), family (b) CC3-vs-random per model per operator (Holm), bootstrap CIs (cluster-safe where pooled), and the pre-specified descriptive estimates (confidence association, cross-model Δ, strata). All are computed by the existing pipeline; `generate_paper_assets.py` only formats them. **Do not add tests post-hoc** — anything else stays descriptive, per the pre-registration in `config/experiment.yaml`.

---

## Part C — Explicitly out of scope (do not build)

- Semantic soft-matching sensitivity (plan Phase D) — gated on the pilot rescore showing R-pairs systematically depressed; it did not, so skip.
- Weighted ECS-adj (Ruzicka, Phase C) — secondary metric; only if reviewer-demanded later. Not needed for launch or the draft.
- New ablations (normalization, k-variation), dashboards, CC-SHAP benchmarking (not computable API-only — position in Related Work instead), human-anchor collection (e-SNLI ~20 items can be a camera-ready addition; not a launch blocker).
- Any change to prompts beyond the two `*_alt.txt` schema corrections in P0.2 — the canonical `*_explain.txt` prompts are frozen and correct as-is.

## Part D — Order of execution (single list)

1. P0.1–P0.4 fixes + P1 "fix" items → suite green.
2. A0 offline re-validation + D1 adoption recorded + D2 config flip → commit.
3. A1 three smokes (quota permitting).
4. A2 main 200×3×3 run → artifact checklist.
5. A3 erasure pass on that run.
6. A4 ablation pass.
7. Freeze commit (code SHA + artifacts).
8. B2 visualization upgrade + B1 asset script (can be written in parallel with A2–A4; they only read artifacts).
9. `python scripts/generate_paper_assets.py outputs/<run> …` → `paper/tables`, `paper/figures`, `paper/numbers.json`.
10. Write the paper prose against those assets; specs/README truth pass (FIX_PLAN P5) alongside.
