"""Library for Word and Lexicon level functionality."""
from __future__ import annotations
from typing import Any, Union
from collections.abc import Sequence
from services.io_service import IOService
from services.lexicon_io_service import LexiconIOService
from core.core import DataFormat, new_garbage_string


class Word:
    """Smallest element of a Lexicon. A single translated word."""
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
        return True

    def find_data_on(self, field_name: str) -> Union[Any, ValueError]:
        """Returns data for field_name, or ValueError if there is no entry"""
        if field_name in self._data:
            return self._data[field_name]
        raise ValueError("Specified field not recognised as a member of Word")

    def set_field_to(self, field_name: str, new_value: Any) -> None:
        """Sets data for field_name to new_value"""
        self._data[field_name] = new_value

    def data_for_export(self) -> dict:
        """Surfaces stored data for export"""
        return self._data


class Lexicon:
    """Container to hold Words that comprise a language."""
    title: str
    members: list[Word]

    def __init__(self) -> None:
        self.title = "BlankProjectLexicon"
        self.members = []
        self.index_by_translated_word = {}

    def _build_indexes(self):
        self.index_by_translated_word.clear()
        for word in self.members:
            self.index_by_translated_word[self.get_field_for_word(
                "translated word",
                word=word)] = word

    def get_all_words(self) -> Sequence[Word]:
        """List all Words currently registered in the Lexicon"""
        return [x for x in self.members]

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
