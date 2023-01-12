# import pytest
from core.core import WordField
from core.wordflow import Wordflow
from core.word import Word


class TestAnEmptyWordflowShould:
    def test__be_able_to_be_constructed(self):
        assert Wordflow()


class TestTheBaseWordFlowShould:
    def test__select_the_root_path_for_a_word_with_no_parents(self):
        baseflow = Wordflow()
        orphan_word = Word()
        assert ("WORD IS ROOT") in baseflow.run_stages(orphan_word)

    def test__select_the_combined_path_for_a_word_with_parents(self):
        baseflow = Wordflow()
        word = Word({"translated_word_components": ["One", "Two"]})
        assert ("WORD IS COMBINED") in baseflow.run_stages(word)

    def test__pass_for_a_combined_word_that_does_not_fail_stages(self):
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"]})
        stage_results = baseflow.run_stages(word)
        for result in stage_results:
            if isinstance(result, tuple):
                assert result[-1] is True

    def test__fail_for_a_combined_word_that_fails_translatedword_stage(self):
        baseflow = Wordflow()
        word = Word({
            "translated_word_components": ["One", "Two"]})
        word.set_field_to(WordField.TRANSLATEDWORD, "")
        stage_results = baseflow.run_stages(word)
        tuple_results = [x[-1] for x in stage_results if isinstance(x, tuple)].count(False)
        assert tuple_results == 1

    def test__pass_for_a_combined_word_that_fails_translated_components_stage(self):
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["", "Two"]})
        stage_results = baseflow.run_stages(word)
        tuple_results = [x[-1] for x in stage_results if isinstance(x, tuple)].count(False)
        assert tuple_results == 1
