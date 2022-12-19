"""Component level tests for Word and LexiconChangeHistory below Lexicon level."""
from core.core import WordField
from core.word import Word
from core.lexicon import Lexicon
from core.change_history import LexiconChangeHistory

class TestGivenAModifiedWord:
    """Test functionality around distributed change tracking"""
    def test__when_a_field_is_changed__then_an_unresolved_self_modification_is_identified(self):
        """BORK"""
        test_history = LexiconChangeHistory()
        new_word = Word()
        change_item = new_word.set_field_to(WordField.TRANSLATEDWORD, "ATestWord")
        test_history.add_item(change_item)
        new_word.identify_unresolved_modifications(test_history)
        assert new_word.has_unresolved_modification

    def test__when_a_field_is_changed__then_ancestor_modifications_are_not_changed(self):
        """BORK"""
        test_history = LexiconChangeHistory()
        new_word = Word()
        change_item = new_word.set_field_to(WordField.TRANSLATEDWORD, "ATestWord")
        test_history.add_item(change_item)
        new_word.identify_unresolved_modifications(test_history)
        assert not new_word.has_modified_ancestor

    def test__when_an_ancestor_field_is_changed__then_no_unresolved_self_modification(self):
        """BORK"""
        test_history = LexiconChangeHistory()
        parent_word = Word(merge_data={"translated_word": "Parent"})
        child_word = Word(merge_data={"translated_word_components": ["Parent"]})
        change_item = parent_word.set_field_to(WordField.INLANGUAGEWORD, "droWtseTA")
        test_history.add_item(change_item)
        child_word.identify_unresolved_modifications(test_history)
        assert not child_word.has_unresolved_modification


    def test__when_an_ancestor_field_is_changed__then_unresolved_ancestor_modification(self):
        """BORK"""
        test_lexicon = Lexicon()
        parent_word = Word(merge_data={"translated_word": "Parent"})
        child_word = Word(merge_data={"translated_word_components": ["Parent"]})
        test_lexicon.add_entry(parent_word)
        test_lexicon.add_entry(child_word)
        test_lexicon.set_field_to_value("In Language Word", parent_word, "droWtseTA")
        assert child_word.has_modified_ancestor
