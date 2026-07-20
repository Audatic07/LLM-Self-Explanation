# Paper draft — "Do LLM Self-Explanations Tell One Story?"

Draft of record built from run `outputs/20260718_041618_eaa24e67`.
Current build: **19 pages** (main content pp. 1–9, Limitations onward exempt),
zero LaTeX errors, zero overfull boxes, all citations resolved, `verify_numbers.py` green.

## Files

- `main.tex` — full paper (ACL format, `[preprint]` mode: named authors + page numbers).
  Switch to `\usepackage[review]{acl}` for anonymous *ACL submission.
- `refs.bib` (NOT `references.bib` — a sibling `references/` PDF directory shadows that basename in BibTeX lookup) — two entries carry `TODO-VERIFY` notes on author lists
  (arXiv:2407.14487, arXiv:2502.18156); verify before submission.
- `acl.sty`, `acl_natbib.bst` — official ACL style files (acl-org/acl-style-files).
- `figures/` — vector PDFs copied from the run's `paper/figures/`, plus
  `make_dumbbell.py`, which generates the body figure (observed → reliability-corrected
  agreement) from `disattenuated_agreement.json`. It is sized for a single ACL column;
  do not enlarge `figsize` without scaling the font sizes.
- `tables/make_tables.py` — regenerates appendix tables A1–A4 from the run's frozen
  booktabs tables (prettified names only; numbers untouched). Run from repo root.
  `tables/A5_correctness.tex` is hand-written from the correctness computation.
- `verify_numbers.py` — cross-checks every number in Tables 1–5, the appendix additions,
  and the headline prose against the run artifacts (~270 checks). Run from repo root;
  exits nonzero on any mismatch. **Run this after any edit to results text.**
- `../tests/test_disattenuation_recovery.py` — planted-agreement simulation validating
  the Spearman correction on the AJ scale; backs every number in Appendix C.

## Build

```
tectonic main.tex
```

## Before submission

1. **Fill author affiliations + emails** (author block in `main.tex`).
2. **Insert the OSF view-only pre-registration link** — footnote in §3.4. The reviewer
   note is right that "pre-registered" is unverifiable at review time without it, and
   it is the paper's main differentiator.
3. **Verify the two TODO-VERIFY bib entries.**
4. **Page limit: content runs to p. 9; the ACL long-paper limit is 8.** Everything
   cheap has already been cut (Figures 1–2 moved to the appendix, Related Work and
   Discussion compressed, the simulation and degeneracy detail moved to Appendices C–D).
   Closing the last page requires an authorial call. Ranked options, least damaging first:
   - Cut Table 3 (cross-model) to two columns (Δ + CI only), keeping means in prose (~1/4 col).
   - Merge §6's three Discussion paragraphs into two (~1/3 col).
   - Move Table 5 (simulatability) to the appendix, keeping the null in prose (~1/2 col) —
     but this weakens the pre-registered-null framing, so it is listed last.
5. Switch to `[review]` mode.

## Completed collection runs (2026-07-20/21)

Both API runs flagged in earlier revisions are done; their results are in the paper.

1. **Paraphrase expansion** (~11k calls). Two further rewordings of all four elicitation
   prompts, collected per model over all four datasets (`prompts/*_alt2.txt`,
   `*_alt3.txt`; `run_ablations.py --paraphrase alt2|alt3`). Every reliability ceiling
   now pools three rewordings. Re-deriving the table under each wording separately moves
   no pair by more than 0.043 — but pooling shifted RO-CF's CI to exclude 1, so the
   extraction-perturbation pairs are described as approaching, not reaching, the ceiling.
   To extend further: add `alt4` to `ALT_PROMPT_SETS` and rerun the same command.

2. **Erasure salience baseline** (~9k calls, `run_salience_baseline.py`). Size- and
   occurrence-matched NON-consensus controls: SS1 (named by exactly one strategy) and
   TF-IDF (top lexical salience excluding the core). Consensus erasure flips 4-5x more
   than either, every model, both operators, Holm p=.0002.

## Other known open items (flagged in the text, not defects)

- **Simulatability used explanation-independent perturbations**, not Chen et al.'s
  explanation-derived construct. All claims are narrowed accordingly; an
  explanation-derived arm is the natural follow-up.
- **The recovery simulation models independent instrument noise only.** Correlated
  errors (plausible under the shared label anchor) would inflate corrected values;
  disclosed in Appendix C and Limitations. This is the one exposure the paraphrase
  expansion could NOT address - more rewordings do not decorrelate a shared label anchor.
- **Per-cell reliabilities remain wording-sensitive** (up to 0.26 spread for one
  strategy in one cell) even though pooled values are stable; per-cell corrected values
  in Appendix F carry more uncertainty than their bootstrap CIs show.
