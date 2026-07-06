# Improvement Plan — Pilot `20260703_124843_013dd120` → Full 200-Instance Run

**Date:** 2026-07-04
**Pilot analyzed:** `outputs/20260703_124843_013dd120/` (90 instance-runs: 10 instances × 3 datasets × 3 models, post-FIX_PLAN pipeline, git `712b7ba`)
**Goal:** make the study publication-ready before committing to the full run (200/dataset × 3 datasets × 3 models = 1,800 instance-runs).

---

## Verdict

The pipeline is fundamentally healthy: 0 API failures, 0 refusals, token accounting reconciles exactly (182,868), the Holm correction behaves correctly (all 9 cells collapsing to p=0.0108 is the monotonicity rule working, not a bug), internal counts are consistent (23 first-attempt + 2 coached = 25 CF valid ✓), checkpointing exists, and prompt/config/environment provenance is captured.

However, there are **4 blockers (P0)** that would materially damage the paper if the full run were launched today, plus a set of P1 correctness/reporting fixes and P2 polish items. The single most important finding: **CF validity is confounded by tokenization artifacts, and CF validity gates the primary estimand (complete-case ECS).**

Verified-good items (no action needed): Holm correction arithmetic; dynamic top-k tie-breaking (deterministic: score desc, then alphabetical — `parser.py:217`); CF correction-loop bookkeeping; per-model erasure design in `run_validity_tests.py`; MNLI hypothesis-only span protection (`parser.py:360–373`); sampling determinism (seed 42 in config snapshot); prompt SHA-256 manifest.

---

## P0 — Blockers (fix before the 200-run)

### P0.1 CF edit-ratio is tokenization-sensitive → SST-2 CF validity collapse is an artifact

**Evidence.** CF canonical validity per cell: nova-pro/sst2 **0%**, qwen3/sst2 30%, deepseek/sst2 **90%** (report Per-Dataset Summary). Same instance, both models correct, near-identical rewrites semantically:

- `sst2_validation_000665` — nova-pro (report L223): rewrote SST-2's pre-tokenized text `"you 're … scenes , you 've got ice water in your veins ."` with normal spacing (`you're`, `scenes,`) → **rules-compliant: No** (edit ratio 0.625).
- `sst2_validation_000665` — deepseek-v3 (report L3618): preserved the tokenized style (`"you 've got a heart of gold ."`) → **valid, flip verified**.

**Root cause.** `_word_edit_ratio` (`src/parsing/parser.py:515`) does whitespace `split()` + exact string equality per word. SST-2 curated text is Treebank-tokenized (`you 're`, `scenes ,`), so a model that writes normal English is charged phantom edits: `you 're`→`you're` = 2 edits, `scenes ,`→`scenes,` = 2 edits. On instance 000665 the detokenization fixes alone consume ~0.25 of the 0.3 budget before any semantic edit. `_extract_changed_tokens` (`parser.py:393`) has the same sensitivity and can attribute unchanged words (e.g. `scenes`) as CF evidence.

**Consequences if unfixed.** (a) "CF reliability differs by model" becomes partly "which model mimics Treebank spacing" — a reviewer-fatal confound; (b) complete-case selection (the primary estimand) is driven by this artifact (see P1.1); (c) CF evidence sets carry spurious tokens into ECS extraction–perturbation pairs.

**Fix (recommended, keeps curated data frozen).**
1. Canonicalize BOTH sides before the Levenshtein and the difflib pass: apply one shared regex tokenization (split clitics `'re/'ve/n't`, detach punctuation, casefold) so `you're` ≡ `you 're`, `scenes,` ≡ `scenes ,`. Compute the ratio over canonical content tokens; keep MiCE normalization by original length.
2. Belt-and-suspenders prompt nudge in `counterfactual_explain*.txt`: "Keep the original spacing and punctuation style; only change the words you edit."
3. Unit tests: (i) detok-only rewrite of a tokenized SST-2 sentence → ratio 0.0 and `from_tokens` empty (→ "identical" error path); (ii) one real edit on tokenized text → ratio counts only that edit; (iii) MNLI span path unchanged.

**Acceptance.** Re-parse the pilot's 90 stored raw CF responses offline (no API needed — `raw_counterfactual` is in `instance_results.jsonl`) and confirm SST-2 CF rules-compliance no longer differs by an order of magnitude across models.

### P0.2 H-strategy responses will overflow `max_tokens: 1024` on long MNLI instances

**Evidence.** Curated length distributions (words): sst2 max 46; ag_news max 67 (8 long); **mnli max 206 (17 long >50 words)**. The pilot sampled no instance long enough to trigger this (max sampled ~50 words), so the risk is invisible in the pilot. H asks the model to score **every word** (`highlighting_explain.txt`); a 206-word input needs roughly 6–10 output tokens per `["word", score]` entry → 1,300–2,000+ tokens, well over `inference.max_tokens: 1024` (`config_snapshot.yaml:98`). RO/confidence are safe (short outputs); R is one sentence.

**Consequences if unfixed.** H truncation on exactly the long-input stratum → coverage loss correlated with length → biased "ECS by Input Length" analysis, and the truncation retry (`data_models.py:610` counter) retries at the same cap, so it fails again.

**Fix.** Raise the elicitation cap (e.g. 4096) globally or per-strategy for H (cheapest robust option: `max_tokens = max(1024, 12 × n_words + 200)` for H). Then smoke-test the single longest MNLI instance (206 words) on all 3 models and confirm `truncated_strategies` stays empty.

### P0.3 Erasure pass (pre-registered test family b) has never run on the post-v3.0 pipeline

**Evidence.** The only erasure artifact in the repo is `outputs/20260617_141418_1b6e9551/aggregate_erasure.json` — from **2026-06-17**, i.e. pre-lemmatization, explicitly stale per project memory. The report's framing note (report L100) promises the erasure axis; the pilot dir has no `aggregate_erasure.json`.

**Risk.** Test family (b) is half of the pre-registered inference plan. If it crashes or behaves badly, better to learn on 90 pilot instances than after a 1,800-instance run. Also its cost dominates the study (see P0.4).

**Fix.** Run `python scripts/run_validity_tests.py --results-dir outputs/20260703_124843_013dd120` (optionally `--max-instances 6 --trials 3` first as a smoke, then the full pilot). Review the output shape, per-model grouping, and the CC-vs-random headline before the 200-run.

### P0.4 API-request accounting is fabricated → cost/quota/wall-time forecasts are ~2× off

**Evidence.** `scripts/run_experiment.py:1366`: `summary.api_requests_total = len(all_results) * 5` (hardcoded). The execution summary says 450 requests; the log contains **805** "Bedrock request" lines (~8.9/instance: classification, confidence, H, R, CF-minimal, CF-free, CF flip-verification calls, correction attempts, RO self-correction).

**Fix.** Count actual requests in the inference engine (increment on every invocation, including verification/correction calls) and surface per-category counts in the execution summary. Token totals are already correct — only the request counter lies.

**Full-run forecast (using real pilot rates).**

| Pass | Calls (est.) | Basis | Wall-time @ pilot throughput (~1.07 calls/s) |
|---|---|---|---|
| Main collection | ~16,100 | 1,800 × 8.9 | ~4.2 h |
| Erasure (as configured) | ~50–55,000 | ~30/instance: (valid strategies + CC3 + CC4) × 2 operators + **10 random trials × 2 operators** + held-out CF | **~13–14 h** |
| Ablation (`run_ablations.py`, subset 50) | ~2–4,000 | 4 alt strategies × 50 × 3 datasets × 3 models + reparses | ~1 h |

The erasure random control (`n_random_baseline_trials: 10` × 2 operators = 20 classifications/instance) is the cost driver. **Decision needed** (pre-register whichever you choose): keep 10 trials, or cut to 5 (saves ~18k calls, the average over 5 is still a fine control), and/or restrict erasure to instances with defined ECS (86/90 ≈ 4% saving only). Also consider raising `concurrent_requests` from 2 if Bedrock quotas allow — verify with a quota check first.

---

## P1 — Methodological & correctness items (strongly recommended)

### P1.1 Complete-case ECS (primary estimand) has structural selection bias

Complete cases = instances where CF survived. Pilot: 22/90 (24%), and CF validity ranges **0%–90% across cells**, so the complete-case pool over-represents deepseek-v3 and sst2 (9 of deepseek/sst2's 10 instances are complete; nova/sst2 contributes 0). The pooled "primary estimand" is then a weighted average over a non-random cell mix — a reviewer will flag this immediately.

Mitigations (do all three):
1. **P0.1 fix** raises SST-2 CF validity and shrinks the cell imbalance mechanically.
2. **Report complete-case ECS per model×dataset cell** (the aggregate JSON already stores `mean_ecs_complete`/`n_complete_cases` per cell — surface them in the report table; suppress cells with n below `min_n_for_test`).
3. **Add a pre-specified sensitivity analysis: ECS with free-CF evidence** in place of minimal-CF. `cf_contrast_tokens` (82% validity) is already stored per instance — this is a pure post-processing computation, zero API cost, and it shows whether conclusions survive when the perturbation paradigm isn't gated by the 28%-validity minimal-edit constraint. State plainly: minimal-CF ECS is primary, free-CF ECS is robustness, missingness is MNAR and that is why the sensitivity analysis exists.

### P1.2 Report-generator bugs (all confirmed in `src/utils/data_models.py`)

| # | Bug | Location | Fix |
|---|---|---|---|
| 1 | "**No long inputs (>50 words) were sampled**" printed unconditionally — pilot report contains this note AND a `Long (>50): N=3` row 160 lines later; note arithmetic (22+61) also ≠ 90 because it silently uses only ECS-defined instances | `data_models.py:648` | Make conditional on `overall.n_long == 0`; include all three bucket Ns; count over all sampled instances or say "with defined ECS" |
| 2 | `Mean ECS (all with ≥3 valid, N=90)` — N is `overall.n_instances` (90), but mean is over the 86 with defined ECS (4 instances had only 2 valid strategies; see log "ECS not computed") | `data_models.py:692` | Add/report `n_ecs` (86), not total instances |
| 3 | Second overall-metrics block (Introduced-concept rate … CC4) is a **headerless markdown table** — no `\|---\|` separator after the blockquote, renders as literal pipe text on GitHub | `data_models.py:720–732` | Add `\| Metric \| Value \|` header + separator (or merge into the first table) |
| 4 | ECS-by-correctness prints `0.0000 (0)` for empty strata (all three sst2 rows) — reads as "measured zero" | `data_models.py:777` | Print `—` when n=0 |
| 5 | Every per-instance strategy section is numbered `#### 4.` (H, R, CF, RO all "4", then "5. Pairwise") | `data_models.py:975` | Enumerate 4–7 |
| 6 | Per-instance pairwise table: `Kendall τ`, `Normalized τ`, `RBO` rows have 2 cells in a 3-column table | `data_models.py:1034–1036` | Pad third cell or move rank metrics to their own list |
| 7 | High/Low-ECS examples: `mnli_..._008565` appears **twice verbatim** (same instance under two models); headings never say which model produced the ECS | `data_models.py:1040–1052`, `extract_high_low_ecs_examples` (`:1174`) | Dedupe by `instance_id`; append `— {model}` to the heading |
| 8 | Per-Dataset Summary columns `H \| R \| CF \| RO` are validity rates but the header doesn't say so | `data_models.py:615` | Rename to `H valid` etc., or add a caption line |
| 9 | `Verbalized confidence — mean (N=86)` but all 90 instances have confidence (CSV `confidence` has 0 missing); the 86 is the ECS-paired subset (mean over 90 = 0.936, over 86 = 0.940) | `n_confidence` population | Either compute over all with confidence or relabel "(ECS-paired N=86)" |
| 10 | Kendall/RBO aggregates are means over the defined-only subset but no N is shown (τ is undefined for many instances — pilot per-instance tables show `—` while cell means exist) | rank-metric rows | Report N alongside |
| 11 | Cross-model agreement CF cells rest on N=2–3 pairs, displayed identically to N=30 cells | cross-model table | Footnote or suppress cells with N<5 |

### P1.3 Execution-summary bugs (`src/utils/data_models.py:520–553` + producer)

1. **Sampling log pools wrong_pred across models but not requested/sampled**: `mnli: requested=10, sampled=10, wrong_pred=12` — 12 wrong out of 10 sampled is nonsense as printed. Emit one line per model×dataset (matching the report table) or pool all three columns (30/30/12).
2. **"Parsing Failures by Strategy:" is empty** despite ~65 CF failures, R failures, etc. in the log — `summary.parsing_failures` is never populated. Populate per-strategy counts (they're already in the per-instance `*_parsed`/`*_valid` fields).
3. `Duration: 783.87s` here vs `754.8s` in report.md — two different clocks; unify (cosmetic).
4. Field naming: `dropped_wrong_pred` — wrong-prediction instances are **kept** (D5 stratum), not dropped. Rename to `wrong_pred_kept` to avoid a future misreading (code hygiene, not user-facing).

### P1.4 Provenance gaps for the paper

- **Confidence elicitation is invisible**: `instance_results.jsonl` stores classification/H/R/CF/RO prompts and raw responses, but not the confidence prompt or raw confidence response, and the per-instance report sections never show it. Persist both (matters for a paper claiming Tian/Xiong-style elicitation).
- **`git_dirty` flag** absent from `environment_snapshot.json` (has commit + packages). Record dirty/clean state at run start.
- **Log encoding**: arrows in log messages render as `�` (cp1252 write on Windows). Open log handlers with `encoding="utf-8"`.

---

## P2 — Polish / robustness (worth doing, not blocking)

1. **Stopword-discarded RO evidence**: pilot discarded rank items `too`(×5), `did`(×5), `up`(×4), `only`(×4), `doing`(×4), `off`, `but`, `she`… as stopwords. For sentiment, `too` and `only` can be genuine cues ("too long", "only redeeming quality"). POLARITY_WORDS already whitelists negations; decide whether to extend it with degree/focus particles (`too`, `only`, `enough`) — either way, **freeze the decision now and document it**, since changing token space mid-study invalidates comparisons. Cheap check: count how often these were the model's rank-1 item in the pilot (log lines at `parser.py:432`).
2. **Confidence ceiling**: values concentrate in {0.9…1.0} (min 0.7, mean 0.94) → heavy ties make per-cell Spearman fragile (8/9 pilot CIs span 0). Keep as pre-registered *estimate* (already the design); at N=200/cell it will stabilize, but consider adding Kendall τ-b (tie-robust) as a companion column, pre-specified as descriptive.
3. **Pooled CI is cluster-blind** (same instance under 3 models). The report already caveats this; for the paper either implement an instance-level cluster bootstrap for pooled rows or drop pooled CIs and keep everything per-cell.
4. **Cross-model finding deserves a pre-specified readout**: pilot shows cross-model same-strategy agreement (0.56–0.66) **exceeds** within-model cross-strategy ECS (0.40–0.44) in all 3 datasets — evidence for a shared task prior over privileged self-knowledge (the report cites both hypotheses but never states which pattern was observed). Add: (a) a paired per-instance contrast (Δ = cross-model mean − within-model ECS) with a bootstrap CI, descriptive; (b) one sentence in the report template stating the observed direction. This is likely a headline result — treat it with the same rigor as ECS-lift.
5. **Ablation pass** (`run_ablations.py`, one pre-registered paraphrase ablation, subset 50): never smoke-tested post-fix. Run `--max-instances 3`-style smoke before the full run; alt prompt files all exist.
6. **SST-2 has zero long instances by construction** (max 46 words; max_chars 400). Pre-declare in the paper that the long stratum is MNLI/AG-News-only, so it doesn't look post-hoc.
7. **Length-note vs bucket-table basis**: unify on one definition (raw whitespace words vs normalized tokens) for "input_length" everywhere (report note, buckets, `input_length` field).

---

## Pre-flight checklist for the 200-run

1. [x] P0.1 CF canonicalization merged + unit tests + offline re-parse of pilot CFs shows cell convergence — done 2026-07-05; see `outputs/20260703_124843_013dd120/P0.1_cf_canonicalization_reparse.md`; SST-2 spread narrowed 90pts→60pts, all changes were false-rejection fixes.
2. [~] P0.2 `max_tokens` raised for H (length-proportional formula, code done + tested). Live smoke-pass on the 206-word MNLI instance across all 3 models is **BLOCKED**: Bedrock account hit a "Too many tokens per day" daily quota exhaustion 2026-07-05. Re-run `scripts/resume_experiment.py` or a fresh smoke once quota clears.
3. [~] P0.3 erasure smoke — **BLOCKED** by the same quota exhaustion. `run_validity_tests.py` needs no code changes (already reads `config.validity.n_random_baseline_trials` dynamically); run `python scripts/run_validity_tests.py --results-dir outputs/20260703_124843_013dd120 --max-instances 6 --trials 3` once quota clears.
4. [x] P0.4 real API counter in place (`InferenceEngine.total_requests`/`total_requests_failed`/`requests_by_category`, surfaced in `ExecutionSummary`) + tested. Erasure `trials` decided: **5** (recorded in `config/experiment.yaml`). Quota headroom for ~70k calls: **not verifiable from here** — check the AWS Bedrock Service Quotas console before launching.
5. [x] P1.2/P1.3 report + summary fixes merged — all 11 + 4 items fixed and tested.
6. [x] P1.4 confidence prompt/response persisted (`InstanceResult.confidence_prompt`/`confidence_raw_response`); `git_dirty` flag added to `environment_snapshot.json`; log file handler now UTF-8.
7. [x] Full test suite green — 581 tests passing (up from 518). Commit/tag and `git_dirty=false` are launch-time actions for you to take when ready (not done here — many uncommitted changes are this implementation pass itself).
8. [ ] Config diff reviewed: confirmed the ONLY diff needed for the 200-run is `sample_size: 200` (all 3 datasets) and dropping `-pilot` from `experiment.name` — every other setting in `config/experiment.yaml` is already correct for the full run. **Not flipped** — that's the launch trigger, left for you.
9. [x] Kill/resume drill — done via `tests/test_resume_drill.py` (mocked engine, since live Bedrock is quota-blocked): resume after a simulated kill produces IDENTICAL results to an uninterrupted run; `--force-restart` correctly discards and reprocesses. Real infrastructure also added: `scripts/resume_experiment.py`, checkpoints now loaded (previously write-only), `RateLimitExhausted` now stops a model's loop early instead of churning through guaranteed failures.
10. [ ] Launch order (main → erasure → ablation, reviewing each artifact before the next) — process guidance for you at actual launch time, unaffected by this pass.

## Decisions needed from you (everything else can proceed without input)

1. **CF fix flavor** — **DECIDED (2026-07-05): canonicalized diff + prompt nudge.** Implemented in `src/parsing/parser.py` (`_canonical_tokens`, `_word_edit_ratio`, `_extract_changed_tokens`) + a "keep original spacing" line added to all 6 canonical CF prompt files.
2. **Erasure budget** — **DECIDED (2026-07-05): 5 trials** (down from the pre-registered 10), recorded as a pilot-informed amendment in `config/experiment.yaml`'s `validity.n_random_baseline_trials`.
3. **Concurrency** — **DECIDED (2026-07-05): keep `concurrent_requests: 2`.** Unchanged from the pilot config.
