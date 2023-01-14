"""Tests for a Lexicon of Words."""
import pytest
from core.lexicon import Lexicon, Word, WordField
from core.change_history_item import ChangeHistoryItem


class TestAnEmptyLexiconShould:
    """Test operations on an empty Lexicon (0 words)"""
    def test__lex_ist_00__be_able_to_be_instantiated(self):
        """State Test"""
        empty_lexicon = Lexicon()
        assert empty_lexicon

    def test_have_a_default_but_valid_title(self):
        """Placeholder: State Test"""
        empty_lexicon = Lexicon()
        assert empty_lexicon.title

    def test_have_a_default_unique_identifier(self):
        """Placeholder: State Test"""
        first_lexicon = Lexicon()
        second_lexicon = Lexicon()
        assert first_lexicon.uuid
        assert first_lexicon.uuid != second_lexicon.uuid

    def test_return_an_empty_list_when_all_words_are_requested(self):
        """State Test"""
        empty_lexicon = Lexicon()
        assert not empty_lexicon.get_all_words()

    def test_return_an_item_when_an_entry_is_created_and_get_all_words(self):
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

    def test_return_true_when_validating_symbology_with_correct_characters(self):
        """Return - True if the string only contains allowed characters for a Word."""
        assert Lexicon().validate_for_word_field(
            "Etymological Symbology",
            "|b|ac|de|ifo|g|h|j|k|l|m|n|p|q|r|s|sh|tu|th|v|w|x|y|z|aab|aaba|aabaa[]")

    def test_return_false_when_validating_symbology_with_invalid_characters_in_valid_groups(self):
        """Return - False if the string contains non-alphanumeric or non delimeters."""
        invalid_characters = '!"£$%^&*()_-={}~#:;@<,>.?\\/'
        for test_character in invalid_characters:
            assert not Lexicon().validate_for_word_field(
                "Etymological Symbology",
                f"|aba|d{test_character}|")

    def test_return_false_including_valid_characters_in_invalid_groups(self):
        """Return - False if the string contains invalid group structures"""
        invalid_groups = ['a', 'e', 'i', 'o', 'u', 'aa', 'bc']
        for test_group in invalid_groups:
            assert Lexicon().validate_for_word_field(
                field_name="Etymological Symbology",
                to_validate=f"|{test_group}|") is False

    def test__return_none_when_validating_for_an_extant_word_field_with_no_validator(self):
        """Return - None if the field has no validator."""
        assert Lexicon().validate_for_word_field(
            field_name="Translated Word",
            to_validate="abcde") is None


class TestModifyingWordFieldsShould:
    """Test operations for a Lexicon and the linked changes when changing field values"""
    def test__setting_a_field_successfully_sets_the_word_change_flag_to_true(self):
        """Flag value is true and has changed after being successfully set"""
        new_lexicon = Lexicon()
        new_word = Word()
        new_lexicon.add_entry(new_word)
        status_before = new_word.has_unresolved_modification
        new_lexicon.set_field_to_value("Etymological Symbology", new_word, "|abu|da|")
        status_after = new_word.has_unresolved_modification
        assert status_after != status_before
        assert status_after

    # def test__setting_a_field_unsuccessfully_does_not_change_the_word_flag(self):
    #     """Flag value is true and has changed after being successfully set"""
    #     new_lexicon = Lexicon()
    #     new_word = Word()
    #     new_lexicon.add_entry(new_word)
    #     status_before = new_word.has_unresolved_modification
    #     with pytest.raises(Exception) as e_info:
    #         new_lexicon.set_field_to_value("Etymological Symbology", new_word, "|abu!da|")
    #     status_after = new_word.has_unresolved_modification
    #     assert status_after == status_before
    #     assert e_info.type == ValueError

    def test__setting_a_field_successfully_adds_to_the_version_history(self):
        """Version History is longer after a field is successfully set"""
        new_lexicon = Lexicon()
        new_word = Word()
        new_lexicon.add_entry(new_word)
        history_before = new_word.find_data_on(WordField.VERSIONHISTORY)
        new_lexicon.set_field_to_value("Etymological Symbology", new_word, "|abu|da|")
        history_after = new_word.find_data_on(WordField.VERSIONHISTORY)
        assert len(history_before) < len(history_after)

    # def test__setting_a_field_unsuccessfully_does_not_add_to_the_version_history(self):
    #     """Version History is the same length after a field is unsuccessfully set"""
    #     new_lexicon = Lexicon()
    #     new_word = Word()
    #     new_lexicon.add_entry(new_word)
    #     history_before = new_word.find_data_on(WordField.VERSIONHISTORY)
    #     with pytest.raises(Exception) as e_info:
    #         new_lexicon.set_field_to_value("Etymological Symbology", new_word, "|abu!da|")
    #     history_after = new_word.find_data_on(WordField.VERSIONHISTORY)
    #     assert history_before == history_after
    #     assert e_info.type == ValueError


class TestRetrievingWordChildrenShould:
    """Test operations for a Lexicon and Word cases"""
    def test__return_an_empty_list_for_a_childless_word(self):
        """A word with no children will return an empty list"""
        new_lexicon = Lexicon()
        new_word = Word()
        new_lexicon.add_entry(new_word)
        assert not new_lexicon.get_children_of(new_word)
        assert isinstance(new_lexicon.get_children_of(new_word), list)

    def test__return_a_single_item_list_for_a_parent_word(self):
        """BORK"""
        new_lexicon = Lexicon()
        parent_word = Word(merge_data={"translated_word": "Parent"})
        new_lexicon.add_entry(parent_word)
        child_word = Word(merge_data={"translated_word_components": ["Parent"]})
        new_lexicon.add_entry(child_word)
        assert new_lexicon.get_children_of(parent_word) == [child_word]

    def test__return_multi_item_list_for_child_with_sibling(self):
        """BORK"""
        new_lexicon = Lexicon()
        parent_word = Word(merge_data={"translated_word": "Parent"})
        new_lexicon.add_entry(parent_word)
        first_child_word = Word(merge_data={"translated_word_components": ["Parent"]})
        second_child_word = Word(merge_data={"translated_word_components": ["Parent"]})
        new_lexicon.add_entry(first_child_word)
        new_lexicon.add_entry(second_child_word)
        assert new_lexicon.get_children_of(parent_word).count(first_child_word) == 1
        assert new_lexicon.get_children_of(parent_word).count(second_child_word) == 1

    def test_return_all_descendents_for_grandparent_word(self):
        """BORK"""
        new_lexicon = Lexicon()
        grandparent_word = Word(merge_data={
            "translated_word": "Grandparent"})
        new_lexicon.add_entry(grandparent_word)
        parent_word = Word(merge_data={
            "translated_word": "Parent", "translated_word_components": ["Grandparent"]})
        new_lexicon.add_entry(parent_word)
        child_word = Word(merge_data={
            "translated_word_components": ["Parent"]})
        new_lexicon.add_entry(child_word)
        assert new_lexicon.get_descendants_of(grandparent_word).count(parent_word) == 1
        assert new_lexicon.get_descendants_of(grandparent_word).count(child_word) == 1
        assert new_lexicon.get_descendants_of(parent_word).count(child_word) == 1


class TestAPopulatedLexiconShould:
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

    def test_retrieve_a_word_that_exists(self):
        """Placeholder: State Test"""
        lexicon = Lexicon()
        new_word = Word()
        new_word.set_field_to(WordField.TRANSLATEDWORD, "ATestWord")
        lexicon.add_entry(new_word)
        retrieved_word = lexicon.retrieve("ATestWord")
        assert new_word == retrieved_word

    def test_return_none_for_a_word_that_doesnt_exist(self):
        """Placeholder: State Test"""
        lexicon = Lexicon()
        new_word = Word()
        lexicon.add_entry(new_word)
        assert lexicon.retrieve("NotAValidEntry") is None

    def test__lex_cwd_00__accurately_retrieve_the_data_of_all_words_for_export(self):
        """Placeholder: State Test"""
        new_lexicon = Lexicon()
        first_new_word = Word()
        second_new_word = Word()
        new_lexicon.add_entry(first_new_word)
        new_lexicon.add_entry(second_new_word)
        export_data = new_lexicon.retrieve_export_data_for()
        assert first_new_word._data in export_data  # pylint: disable=protected-access
        assert second_new_word._data in export_data  # pylint: disable=protected-access

    def test__lex_mio_00__passes_data_from_selected_words(self, mocker):
        """Placeholder: Behaviour Test"""
        mock_service = mocker.patch(
            "services.lexicon_io_service.LexiconIOService.store_to",
            return_value=True)
        new_lexicon = Lexicon()
        first_new_word = Word()
        second_new_word = Word()
        new_lexicon.add_entry(first_new_word)
        new_lexicon.add_entry(second_new_word)
        new_lexicon.store_to("NotAFile")
        mock_service.assert_called_once()  # pylint: disable=protected-access

    def test_get_valid_field_for_extant_word_is_accurate(self):
        """State Test"""
        new_lexicon = Lexicon()
        new_word = Word()
        new_lexicon.add_entry(new_word)
        field_data = new_lexicon.get_field_for_word("Translated Word", new_word)
        assert field_data == new_word.find_data_on(WordField.TRANSLATEDWORD)

    def test_get_invalid_field_for_extant_word_throws(self):
        """State Test"""
        new_lexicon = Lexicon()
        new_word = Word()
        new_lexicon.add_entry(new_word)
        with pytest.raises(Exception) as e_info:
            new_lexicon.get_field_for_word("NotAField", new_word)
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
        new_lexicon.set_field_to_value("Translated Word", new_word, new_value)
        field_data = new_lexicon.get_field_for_word("Translated Word", new_word)
        assert field_data == new_value

    def test_it_can_be_stored_locally(self):
        """State Test"""
        new_lexicon = Lexicon()
        new_lexicon.create_entry()
        new_lexicon.store_to("TestLexicon")

    def test_it_can_be_read_from_local_storage(self):
        """State Test"""
        existing_lexicon = Lexicon()
        existing_lexicon.create_entry()
        existing_lexicon.store_to("TestLexicon")
        new_lexicon = Lexicon()
        new_lexicon.load_from("TestLexicon")

    def test_is_read_accurately_from_local_storage(self):
        """State Test"""
        lexicon_to_store = Lexicon()
        storeable_word = Word()
        print(f"Empty Lexicon      : {lexicon_to_store.members}")
        lexicon_to_store.add_entry(storeable_word)
        print(f"Lexicon after add  : {lexicon_to_store.members}")
        lexicon_to_store.store_to("TestLexicon")
        print(f"Lexicon after store: {lexicon_to_store.members}")
        for word in lexicon_to_store.members:
            print(f"Words Stored   : {word.find_data_on(WordField.TRANSLATEDWORD)}")
        read_lexicon = Lexicon()
        print(f"Empty Read Lexicon : {read_lexicon.members}")
        read_lexicon.load_from("TestLexicon")
        print(f"Read Lexicon After : {read_lexicon.members}")
        for word in read_lexicon.members:
            print(f"Words Unpacked  : {word.find_data_on(WordField.TRANSLATEDWORD)}")
        assert read_lexicon.get_all_words() == [storeable_word]

    def test__change_etymological_symbology_for_word_with_valid_input(self):
        """An input of valid characters with valid structure will change the value of the field"""
        new_lexicon = Lexicon()
        new_word = Word({"etymological_symbology": "|aba|et|"})
        new_lexicon.add_entry(new_word)
        new_lexicon.set_field_to_value("Etymological Symbology", new_word, "|ino|mu|")
        assert new_lexicon.get_field_for_word("Etymological Symbology", new_word) == "|ino|mu|"

    # def test__not_change_etymological_symbology_for_word_with_invalidly_structured_input(self):
    #     """An input of valid characters with invalid structure will not change the field value"""
    #     new_lexicon = Lexicon()
    #     new_word = Word({"etymological_symbology": "|aba|et|"})
    #     new_lexicon.add_entry(new_word)
    #     with pytest.raises(Exception) as e_info:
    #         new_lexicon.set_field_to_value("Etymological Symbology", new_word, "|inomu|")
    #     assert new_lexicon.get_field_for_word("Etymological Symbology", new_word) == "|aba|et|"
    #     assert e_info.type == ValueError

    # def test__not_change_etymological_symbology_for_word_input_with_invalid_characters(self):
    #     """An input of invalid characters with valid structure will not change the field value"""
    #     new_lexicon = Lexicon()
    #     new_word = Word({"etymological_symbology": "|aba|et|"})
    #     new_lexicon.add_entry(new_word)
    #     with pytest.raises(Exception) as e_info:
    #         new_lexicon.set_field_to_value("Etymological Symbology", new_word, "|ino!mu|")
    #     assert new_lexicon.get_field_for_word("Etymological Symbology", new_word) == "|aba|et|"
    #     assert e_info.type == ValueError


class TestResolvingChangesOnAWordShould:
    """Test operations on resolving change history items."""
    def test__succeed_if_both_the_change_and_word_exist(self):
        """Happy path - A change is resolved successfully."""
        new_lexicon = Lexicon()
        new_word = new_lexicon.create_entry()
        new_lexicon.add_entry(new_word)
        new_lexicon.set_field_to_value("In Language Word", new_word, "NotAWord")
        new_lexicon.resolve_modification_flags()
        assert new_word.has_unresolved_modification
        unresolved_id = new_word.find_data_on(WordField.VERSIONHISTORY)
        change_item = new_lexicon.changehistory.find_item_with_id(unresolved_id[0])
        new_lexicon.resolve_change_for(change_item, new_word)
        new_lexicon.resolve_modification_flags()
        assert not new_word.has_unresolved_modification

    def test__fail_if_the_word_and_change_are_mismatched(self):
        """Error path - A non-existant change cannot be resolved."""
        new_lexicon = Lexicon()
        new_word = new_lexicon.create_entry()
        new_lexicon.add_entry(new_word)
        new_lexicon.set_field_to_value("In Language Word", new_word, "NotAWord")
        new_lexicon.resolve_modification_flags()
        assert new_word.has_unresolved_modification
        false_change_item = ChangeHistoryItem(
            "NotTheRightChange",
            new_word.find_data_on(WordField.UID))
        new_lexicon.resolve_change_for(false_change_item, new_word)
        new_lexicon.resolve_modification_flags()
        assert new_word.has_unresolved_modification
