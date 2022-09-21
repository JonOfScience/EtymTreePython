"""Tests for a Lexicon of Words."""
from lib.core import Lexicon


class TestGivenEmptyLexicon:
    """Test operations on an empty lexicon (0 words)"""
    def test_when_all_words_are_requested_then_an_empty_list_is_returned(self):
        """State Test"""
        empty_lexicon = Lexicon()
        assert empty_lexicon.get_all_words() == []
