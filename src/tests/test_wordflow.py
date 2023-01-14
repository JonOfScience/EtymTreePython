"""Test operations associated with word validity pipeline"""
# import pytest
from core.core import WordField
from core.wordflow import Wordflow
from core.word import Word


class TestAnEmptyWordflowShould:
    """Test operations on a empty Wordflow"""
    def test__be_able_to_be_constructed(self):
        """State Test: Placeholder"""
        assert Wordflow()


class TestTheBaseWordFlowShould:
    """Test operations for the system default Wordflow"""
    def test__select_the_root_path_for_a_word_with_no_parents(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        orphan_word = Word()
        assert "WORD IS ROOT" in baseflow.run_stages(orphan_word)

    def test__select_the_combined_path_for_a_word_with_parents(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({"translated_word_components": ["One", "Two"]})
        assert "WORD IS COMBINED" in baseflow.run_stages(word)

    def test__pass_for_a_combined_word_that_does_not_fail_stages(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba|et|"})
        baseflow.run_stages(word)
        assert baseflow.failed_stages() == 0

    def test__fail_for_a_combined_word_that_fails_translatedword_stage(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word_components": ["One", "Two"]})
        word.set_field_to(WordField.TRANSLATEDWORD, "")
        baseflow.run_stages(word)
        assert baseflow.failed_stages() == 1

    def test__fail_for_a_combined_word_that_fails_translated_components_stage(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["", "Two"]})
        baseflow.run_stages(word)
        assert baseflow.failed_stages() == 1

    def test__fail_for_a_combined_word_that_fails_in_language_components_stage(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["", "Two"]})
        baseflow.run_stages(word)
        assert baseflow.failed_stages() == 1

    def test__fail_for_a_combined_word_that_fails_etymological_symbology_stage(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|abaet|"})
        baseflow.run_stages(word)
        assert baseflow.failed_stages() == 1
