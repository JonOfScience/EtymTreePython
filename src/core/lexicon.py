"""Library for Word and Lexicon level functionality."""
from __future__ import annotations
import uuid
import re
from typing import Any, Union
from collections.abc import Sequence
from services.io_service import IOService
from services.lexicon_io_service import LexiconIOService
from core.core import DataFormat, WordField, new_garbage_string


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

        self.fields = {
            WordField.TRANSLATEDWORD: "translated_word",
            WordField.TRANSLATEDCOMPONENTS: "translated_word_components",
            WordField.INLANGUAGECOMPONENTS: "in_language_components",
            WordField.ETYMOLOGICALSYMBOLOGY: "etymological_symbology",
            WordField.COMPILEDSYMBOLOGY: "compiled_symbology",
            WordField.SYMBOLMAPPING: "symbol_mapping",
            WordField.SYMBOLSELECTION: "symbol_selection",
            WordField.SYMBOLPATTERNSELECTED: "symbol_pattern_selected",
            WordField.RULESAPPLIED: "rules_applied",
            WordField.INLANGUAGEWORD: "in_language_word",
            WordField.VERSIONHISTORY: "version_history",
            WordField.HASBEENMODIFIED: "has_been_modified_since_last_resolve",
            WordField.HASMODIFIEDANCESTOR: "has_modified_ancestor"}

        self._protected = [
            WordField.HASBEENMODIFIED,
            WordField.HASMODIFIEDANCESTOR]

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
            "version_history": [],
            "has_been_modified_since_last_resolve": None,  # "Ripple" resolution
            "has_modified_ancestor": None}
        if merge_data is not None:
            for (field_name, field_value) in merge_data.items():
                self._data[field_name] = field_value

    def __eq__(self, __o: Word) -> bool:
        if isinstance(__o, Word):
            for (key, value) in self._data.items():
                if value != __o._data[key]:
                    return False
        else:
            return False
        return True

    @property
    def has_unresolved_modification(self) -> bool:
        """Boolean - Has this Word been modified without being resolved."""
        return self.find_data_on(WordField.HASBEENMODIFIED)

    @property
    def has_modified_ancestor(self) -> bool:
        """Boolean - Does this Word have an ancestor that has been modified."""
        return self.find_data_on(WordField.HASMODIFIEDANCESTOR)

    def acknowledge_ancestor_modification_status_of(self, ancestor_status: bool) -> None:
        """Acts on supplied status of ancestor nodes."""
        self._data["has_modified_ancestor"] = ancestor_status

    def find_data_on(self, field_name: Union[str, WordField]) -> Union[Any, ValueError]:
        """Returns data for field_name, or ValueError if there is no entry"""
        if isinstance(field_name, WordField):
            field_name = self.fields[field_name]
            if field_name in self._data:
                return self._data[field_name]
        raise ValueError(f"Specified field {field_name} not recognised as a member of Word")

    def set_field_to(self, field_name: WordField, new_value: Any) -> None:
        """Sets data for field_name to new_value"""
        if isinstance(field_name, WordField):
            if field_name in self._protected:
                return
            field_name = self.fields[field_name]
        else:
            return
        if self._data[field_name] == new_value:
            return
        if field_name == "version_history":
            return
        if isinstance(new_value, str):
            if self.validate_for_field(field_name=field_name, to_validate=new_value) is False:
                print("Word: Error - Field cannot be set to invalid value.")
                return
        old_value = self._data[field_name]
        self._data[field_name] = new_value
        # System field changes should NOT trigger a modification flag change
        if field_name not in [
            "has_modified_ancestor",
            "has_been_modified_since_last_resolve",
            "version_history"]:
            self._data["has_been_modified_since_last_resolve"] = True
        self._add_version_history_entry(field_name, old_value, new_value)

    def _add_version_history_entry(self, field_name: str, old_value: Any, new_value: Any):
        if not self._data["version_history"]:
            self._data["version_history"] = []
        log_entry = f"{field_name} FROM {old_value} TO {new_value}"
        self._data["version_history"].append(log_entry)

    def _validate_characters_for_field(self, field_name: str, to_validate: str):
        if field_name not in Word._character_validators:
            return None
        acceptable_chars = set(Word._character_validators[field_name])
        characters = set(to_validate.lower())
        return characters.issubset(acceptable_chars)

    def _validate_structure_for_field(self, field_name: str, to_validate: str):
        return Word._structure_validators[field_name](to_validate)

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
