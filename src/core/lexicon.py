"""Library for Word and Lexicon level functionality."""
from __future__ import annotations
import uuid
import re
from typing import Any, Union
from collections.abc import Sequence
from services.io_service import IOService
from services.lexicon_io_service import LexiconIOService
from core.core import DataFormat, new_garbage_string


class Word:
    """Smallest element of a Lexicon. A single translated word."""
    @staticmethod
    def _split_string_into_groups(to_split: str):
        # Split to_validate into groups
        delimiter_processing_order = ['|', '][', '[', ']']
        string_set = [to_split]
        new_string_set = []
        for delimeter in delimiter_processing_order:
            for element in string_set:
                new_string_set.extend(element.split(sep=delimeter))
            string_set = new_string_set.copy()
            new_string_set.clear()
        return string_set

    @staticmethod
    def _structure_validator_etymological_symbology(to_validate: str):
        string_set = Word._split_string_into_groups(to_validate)
        # Check groups for non-conformity
        for group in [x for x in string_set if x]:
            single_consonants = re.match("^[aeiou]?[bcdfghjklmnpqrstvwxyz]{1}[aeiou]?$", group)
            double_consonants = re.match("(^[aeiou]?(th|sh){1}[aeiou]?$)", group)
            if single_consonants is None and double_consonants is None:
                return False
        return True

    _character_validators = {
        "etymological_symbology": 'abcdefghijklmnopqrstuvwxyz|[]'}
    _structure_validators = {
        "etymological_symbology": _structure_validator_etymological_symbology}
    def __init__(self, merge_data: dict = None) -> None:
        self._data = {
            "translated_word": new_garbage_string(),
            "translated_word_components": None,
            "in_language_components": None,
            "etymological_symbology": None,
            "compiled_symbology": None,
            "symbol_mapping": None,
            "symbol_selection": None,
            "symbol_pattern_selected": None,
            "rules_applied": None,
            "in_language_word": None,
            "version_history": None,
            "has_been_modified_since_last_resolve": None,  # "Ripple" resolution
            "has_modified_ancestor": None}
        if merge_data is not None:
            for (field_name, field_value) in merge_data.items():
                self._data[field_name] = field_value

    def __eq__(self, __o: Word) -> bool:
        if isinstance(__o, Word):
            for (key, value) in self._data.items():
                if value != __o.find_data_on(key):
                    return False
        else:
            return False
        return True

    def find_data_on(self, field_name: str) -> Union[Any, ValueError]:
        """Returns data for field_name, or ValueError if there is no entry"""
        if field_name in self._data:
            return self._data[field_name]
        raise ValueError("Specified field not recognised as a member of Word")

    def set_field_to(self, field_name: str, new_value: Any) -> None:
        """Sets data for field_name to new_value"""
        if isinstance(new_value, str):
            if self.validate_for_field(field_name=field_name, to_validate=new_value) is False:
                print("Word: Error - Field cannot be set to invalid value.")
                return
        self._data[field_name] = new_value

    def _validate_characters_for_field(self, field_name: str, to_validate: str):
        if field_name not in Word._character_validators:
            return None
        acceptable_chars = set(Word._character_validators[field_name])
        characters = set(to_validate.lower())
        return characters.issubset(acceptable_chars)

    def _validate_structure_for_field(self, field_name: str, to_validate: str):
        return Word._structure_validators[field_name](to_validate)
        # return True

    def validate_for_field(self, field_name: str, to_validate: str):
        """Returns True if characters in to_validate are valid for field_name.
            Otherwise returns False."""
        validation_pipeline = [
            self._validate_characters_for_field,
            self._validate_structure_for_field]
        for validation_stage in validation_pipeline:
            stage_result = validation_stage(field_name, to_validate)
            if stage_result is not True:
                return stage_result
        return True

    def data_for_export(self) -> dict:
        """Surfaces stored data for export"""
        return self._data


class Lexicon:
    """Container to hold Words that comprise a language."""
    uuid: str
    title: str
    members: list[Word]

    def __init__(self) -> None:
        self.uuid = uuid.uuid4().hex
        self.title = "BlankProjectLexicon"
        self.members = []
        self.index_by_translated_word = {}

    def _build_indexes(self):
        self.index_by_translated_word.clear()
        for word in self.members:
            self.index_by_translated_word[self.get_field_for_word(
                "translated word",
                word=word)] = word

    def retrieve(self, entry_id: str):
        """Returns a Word with identifier entry_id if it has been registered. Otherwise None."""
        return self.index_by_translated_word.get(entry_id)

    def get_all_words(self) -> Sequence[Word]:
        """List all Words currently registered in the Lexicon"""
        return self.members

    def retrieve_export_data_for(self, words_selected: Sequence[Word] = None) -> Sequence[dict]:
        """Strip the internal data out of Word instances ready for export."""
        if words_selected is not None:
            return [x.data_for_export() for x in words_selected]
        return [x.data_for_export() for x in self.get_all_words()]

    def create_entry(self):
        """Create a Word from the Template and then register it in the Lexicon"""
        new_word = Word()
        self.add_entry(new_word)

    def add_entry(self, entry: Word):
        """Register a given Word in the Lexicon"""
        self.members.append(entry)
        self.index_by_translated_word[self.get_field_for_word(
            "translated word",
            word=entry)] = entry

    def _map_label_to_field(self, field_label) -> str:
        return field_label.lower().replace(" ", "_")

    def get_field_for_word(self, field: str, word: Union[Word, str] = None):
        """Return the data for specified field from a supplied word"""
        if isinstance(word, str):
            word: Word = self.index_by_translated_word[word]
        this_field = self._map_label_to_field(field)
        return word.find_data_on(this_field)

    def validate_for_word_field(self, field_name: str, to_validate: str):
        """Returns True if Word validates to_validate"""
        return Word().validate_for_field(
            field_name=field_name,
            to_validate=to_validate)

    def set_field_to_value(self, field: str, word: Union[Word, str], new_value: Any):
        """Set the value of the specified field for a supplied word"""
        if isinstance(word, str):
            word: Word = self.index_by_translated_word[word]
        this_field = self._map_label_to_field(field)
        word.set_field_to(this_field, new_value)
        self._build_indexes()

    def store_to(self, filename: str):
        """Serialise and store Word entries locally"""
        storage_service: LexiconIOService = LexiconIOService(IOService(DataFormat.JSON))
        output_dicts = self.retrieve_export_data_for()
        storage_service.store_to(filename + ".json", output_dicts)

    def load_from(self, filename: str):
        """Read and deserialise Word entries from local store"""
        storage_service: LexiconIOService = LexiconIOService(IOService(DataFormat.JSON))
        input_data = storage_service.load_from(filename + ".json")
        for word_data in input_data:
            self.add_entry(Word(word_data))
