"""Tests for a single Word."""
from core.lexicon import Word, WordField


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
            "has_been_modified_since_last_resolve": True,
            "has_modified_ancestor": False}
        word = Word(init_data)
        for (fieldname, fieldvalue) in init_data.items():
            assert word._data[fieldname] == fieldvalue #pylint: disable=protected-access

    def test__return_none_when_validating_for_an_extant_field_with_no_validator(self):
        """Return - None if the field has no validator."""
        assert Word().validate_for_field(
            field_name="translated_word",
            to_validate="abcde") is None

class TestAnEmptyWordValidatingFieldsShould:
    """Test operations for an empty Word when validating field changes"""
    def test_return_true_for_with_correct_characters_and_groups(self):
        """Return - True if the string only contains alphanumeric characters and '|', ']', '['."""
        result = Word().validate_for_field(
            "etymological_symbology",
            "|b|ac|de|ifo|g|h|j|k|l|m|n|p|q|r|s|sh|tu|th|v|w|x|y|z[]")
        assert result

    def test_return_false_including_invalid_characters_in_valid_groups(self):
        """Return - False if the string contains non-alphanumeric or non delimeters."""
        invalid_characters = '!"£$%^&*()_-+={}~#:;@<,>.?\\/'
        for test_character in invalid_characters:
            assert Word().validate_for_field(
                "etymological_symbology",
                f"|aba|d{test_character}|") is False

    def test_return_false_including_valid_characters_in_invalid_groups(self):
        """Return - False if the string contains invalid group structures"""
        invalid_groups = ['a', 'e', 'i', 'o', 'u', 'aa', 'aab', 'aaba', 'aabaa', 'bc']
        for test_group in invalid_groups:
            assert Word().validate_for_field(
                field_name="etymological_symbology",
                to_validate=f"|{test_group}|") is False


class TestModifyingFieldsShould:
    """Test operations for an empty Word with linked changes when changing field values"""
    def test__setting_a_field_successfully_sets_the_change_flag_to_true(self):
        """Flag value is true and has changed after being successfully set"""
        new_word = Word()
        status_before = new_word.has_unresolved_modification
        new_word.set_field_to(WordField.ETYMOLOGICALSYMBOLOGY, "|abu|da|")
        status_after = new_word.has_unresolved_modification
        assert status_after != status_before
        assert status_after

    def test__setting_a_field_unsuccessfully_does_not_change_the_flag(self):
        """Flag value is true and has changed after being successfully set"""
        new_word = Word()
        status_before = new_word.has_unresolved_modification
        new_word.set_field_to(WordField.ETYMOLOGICALSYMBOLOGY, "|abu!da|")
        status_after = new_word.has_unresolved_modification
        assert status_after == status_before

    def test__setting_a_field_successfully_adds_to_the_version_history(self):
        """Version History is longer after a field is successfully set"""
        new_word = Word()
        history_before = new_word.find_data_on(WordField.VERSIONHISTORY)
        new_word.set_field_to(WordField.ETYMOLOGICALSYMBOLOGY, "|abu|da|")
        history_after = new_word.find_data_on(WordField.VERSIONHISTORY)
        assert len(history_before) < len(history_after)

    def test__setting_a_field_twice_adds_to_the_version_history_each_time(self):
        """Version History is longer after a field is successfully set"""
        new_word = Word()
        original_history = new_word.find_data_on(WordField.VERSIONHISTORY)[:]
        new_word.set_field_to(WordField.ETYMOLOGICALSYMBOLOGY, "|abu|da|")
        history_first = new_word.find_data_on(WordField.VERSIONHISTORY)[:]
        new_word.set_field_to(WordField.ETYMOLOGICALSYMBOLOGY, "|ice|fu|")
        history_second = new_word.find_data_on(WordField.VERSIONHISTORY)[:]
        assert len(original_history) < len(history_first)
        assert len(history_first) < len(history_second)

    def test__setting_a_field_unsuccessfully_does_not_add_to_the_version_history(self):
        """Version History is the same length after a field is unsuccessfully set"""
        new_word = Word()
        history_before = new_word.find_data_on(WordField.VERSIONHISTORY)
        new_word.set_field_to(WordField.ETYMOLOGICALSYMBOLOGY, "|abu!da|")
        history_after = new_word.find_data_on(WordField.VERSIONHISTORY)
        assert history_before == history_after


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

    def test__change_etymological_symbology_with_valid_input(self):
        """An input of valid characters with valid structure will change the value of the field"""
        init_data = {"etymological_symbology": "|aba|et|"}
        word = Word(init_data)
        word.set_field_to(WordField.ETYMOLOGICALSYMBOLOGY, "|ino|mu|")
        assert word.find_data_on(WordField.ETYMOLOGICALSYMBOLOGY) == "|ino|mu|"

    def test__not_change_etymological_symbology_with_invalidly_structured_input(self):
        """An input of valid characters with invalid structure will not change the field value"""
        init_data = {"etymological_symbology": "|aba|et|"}
        word = Word(init_data)
        word.set_field_to(WordField.ETYMOLOGICALSYMBOLOGY, "|inomu|")
        assert word.find_data_on(WordField.ETYMOLOGICALSYMBOLOGY) == "|aba|et|"

    def test__not_change_etymological_symbology_for_input_with_invalid_characters(self):
        """An input of invalid characters with valid structure will not change the field value"""
        init_data = {"etymological_symbology": "|aba|et|"}
        word = Word(init_data)
        word.set_field_to(WordField.ETYMOLOGICALSYMBOLOGY, "|ino!mu|")
        assert word.find_data_on(WordField.ETYMOLOGICALSYMBOLOGY) == "|aba|et|"

    def test__not_change_a_protected_field_directly(self):
        """Protected fields should not respond to calls to set_field_to."""
        word = Word({"has_modified_ancestor": True})
        word.set_field_to(WordField.HASMODIFIEDANCESTOR, False)
        assert word.has_modified_ancestor is True
