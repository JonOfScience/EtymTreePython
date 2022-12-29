"""Tests for a single Word."""
from core.lexicon import Word, WordField
from core.change_history_item import ChangeHistoryItem


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


class TestModifyingFieldsShould:
    """Test operations for an empty Word with linked changes when changing field values"""
    def test__setting_a_field_successfully_produces_a_change_history_item(self):
        """Items are then stored for cross-referencing and recall."""
        new_word = Word()
        change_item = new_word.set_field_to(WordField.ETYMOLOGICALSYMBOLOGY, "|abu|da|")
        assert change_item is not None
        assert isinstance(change_item, ChangeHistoryItem)

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

    def test__not_change_a_protected_field_directly(self):
        """Protected fields should not respond to calls to set_field_to."""
        word = Word({"resolved_history_items": ["OLDITEM"]})
        word.set_field_to(WordField.RESOLVEDHISTORYITEMS, ["NEWITEM"])
        assert word.find_data_on(WordField.RESOLVEDHISTORYITEMS) == ["OLDITEM"]
