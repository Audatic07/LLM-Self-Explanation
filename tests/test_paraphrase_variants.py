"""Paraphrase-variant plumbing (2026-07-20 reliability-spread expansion).

Guards the properties that make additional ceilings comparable to the original:
the variant sets must cover every strategy, keep every format slot, keep the JSON
schema, and actually differ in wording from each other and from the base prompt.
"""
import importlib.util
import string
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.utils.exceptions import ConfigurationError  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "run_ablations", REPO / "scripts" / "run_ablations.py")
run_ablations = importlib.util.module_from_spec(spec)
sys.modules["run_ablations"] = run_ablations
spec.loader.exec_module(run_ablations)

STRATEGIES = ("H", "R", "CF", "RO")
BASE_PROMPTS = {
    "H": "prompts/highlighting_explain.txt",
    "R": "prompts/rationale_explain.txt",
    "CF": "prompts/counterfactual_explain.txt",
    "RO": "prompts/rank_ordering_explain.txt",
}
# Slots each strategy's template must expose, matching format_alt_prompt's call.
REQUIRED_SLOTS = {
    "H": {"predicted_label", "input_text"},
    "R": {"predicted_label", "input_text"},
    "CF": {"predicted_label", "input_text", "other_labels_quoted", "other_labels"},
    "RO": {"predicted_label", "input_text"},
}
JSON_KEY = {"H": '"salience"', "R": '"rationale"', "CF": '"rewritten"', "RO": '"ranking"'}


def _slots(text):
    """Format slots in a template, ignoring the doubled braces of the JSON example."""
    return {f[1] for f in string.Formatter().parse(text) if f[1]}


def _read(rel):
    return (REPO / rel).read_text(encoding="utf-8")


def test_variant_sets_cover_every_strategy():
    assert set(run_ablations.ALT_PROMPT_SETS) == {"alt", "alt2", "alt3"}
    for variant, mapping in run_ablations.ALT_PROMPT_SETS.items():
        assert set(mapping) == set(STRATEGIES), variant


def test_every_variant_template_exists_and_is_nonempty():
    for variant, mapping in run_ablations.ALT_PROMPT_SETS.items():
        for s, rel in mapping.items():
            p = REPO / rel
            assert p.exists(), f"{variant}/{s}: missing {rel}"
            assert p.read_text(encoding="utf-8").strip(), f"{variant}/{s}: empty"


def test_variants_preserve_format_slots():
    """A missing slot would raise KeyError mid-run, after API spend."""
    for variant, mapping in run_ablations.ALT_PROMPT_SETS.items():
        for s, rel in mapping.items():
            assert _slots(_read(rel)) == REQUIRED_SLOTS[s], f"{variant}/{s}"


def test_variants_preserve_json_schema():
    """Same response key as the base prompt, so the frozen parsers still apply."""
    for variant, mapping in run_ablations.ALT_PROMPT_SETS.items():
        for s, rel in mapping.items():
            assert JSON_KEY[s] in _read(rel), f"{variant}/{s} lost {JSON_KEY[s]}"
            assert "Return only valid JSON" in _read(rel), f"{variant}/{s}"


def test_variants_are_actually_different_wordings():
    """The point of the expansion is independent rewordings: every variant must
    differ from the base prompt and from every other variant."""
    for s in STRATEGIES:
        texts = {"base": _read(BASE_PROMPTS[s])}
        for variant, mapping in run_ablations.ALT_PROMPT_SETS.items():
            texts[variant] = _read(mapping[s])
        seen = {}
        for name, t in texts.items():
            norm = " ".join(t.split())
            assert norm not in seen, f"{s}: {name} duplicates {seen.get(norm)}"
            seen[norm] = name


def test_resolve_paraphrase():
    assert run_ablations.resolve_paraphrase(None) == "alt"
    assert run_ablations.resolve_paraphrase("alt2") == "alt2"
    assert run_ablations.resolve_paraphrase("alt3") == "alt3"
    with pytest.raises(ConfigurationError):
        run_ablations.resolve_paraphrase("nope")


def test_back_compat_alias_unchanged():
    """Existing call sites read ALT_PROMPTS; it must stay the original set."""
    assert run_ablations.ALT_PROMPTS == run_ablations.ALT_PROMPT_SETS["alt"]
    assert run_ablations.ALT_PROMPTS["H"] == "prompts/highlighting_alt.txt"


def test_variant_templates_format_without_error():
    """Render each template with representative values, as the runner will."""
    sample = dict(predicted_label="positive", input_text="a fine film",
                  other_labels_quoted='"negative"', other_labels="negative")
    for variant, mapping in run_ablations.ALT_PROMPT_SETS.items():
        for s, rel in mapping.items():
            out = _read(rel).format(**{k: sample[k] for k in REQUIRED_SLOTS[s]})
            assert "{" in out and "}" in out, f"{variant}/{s}: JSON example lost"
            assert "positive" in out
