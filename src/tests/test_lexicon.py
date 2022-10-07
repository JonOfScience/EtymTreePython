"""Tests for a Lexicon of Words."""
import pytest
from lib.core import Lexicon, Word


class TestGivenEmptyLexicon:
    """Test operations on an empty lexicon (0 words)"""
    def test_when_all_words_are_requested_then_an_empty_list_is_returned(self):
        """State Test"""
        empty_lexicon = Lexicon()
        assert empty_lexicon.get_all_words() == []

    def test_when_an_entry_is_created_all_words_returns_an_item(self):
        """State Test"""
        new_lexicon = Lexicon()
        new_lexicon.create_entry()
        assert len(new_lexicon.get_all_words()) == 1

    def test_when_an_entry_is_created_all_words_returns_the_created_item(self):
        """State Test"""
        new_lexicon = Lexicon()
        new_word = Word()
        new_lexicon.add_entry(new_word)
        assert new_lexicon.get_all_words() == [new_word]

class TestGivenPopulatedLexicon:
    """Test operations on a lexicon with more than 1 word (1+ words)"""
    def test_when_all_words_are_requested_then_a_list_of_the_items_is_returned(self):
        """State Test"""
        new_lexicon = Lexicon()
        first_new_word = Word()
        second_new_word = Word()
        new_lexicon.add_entry(first_new_word)
        new_lexicon.add_entry(second_new_word)
        assert first_new_word in new_lexicon.get_all_words()
        assert second_new_word in new_lexicon.get_all_words()

    def test_get_valid_field_for_extant_word_is_accurate(self):
        """State Test"""
        new_lexicon = Lexicon()
        new_word = Word()
        new_lexicon.add_entry(new_word)
        field_data = new_lexicon.get_field_for_word("translated word", new_word.translated_word)
        assert field_data == new_word.translated_word

    def test_get_invalid_field_for_extant_word_throws(self):
        """State Test"""
        new_lexicon = Lexicon()
        new_word = Word()
        new_lexicon.add_entry(new_word)
        with pytest.raises(Exception) as e_info:
            new_lexicon.get_field_for_word("NotAField", new_word.translated_word)
        assert e_info.type == ValueError

    def test_get_valid_field_for_non_existant_word_throws(self):
        """State Test"""
        new_lexicon = Lexicon()
        with pytest.raises(Exception) as e_info:
            new_lexicon.get_field_for_word("translated_word", "NotAWord")
        assert e_info.type == KeyError

    def test_can_set_valid_field_for_extant_word(self):
        """State Test"""
        new_lexicon = Lexicon()
        new_word = Word()
        new_lexicon.add_entry(new_word)
        new_value = "ThisIsAWord"
        new_lexicon.set_field_to_value("translated word", new_word.translated_word, new_value)
        field_data = new_lexicon.get_field_for_word("translated word", new_word.translated_word)
        assert field_data == new_value

    # def test_get_invalid_field_for_extant_word_throws(self):
    #     """State Test"""
    #     new_lexicon = Lexicon()
    #     new_word = Word()
    #     new_lexicon.add_entry(new_word)
    #     with pytest.raises(Exception) as e_info:
    #         new_lexicon.get_field_for_word("NotAField", new_word.translated_word)
    #     assert e_info.type == ValueError

    # def test_get_valid_field_for_non_existant_word_throws(self):
    #     """State Test"""
    #     new_lexicon = Lexicon()
    #     with pytest.raises(Exception) as e_info:
    #         new_lexicon.get_field_for_word("translated_word", "NotAWord")
    #     assert e_info.type == KeyError
