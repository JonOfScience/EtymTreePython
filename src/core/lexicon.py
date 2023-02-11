"""Library for Word and Lexicon level functionality."""
from __future__ import annotations
import uuid
import re
from typing import Any, Union
from collections.abc import Sequence
from services.io_service import IOService
from services.lexicon_io_service import LexiconIOService
# from services.io_service_api import IOServiceAPI
from core.core import DataFormat, WordField, split_string_into_groups
from core.word import Word
from core.change_history import LexiconChangeHistory
from core.change_history_item import ChangeHistoryItem
from core.wordflow import Wordflow


class Lexicon:
    """Container to hold Words that comprise a language."""
    @staticmethod
    def _structure_validator_etymological_symbology(to_validate: str):
        string_set = split_string_into_groups(to_validate)
        # Check groups for non-conformity
        for group in [x for x in string_set if x]:
            single_consonants = re.match(
                "^[aeioué]{0,2}[bcdfghjklmnpqrstvwxyz][aeioué]{0,2}$",
                group)
            double_consonants = re.match(
                "(^[aeioué]?(th|sh|ch){1}[aeioué]?$)",
                group)
            if single_consonants is None and double_consonants is None:
                return False
        return True

    _character_validators = {
        WordField.ETYMOLOGICALSYMBOLOGY: 'abcdeéfghijklmnopqrstuvwxyz|[]+ '}
    _structure_validators = {
        WordField.ETYMOLOGICALSYMBOLOGY: _structure_validator_etymological_symbology}

    uuid: str
    title: str
    members: list[Word]

    def __init__(self) -> None:
        self.uuid = uuid.uuid4().hex
        self.title = "BlankProjectLexicon"
        self.members = []
        self.changehistory = LexiconChangeHistory()
        self.index_by_translated_word = {}
        self.index_by_relationship = {}
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
            "Has Modified Ancestor": WordField.HASMODIFIEDANCESTOR,
            "Is Related To": WordField.ISRELATEDTO}

    def _build_indexes(self):
        self.index_by_translated_word.clear()
        self.index_by_relationship = {"ROOT": []}
        for word in self.members:
            translated_word = word.find_data_on(WordField.TRANSLATEDWORD)
            self.index_by_translated_word[translated_word] = word
            self.index_by_relationship[translated_word] = []
        for word in self.members:
            parent_components: list = word.find_data_on(WordField.TRANSLATEDCOMPONENTS)
            if parent_components is None:
                self.index_by_relationship["ROOT"].append(word)
            elif len(parent_components) == 0:
                self.index_by_relationship["ROOT"].append(word)
            else:
                for component in parent_components:
                    if self.index_by_translated_word.get(component) is not None:
                        self.index_by_relationship[component].append(word)

    def get_children_of(self, parent_word: Word) -> Union[list[Word], None]:
        """Gets the immediate child Words of the specified Word, otherwise None"""
        return self.index_by_relationship[parent_word.find_data_on(WordField.TRANSLATEDWORD)]

    def get_descendants_of(
            self,
            parent_word: Word,
            descendants_list: list = None) -> Union[list[Word], None]:
        """Recursively gets all children and further descendents of a parent Word"""
        further_descendants_list = []
        if descendants_list is not None:
            further_descendants_list = descendants_list
        next_children = self.get_children_of(parent_word)
        further_descendants_list.extend(next_children)
        for child_word in next_children:
            further_descendants_list = self.get_descendants_of(child_word, further_descendants_list)
        return further_descendants_list

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

    def create_entry(self) -> Word:
        """Create a Word from the Template and then register it in the Lexicon"""
        new_word = Word()
        self.add_entry(new_word)
        return new_word

    def add_entry(self, entry: Word):
        """Register a given Word in the Lexicon"""
        self.members.append(entry)
        self._build_indexes()

    def get_field_for_word(self, field: str, word: Union[Word, str] = None):
        """Return the data for specified field from a supplied word"""
        if isinstance(word, str):
            word: Word = self.index_by_translated_word[word]
        this_field = self._map_label_to_field(field)
        if this_field is not None:
            return word.find_data_on(this_field)
        raise ValueError(f"Field label {field} is not mapped to a Word field")

    def resolve_modification_flags(self):
        """Identifies unresolved modifications on all entries."""
        for word in self.members:
            word.identify_unresolved_modifications(self.changehistory)

    def _validate_characters_for_field(self, field: WordField, to_validate: str):
        if field not in Lexicon._character_validators:
            return None
        acceptable_chars = set(Lexicon._character_validators[field])
        characters = set(to_validate.lower())
        return characters.issubset(acceptable_chars)

    def _validate_structure_for_field(self, field: WordField, to_validate: str):
        return Lexicon._structure_validators[field](to_validate)

    def validate_for_field(self, field_name: str, to_validate: str):
        """Returns True if characters in to_validate are valid for field_name.
            Otherwise returns False."""
        validation_pipeline = [
            self._validate_characters_for_field,
            self._validate_structure_for_field]
        for validation_stage in validation_pipeline:
            stage_result = validation_stage(
                self._map_label_to_field(field_name),
                to_validate)
            if stage_result is not True:
                return stage_result
        return True

    def validate_for_word_field(self, field_name: str, to_validate: str):
        """Returns True if Word validates to_validate"""
        return self.validate_for_field(
            field_name=field_name,
            to_validate=to_validate)

    def get_word_validitor(self):
        """Returns Wordflow results"""
        return Wordflow()

    def set_field_to_value(self, field: str, word: Union[Word, str], new_value: Any):
        """Set the value of the specified field for a supplied word"""
        if isinstance(word, str):
            word: Word = self.index_by_translated_word[word]

        # if isinstance(new_value, str):
        #     if self.validate_for_field(field_name=field, to_validate=new_value) is False:
        #         raise ValueError("Word: Error - Field cannot be set to invalid value.")

        this_field = self._map_label_to_field(field)
        change_history_item = word.set_field_to(this_field, new_value)

        if change_history_item is not None:
            self._build_indexes()

            self.changehistory.add_item(change_history_item)

            word.identify_unresolved_modifications(self.changehistory)

            all_children = self.get_descendants_of(word)
            for child_word in all_children:
                child_word.acknowledge_ancestor_modification_of(change_history_item.uid)
                child_word.identify_unresolved_modifications(self.changehistory)

    def resolve_change_for(self, change_item: ChangeHistoryItem, changed_word: Word):
        """Logs that change_item has been resolved for changed_word"""
        changed_word.resolve_change_with_id(change_item.uid)
        changed_word.identify_unresolved_modifications(self.changehistory)

    def store_to(self, filename: str):
        """Serialise and store Word entries locally"""
        storage_service: LexiconIOService = LexiconIOService(IOService(DataFormat.JSON))
        output_dicts = self.retrieve_export_data_for()
        storage_service.store_to(filename + ".json", output_dicts)
        # ruleset_io_service: IOServiceAPI = IOServiceAPI("LSR", IOService(DataFormat.JSON))
        # ruleset_io_service.store_to(filename + ".json", self._rulesets)

    def load_from(self, filename: str):
        """Read and deserialise Word entries from local store"""
        storage_service: LexiconIOService = LexiconIOService(IOService(DataFormat.JSON))
        input_data = storage_service.load_from(filename + ".json")
        self.uuid = filename
        for word_data in input_data:
            self.add_entry(Word(word_data))
        # ruleset_io_service: IOServiceAPI = IOServiceAPI("LSR", IOService(DataFormat.JSON))
        # ruleset_data = ruleset_io_service.load_from(filename + ".json")
        # self._rulesets = ruleset_data
