"""Library for Word and Lexicon level functionality."""
from __future__ import annotations
import uuid
from typing import Any, Union
from collections.abc import Sequence
from services.io_service import IOService
from services.lexicon_io_service import LexiconIOService
from core.core import DataFormat, WordField
from core.word import Word


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
        self.label_to_wordfield_mapping = {
            "Translated Word": WordField.TRANSLATEDWORD,
            "Translated Word Components": WordField.TRANSLATEDCOMPONENTS,
            "In Language Components": WordField.INLANGUAGECOMPONENTS,
            "Etymological Symbology": WordField.ETYMOLOGICALSYMBOLOGY,
            "Compiled Symbology": WordField.COMPILEDSYMBOLOGY,
            "Symbol Mapping": WordField.SYMBOLMAPPING,
            "Symbol Selection": WordField.SYMBOLSELECTION,
            "Symbol Pattern Selected": WordField.SYMBOLPATTERNSELECTED,
            "Rules Applied": WordField.RULESAPPLIED,
            "In Language Word": WordField.INLANGUAGEWORD,
            "Version History": WordField.VERSIONHISTORY,
            "Has Been Modified Since Last Resolve": WordField.HASBEENMODIFIED,
            "Has Modified Ancestor": WordField.HASMODIFIEDANCESTOR}

    def _build_indexes(self):
        self.index_by_translated_word.clear()
        for word in self.members:
            self.index_by_translated_word[word.find_data_on(WordField.TRANSLATEDWORD)] = word

    def _map_label_to_field(self, field_label) -> WordField:
        return self.label_to_wordfield_mapping.get(field_label)

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
        self.index_by_translated_word[entry.find_data_on(WordField.TRANSLATEDWORD)] = entry

    def get_field_for_word(self, field: str, word: Union[Word, str] = None):
        """Return the data for specified field from a supplied word"""
        if isinstance(word, str):
            word: Word = self.index_by_translated_word[word]
        this_field = self._map_label_to_field(field)
        if this_field is not None:
            return word.find_data_on(this_field)
        raise ValueError(f"Field label {field} is not mapped to a Word field")

    def get_parents_of(self, word: Word) -> Sequence[Word]:
        """Return the Word objects for any extant Translated Word Components"""
        parent_items = word.find_data_on(WordField.TRANSLATEDCOMPONENTS)
        if parent_items is None:
            return []
        return [self.index_by_translated_word.get(x)
                for x
                in parent_items
                if self.index_by_translated_word.get(x) is not None]

    def determine_ancestor_modification_for(self, word: Word) -> bool:
        """Return True if a parent has been modified or has a modified ancestor, else false"""
        word_parents = self.get_parents_of(word)
        if not word_parents:
            return False
        for parent_word in word_parents:
            if (parent_word.has_unresolved_modification
                or parent_word.has_modified_ancestor):
                return True
        return False

    def resolve_modification_flags_pass(self) -> int:
        """Loops through all entries checking for status flag changes.
        Returns number of changes made."""
        flags_flipped = 0
        word: Word
        for word in self.members:
            old_value = word.has_modified_ancestor
            new_value = self.determine_ancestor_modification_for(word)
            word.acknowledge_ancestor_modification_status_of(new_value)
            if old_value != word.has_modified_ancestor:
                flags_flipped += 1
        return flags_flipped

    def resolve_modification_flags(self) -> bool:
        """Calls multiple resolving passes.
        Continues until no changes are made in consecutive passes.
        Returns - Positive pass count on successful resolution or 0 if resolution fails"""
        resolve_pass_max = 10
        flags_flipped = 1
        passes_since_last_flip = 0
        while passes_since_last_flip < resolve_pass_max and flags_flipped > 0:
            flags_flipped = self.resolve_modification_flags_pass()
            if flags_flipped:
                passes_since_last_flip += 1
        if flags_flipped == 0:
            return True
        return False

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
        change_history_item = word.set_field_to(this_field, new_value)
        self._build_indexes()
        return change_history_item

    def store_to(self, filename: str):
        """Serialise and store Word entries locally"""
        storage_service: LexiconIOService = LexiconIOService(IOService(DataFormat.JSON))
        output_dicts = self.retrieve_export_data_for()
        storage_service.store_to(filename + ".json", output_dicts)

    def load_from(self, filename: str):
        """Read and deserialise Word entries from local store"""
        storage_service: LexiconIOService = LexiconIOService(IOService(DataFormat.JSON))
        input_data = storage_service.load_from(filename + ".json")
        self.uuid = filename
        for word_data in input_data:
            self.add_entry(Word(word_data))
