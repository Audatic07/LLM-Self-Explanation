import json
import pytest
from unittest.mock import patch
from src.parsing.parser import Parser, ensure_spacy_available
from src.normalization.normalizer import Normalizer
from src.utils.exceptions import ParsingError


@pytest.fixture
def parser():
    return Parser()


@pytest.fixture
def normalizer():
    return Normalizer()


class TestEnsureSpacyAvailable:
    def test_passes_when_spacy_available(self):
        with patch('src.parsing.parser._get_spacy', return_value=object()):
            ensure_spacy_available()  # must not raise

    def test_raises_when_spacy_unavailable(self):
        with patch('src.parsing.parser._get_spacy', return_value=None):
            with pytest.raises(RuntimeError, match="spaCy"):
                ensure_spacy_available()


class TestParseClassification:
    def test_valid_json(self, parser):
        label = parser.parse_classification(
            '{"label":"positive"}', ["positive", "negative"]
        )
        assert label == "positive"

    def test_json_in_code_fence(self, parser):
        resp = '```json\n{"label":"entailment"}\n```'
        label = parser.parse_classification(resp, ["entailment", "neutral", "contradiction"])
        assert label == "entailment"

    def test_json_surrounded_by_text(self, parser):
        resp = 'Here is my answer: {"label":"Sci/Tech"}'
        label = parser.parse_classification(resp, ["World", "Sports", "Business", "Sci/Tech"])
        assert label == "Sci/Tech"

    def test_label_not_in_set_raises(self, parser):
        with pytest.raises(Exception):
            parser.parse_classification('{"label":"invalid"}', ["positive", "negative"])

    def test_empty_response_raises(self, parser):
        with pytest.raises(Exception):
            parser.parse_classification("", ["positive", "negative"])

    def test_non_json_response_raises(self, parser):
        with pytest.raises(Exception):
            parser.parse_classification("Prediction: positive", ["positive", "negative"])


class TestParseHighlighting:
    def test_valid_salience(self, parser, normalizer):
        input_text = "This movie was great and wonderful and amazing."
        tokens = parser.parse_highlighting(
            '{"salience":{"great":10,"wonderful":8,"amazing":5}}', input_text, normalizer
        )
        assert len(tokens) == 3
        assert "great" in tokens

    def test_salience_dynamic_k_scales_with_length(self, parser, normalizer):
        # Dynamic k = max(3, round(L/5)). 10 content words -> k=2 -> floored to 3.
        short_input = "one two three four five six seven eight nine ten"
        tokens = parser.parse_highlighting(
            '{"salience":{"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10}}',
            short_input, normalizer
        )
        assert tokens == ["ten", "nine", "eight"]

        # 25 content words -> round(25/5)=5.
        words = [f"w{i}" for i in range(25)]
        long_input = " ".join(words)
        salience = {w: i + 1 for i, w in enumerate(words)}
        tokens_long = parser.parse_highlighting(
            json.dumps({"salience": salience}), long_input, normalizer
        )
        assert len(tokens_long) == 5
        assert tokens_long[0] == "w24"

    def test_salience_dynamic_k_capped_by_valid_count(self, parser, normalizer):
        # Long input but only 3 valid scored tokens -> k cannot exceed 3.
        long_input = " ".join(f"w{i}" for i in range(40)) + " great wonderful amazing"
        tokens = parser.parse_highlighting(
            '{"salience":{"great":10,"wonderful":8,"amazing":5}}', long_input, normalizer
        )
        assert len(tokens) == 3

    def test_salience_unanchored_discarded(self, parser, normalizer):
        result = parser.parse_highlighting(
            '{"salience":{"great":10,"nonexistent":8,"amazing":5}}',
            "This is great and amazing", normalizer
        )
        assert len(result) == 2
        assert "great" in result
        # H tokens are returned in the shared normalized token space (v3.0 lemmas):
        # "amazing" -> "amaze"
        assert "amaze" in result

    def test_too_few_valid_raises(self, parser, normalizer):
        with pytest.raises(Exception):
            parser.parse_highlighting(
                '{"salience":{"great":10}}', "great wonderful", normalizer
            )

    def test_empty_response_raises(self, parser, normalizer):
        with pytest.raises(Exception):
            parser.parse_highlighting("", "some input text", normalizer)


class TestParseRationale:
    def test_valid_rationale(self, parser, normalizer):
        input_text = "The acting was superb and the plot compelling."
        rationale, evidence = parser.parse_rationale(
            '{"rationale":"The acting was superb and the plot compelling."}',
            input_text, normalizer
        )
        assert "superb" in rationale or "acting" in rationale
        assert len(evidence) >= 2

    def test_unanchored_rationale_raises(self, parser, normalizer):
        """Rationale sentence with no dependency tokens that anchor into input text."""
        with pytest.raises(Exception):
            parser.parse_rationale(
                '{"rationale":"This is completely unrelated."}',
                "Great movie", normalizer
            )

    def test_empty_rationale_raises(self, parser, normalizer):
        with pytest.raises(Exception):
            parser.parse_rationale(
                '{"rationale":""}',
                "Great movie", normalizer
            )

    def test_content_words_kept_function_words_dropped(self, parser, normalizer):
        """Open-class POS extraction keeps content-word lemmas and drops function words."""
        input_text = "The brilliant director crafted a stunning film."
        _, evidence = parser.parse_rationale(
            '{"rationale":"The brilliant director crafted a stunning film."}',
            input_text, normalizer
        )
        # Content words (lemmas) present; function words absent.
        assert "director" in evidence
        assert "film" in evidence
        for fn in ("the", "a", "and", "was"):
            assert fn not in evidence

    def test_introduced_concepts_tracked(self, parser, normalizer):
        """Rationale concepts absent from the input are surfaced as introduced
        concepts (post-hoc rationalization signal), not silently dropped."""
        input_text = "The movie was great."
        rationale, evidence = parser.parse_rationale(
            '{"rationale":"The great movie felt boring overall."}',
            input_text, normalizer
        )
        introduced = parser._r_introduced
        assert isinstance(introduced, list)
        # Partition invariant: anchored evidence is in the input; introduced is not.
        for tok in evidence:
            assert normalizer.is_anchored(tok, input_text)
        for tok in introduced:
            assert not normalizer.is_anchored(tok, input_text)
        # 'boring' is a salient concept absent from the input → should be introduced.
        assert any(t.startswith("bor") for t in introduced)


class TestParseCounterfactual:
    def test_valid_counterfactual(self, parser, normalizer):
        input_text = "This movie was great."
        cf_text, new_pred, from_tokens = parser.parse_counterfactual(
            '{"rewritten":"This movie was terrible.","new_prediction":"negative"}',
            input_text, "positive", ["positive", "negative"], normalizer
        )
        assert cf_text == "This movie was terrible."
        assert new_pred == "negative"
        assert "great" in from_tokens

    def test_insertion_only_flip_has_no_original_attribution(self, parser, normalizer):
        # Flipping by inserting "not" changes the text but replaces/deletes no original
        # token, so there is no original-token attribution -> raises (not "identical").
        with pytest.raises(ParsingError, match="insertion"):
            parser.parse_counterfactual(
                '{"rewritten":"This movie was not great.","new_prediction":"negative"}',
                "This movie was great.", "positive", ["positive", "negative"], normalizer,
                skip_validation=True
            )

    def test_no_flip_raises(self, parser, normalizer):
        with pytest.raises(Exception):
            parser.parse_counterfactual(
                '{"rewritten":"This movie was awesome.","new_prediction":"positive"}',
                "This movie was great.", "positive", ["positive", "negative"], normalizer
            )

    def test_invalid_label_raises(self, parser, normalizer):
        with pytest.raises(Exception):
            parser.parse_counterfactual(
                '{"rewritten":"This movie was terrible.","new_prediction":"invalid"}',
                "This movie was great.", "positive", ["positive", "negative"], normalizer
            )

    def test_edit_ratio_too_high_raises(self, parser, normalizer):
        with pytest.raises(Exception):
            parser.parse_counterfactual(
                '{"rewritten":"This car was terrible.","new_prediction":"negative"}',
                "This movie was great.", "positive", ["positive", "negative"], normalizer,
                max_edit_ratio=0.3
            )

    def test_null_rewritten_raises(self, parser, normalizer):
        with pytest.raises(Exception):
            parser.parse_counterfactual(
                '{"rewritten":null,"new_prediction":null}',
                "This movie was great.", "positive", ["positive", "negative"], normalizer
            )

    def test_non_string_rewritten_raises_parsing_error(self, parser, normalizer):
        # Some models emit an object/list for "rewritten". This must raise ParsingError
        # (so only CF is invalidated), NOT AttributeError (which escapes the caller's
        # handler and would kill the whole instance).
        for bad in ('{"rewritten":{"text":"x"},"new_prediction":"negative"}',
                    '{"rewritten":["a","b"],"new_prediction":"negative"}'):
            with pytest.raises(ParsingError):
                parser.parse_counterfactual(
                    bad, "This movie was great.", "positive",
                    ["positive", "negative"], normalizer
                )

    def test_identical_text_raises(self, parser, normalizer):
        with pytest.raises(Exception):
            parser.parse_counterfactual(
                '{"rewritten":"This movie was great.","new_prediction":"negative"}',
                "This movie was great.", "positive", ["positive", "negative"], normalizer
            )


class TestParseRankOrdering:
    def test_valid_ranking(self, parser, normalizer):
        input_text = "the quick brown fox jumps over the lazy dog"
        tokens = parser.parse_rank_ordering(
            '{"ranking":["quick","brown","fox","jumps","lazy"]}',
            input_text, normalizer
        )
        assert len(tokens) == 5
        assert tokens[0] == ("quick", 1)
        assert tokens[4] == ("lazy", 5)

    def test_too_few_items_raises(self, parser, normalizer):
        with pytest.raises(Exception):
            parser.parse_rank_ordering(
                '{"ranking":["quick","brown"]}',
                "the quick brown fox", normalizer
            )

    def test_not_anchored_raises(self, parser, normalizer):
        with pytest.raises(Exception):
            parser.parse_rank_ordering(
                '{"ranking":["quick","nonexistent1","nonexistent2"]}',
                "the quick brown fox", normalizer
            )


class TestWordEditRatio:
    def test_identical_texts(self, parser):
        assert parser._word_edit_ratio("hello world", "hello world") == 0.0

    def test_one_word_change(self, parser):
        r = parser._word_edit_ratio("hello world", "hello there")
        assert 0.0 < r < 0.6

    def test_completely_different(self, parser):
        r = parser._word_edit_ratio("hello world", "foo bar baz")
        assert r > 0.5

    def test_empty_both(self, parser):
        assert parser._word_edit_ratio("", "") == 0.0

    def test_one_empty(self, parser):
        assert parser._word_edit_ratio("hello", "") == 1.0

    def test_normalized_by_original_length(self, parser):
        # MiCE: distance / len(original), not / max(n, m). One insertion into a
        # 2-word original => 1/2 = 0.5 (would be 1/3 under the old max(n,m) denom).
        assert parser._word_edit_ratio("hello world", "hello big world") == 0.5


class TestExtractJson:
    def test_direct_json(self, parser):
        assert parser._extract_json('{"a":1}') == {"a": 1}

    def test_code_fence(self, parser):
        result = parser._extract_json('```json\n{"a":1}\n```')
        assert result == {"a": 1}

    def test_surrounding_text(self, parser):
        result = parser._extract_json('Answer: {"a":1} done')
        assert result == {"a": 1}

    def test_invalid_json_returns_none(self, parser):
        assert parser._extract_json("not json") is None

    def test_repairs_unescaped_inner_quotes(self, parser):
        # Real failure mode: a rationale value that quotes a phrase from the text,
        # leaving unescaped double quotes that break strict json.loads.
        raw = ('{"rationale":"The film as being "as seductive as it is haunting" '
               'implies a captivating quality."}')
        obj = parser._extract_json(raw)
        assert obj is not None
        assert obj["rationale"].startswith("The film as being")
        assert "seductive" in obj["rationale"]

    def test_repair_preserves_legit_inner_quotes_in_rewrite(self, parser):
        raw = '{"rewritten":"he said "hello" loudly","new_prediction":"negative"}'
        obj = parser._extract_json(raw)
        assert obj == {"rewritten": 'he said "hello" loudly', "new_prediction": "negative"}

    def test_repair_does_not_corrupt_valid_json(self, parser):
        assert parser._extract_json('{"salience":{"a":2,"film":6}}') == {"salience": {"a": 2, "film": 6}}


class TestHighlightingSelection:
    def test_punctuation_only_keys_dropped_silently(self, parser, normalizer):
        # Model padding such as "(" and "." must never surface as evidence tokens.
        raw = ('{"salience":{"expect":6,"same-old":8,"lame-old":9,"slasher":7,'
               '"nonsense":8,"scenery":4,"(":1,".":1}}')
        text = "expect the same-old , lame-old slasher nonsense , just with different scenery ."
        result = parser.parse_highlighting(raw, text, normalizer)
        assert "(" not in result and "." not in result
        assert "lame-old" in result

    def test_topk_selects_content_words_not_stopwords(self, parser, normalizer):
        # Top-scored stopwords ("very","too") must not crowd out content words and
        # then vanish in normalization, leaving an erratically tiny H set.
        raw = ('{"salience":{"a":2,"very":8,"long":9,"movie":6,"dull":10,"too":9,'
               '"much":8,"stretches":8,"entirely":8,"focus":5}}')
        text = "a very long movie , dull in stretches , with entirely too much focus ."
        result = parser.parse_highlighting(raw, text, normalizer)
        norm = normalizer.normalize_tokens(result)
        assert "very" not in norm and "too" not in norm
        assert len(norm) >= 3  # content words survive instead of collapsing to 2


class TestRationaleInflectionAnchoring:
    def test_inflected_rationale_token_anchors(self, parser, normalizer):
        # Rationale lemma "scene" must anchor to input surface "scenes" (was dropped
        # as "unanchored", emptying the whole rationale evidence set).
        raw = ('{"rationale":"The scenes are emotionally powerful and the work has a '
               'profound impact on the viewer."}')
        text = "moved to tears by a couple of scenes , you have ice water in your veins"
        _, evidence = parser.parse_rationale(raw, text, normalizer)
        norm = normalizer.normalize_tokens(evidence)
        assert "scene" in norm


class TestCanonicalTokens:
    """Review P0.1: SST-2's curated text is Treebank-pretokenized ("you 're",
    "scenes ,"). A model that writes normal spacing ("you're", "scenes,") must
    canonicalize identically, or CF edit-ratio/diff charges phantom edits for
    spacing alone."""

    def test_detokenized_and_tokenized_forms_match(self, parser):
        tokenized = "you 're not going to enjoy this film ."
        detokenized = "you're not going to enjoy this film."
        assert parser._canonical_tokens(tokenized) == parser._canonical_tokens(detokenized)

    def test_comma_detached_regardless_of_spacing(self, parser):
        assert parser._canonical_tokens("scenes ,") == parser._canonical_tokens("scenes,")

    def test_negation_contraction_preserved_as_single_token(self, parser):
        # "n't" must survive as its own token (not fragmented into "n" + "'" + "t")
        # since the normalizer's POLARITY_WORDS whitelist matches it literally.
        assert parser._canonical_tokens("isn't") == ["is", "n't"]
        assert parser._canonical_tokens("is n't") == ["is", "n't"]

    def test_hyphenated_compound_kept_as_one_token(self, parser):
        assert parser._canonical_tokens("charm-less,") == ["charm-less", ","]

    def test_various_clitics_split_consistently(self, parser):
        assert parser._canonical_tokens("I've") == parser._canonical_tokens("I 've")
        assert parser._canonical_tokens("we'll") == parser._canonical_tokens("we 'll")
        assert parser._canonical_tokens("it's") == parser._canonical_tokens("it 's")


class TestCFTokenizationConfound:
    """Review P0.1 acceptance criteria: CF edit-ratio/diff must not be confounded by
    SST-2's Treebank pretokenization."""

    def test_pure_detokenization_rewrite_raises_identical(self, parser, normalizer):
        # A rewrite that ONLY de-tokenizes (no semantic edit) must be rejected as a
        # non-edit via the canonical-identity check, not fall through to a confusing
        # "insertion-only" message.
        tokenized = "you 're not going to enjoy this film ."
        detokenized_same = "you're not going to enjoy this film."
        raw = json.dumps({"rewritten": detokenized_same, "new_prediction": "negative"})
        with pytest.raises(ParsingError, match="identical"):
            parser.parse_counterfactual(
                raw, tokenized, "positive", ["positive", "negative"], normalizer,
                skip_validation=True,
            )

    def test_edit_ratio_on_detokenized_rewrite_counts_only_real_edit(self, parser):
        # One genuine word change ("enjoy"->"hate") plus a full de-tokenization must
        # cost ~1/9, not the ~0.6 a raw-whitespace-split diff would charge.
        tokenized = "you 're not going to enjoy this film ."
        detokenized_edit = "you're not going to hate this film."
        ratio = parser._word_edit_ratio(tokenized, detokenized_edit)
        assert ratio < 0.2

    def test_extract_changed_tokens_ignores_detokenization_noise(self, parser):
        tokenized = "you 're not going to enjoy this film ."
        detokenized_edit = "you're not going to hate this film."
        changed = parser._extract_changed_tokens(tokenized, detokenized_edit)
        assert changed == {"enjoy"}

    def test_sst2_style_full_rewrite_passes_edit_ratio_threshold(self, parser, normalizer):
        # Reproduces the pilot's sst2_validation_000665 shape: Treebank-tokenized
        # original, a detokenized rewrite with ONE real content edit. Previously this
        # kind of rewrite was rejected (ratio inflated by spacing alone); it must now
        # pass the standard 0.3 threshold.
        original = "you 're too old for this movie , you 've heard it all before ."
        rewritten = "you're just right for this movie, you've heard it all before."
        raw = json.dumps({"rewritten": rewritten, "new_prediction": "negative"})
        cf_text, new_pred, from_tokens = parser.parse_counterfactual(
            raw, original, "positive", ["positive", "negative"], normalizer,
            max_edit_ratio=0.3,
        )
        assert new_pred == "negative"
        assert "too" in from_tokens or "old" in from_tokens

    def test_mnli_span_path_unaffected_by_canonicalization(self, parser, normalizer):
        # MNLI span-restricted CF: Premise untouched, Hypothesis has a Treebank-style
        # rewrite with exactly one real edit. Ratio must be computed over the
        # editable span only, and canonicalization must not break span protection.
        original = ('Premise: A man is playing a guitar on stage . '
                    "Hypothesis: The man is n't performing music .")
        rewritten = ('Premise: A man is playing a guitar on stage . '
                    "Hypothesis: The man is performing music.")
        raw = json.dumps({"rewritten": rewritten, "new_prediction": "entailment"})
        cf_text, new_pred, from_tokens = parser.parse_counterfactual(
            raw, original, "contradiction", ["entailment", "neutral", "contradiction"],
            normalizer, max_edit_ratio=0.3, edit_span_marker="Hypothesis:",
        )
        assert new_pred == "entailment"
        assert "n't" in from_tokens

    def test_mnli_premise_edit_still_rejected_after_canonicalization(self, parser, normalizer):
        # Editing the Premise must still be a rules violation, canonicalization must
        # not accidentally make a changed Premise look "unchanged".
        original = ('Premise: A man is playing a guitar on stage . '
                    "Hypothesis: The man is n't performing music .")
        rewritten = ('Premise: A woman is playing a guitar on stage . '
                    "Hypothesis: The man is performing music.")
        raw = json.dumps({"rewritten": rewritten, "new_prediction": "entailment"})
        with pytest.raises(ParsingError, match="outside the allowed span"):
            parser.parse_counterfactual(
                raw, original, "contradiction", ["entailment", "neutral", "contradiction"],
                normalizer, max_edit_ratio=0.3, edit_span_marker="Hypothesis:",
            )
