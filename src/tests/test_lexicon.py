"""Tests for a Lexicon of Words."""
import pytest
from core.lexicon import Lexicon, Word


class TestAnEmptyWordShould:
    """Test operations for an empty Word"""
    def test__wrd_ist_00__be_able_to_be_instantiated(self):
        """State Test"""
        empty_word = Word()
        assert empty_word

    def test__wrd_ist_01__merges_in_parameter_data(self):
        """State Test"""
        init_data = {
            "translated_word": "NotAWord",
            "translated_word_components": ["Not", "A", "Word"],
            "in_language_components": ["Ton", "A", "Drow"],
            "etymological_symbology": None,
            "compiled_symbology": None,
            "symbol_mapping": ["A", "B", "C"],
            "symbol_selection": ["D", "E", "F"],
            "symbol_pattern_selected": None,
            "rules_applied": None,
            "in_language_word": "TonADrow",
            "version_history": {"Here": "Today"},
            "has_been_modified_since_last_resolve": True,  # "Ripple" resolution
            "has_modified_ancestor": False}
        word = Word(init_data)
        for (fieldname, fieldvalue) in init_data.items():
            assert word.find_data_on(fieldname) == fieldvalue

    def test_return_true_when_validating_symbology_with_correct_characters(self):
        """Return - True if the string only contains alphanumeric characters and '|', ']', '['."""
        assert Word().validate_for_field(
            "etymological_symbology",
            "abcdefghijklmnopqrstuvwxyz|[]")

    def test_return_false_when_validating_symbology_including_invalid_characters(self):
        """Return - False if the string contains non-alphanumeric or non delimeters."""
        invalid_characters = '!"£$%^&*()_-+={}~#:;@<,>.?\\/'
        for test_character in invalid_characters:
            assert not Word().validate_for_field(
                "etymological_symbology",
                f"abcdef{test_character}")

    def test_return_none_when_validating_for_an_extant_field_with_no_validator(self):
        """Return - None if the field has no validator."""
        assert Word().validate_for_field(
            field_name="translated_word",
            to_validate="abcde") is None


class TestAPopulatedWordShould:
    """Test operations for a Word with populated fields"""
    def test__wrd_dio_00__return_internal_data_accurately(self):
        """State Test"""
        init_data = {
            "translated_word": "NotAWord",
            "translated_word_components": ["Not", "A", "Word"],
            "in_language_components": ["Ton", "A", "Drow"],
            "symbol_mapping": ["A", "B", "C"],
            "symbol_selection": ["D", "E", "F"],
            "in_language_word": "TonADrow",
            "version_history": {"Here": "Today"},
            "has_been_modified_since_last_resolve": True,  # "Ripple" resolution
            "has_modified_ancestor": False}
        word = Word(init_data)
        returned_data = word.data_for_export()
        for (fieldname, fieldvalue) in init_data.items():
            assert returned_data[fieldname] == fieldvalue


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
            "etymological_symbology",
            "abcdefghijklmnopqrstuvwxyz|[]")

    def test_return_false_when_validating_symbology_including_invalid_characters(self):
        """Return - False if the string contains non-alphanumeric or non delimeters."""
        invalid_characters = '!"£$%^&*()_-+={}~#:;@<,>.?\\/'
        for test_character in invalid_characters:
            assert not Lexicon().validate_for_word_field(
                "etymological_symbology",
                f"abcdef{test_character}")

    def test_return_none_when_validating_for_an_extant_word_field_with_no_validator(self):
        """Return - None if the field has no validator."""
        assert Lexicon().validate_for_word_field(
            field_name="translated_word",
            to_validate="abcde") is None


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
        new_word.set_field_to("translated_word", "ATestWord")
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
        field_data = new_lexicon.get_field_for_word("translated word", new_word)
        assert field_data == new_word.find_data_on("translated_word")

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
        new_lexicon.set_field_to_value("translated word", new_word, new_value)
        field_data = new_lexicon.get_field_for_word("translated word", new_word)
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
            print(f"Words Stored   : {word.find_data_on('translated_word')}")
        read_lexicon = Lexicon()
        print(f"Empty Read Lexicon : {read_lexicon.members}")
        read_lexicon.load_from("TestLexicon")
        print(f"Read Lexicon After : {read_lexicon.members}")
        for word in read_lexicon.members:
            print(f"Words Unpacked  : {word.find_data_on('translated_word')}")
        assert read_lexicon.get_all_words() == [storeable_word]
