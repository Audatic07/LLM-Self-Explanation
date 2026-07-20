# Paper draft — "Do LLM Self-Explanations Tell One Story?"

Draft of record built from run `outputs/20260718_041618_eaa24e67`.
Current build: **18 pages** (main content pp. 1–9, Limitations onward exempt),
zero LaTeX errors, zero overfull boxes, all citations resolved, `verify_numbers.py` green.

## Files

- `main.tex` — full paper (ACL format, `[preprint]` mode: named authors + page numbers).
  Switch to `\usepackage[review]{acl}` for anonymous *ACL submission.
- `references.bib` — two entries carry `TODO-VERIFY` notes on author lists
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
  and the headline prose against the run artifacts (~180 checks). Run from repo root;
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

## Two API runs that would close the last open holes

Both are specified in the text as not-run. Neither is possible right now: Bedrock
credentials are not loaded, and the campaign key was slated for rotation. With access
restored, these are the highest-value additions, in order:

1. **Paraphrase expansion** (~5k calls). Two further paraphrases per strategy across all
   cells, so each reliability ceiling becomes a distribution rather than a point, and
   Table 2's corrected column can be re-derived across the spread. This is the one thing
   that would convert the "extraction↔CF at ceiling" claim from provisional to solid —
   it currently rests on a single paraphrase per strategy, and low reliability inflates
   the corrected ratio. Run: `python scripts/run_ablations.py --model <name>` per model
   with the additional paraphrase templates, then re-run
   `scripts/run_disattenuated_agreement.py`.
2. **Erasure salience baseline** (~4–5k calls). CC3-sized top-TF-IDF or
   single-strategy-only token sets, both operators, over the ~2,200 CC3 instances. The
   post-hoc per-token density analysis (§5.4) already shows CC3 is the densest evidence
   per token erased, but a like-sized non-consensus baseline is the controlled version.

## Other known open items (flagged in the text, not defects)

- **Simulatability used explanation-independent perturbations**, not Chen et al.'s
  explanation-derived construct. All claims are narrowed accordingly; an
  explanation-derived arm is the natural follow-up.
- **The recovery simulation models independent instrument noise only.** Correlated
  errors (plausible under the shared label anchor) would inflate corrected values;
  disclosed in Appendix C and Limitations.
