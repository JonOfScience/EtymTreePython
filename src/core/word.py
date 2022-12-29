"""Library for Word level functionality."""
from __future__ import annotations
import logging
from typing import Union, Any
import uuid
from core.core import WordField, new_garbage_string
from core.change_history_item import ChangeHistoryItem
from core.change_history import LexiconChangeHistory


class Word:
    """Smallest element of a Lexicon. A single translated word."""
    def __init__(self, merge_data: dict = None) -> None:
        self._unresolved_changes_to_self = []
        self._unresolved_changes_to_ancestor = []

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
            WordField.HASMODIFIEDANCESTOR: "has_modified_ancestor",
            WordField.RESOLVEDHISTORYITEMS: "resolved_history_items",
            WordField.ISRELATEDTO: "is_related_to",
            WordField.UID: "uid"}

        self._protected = [
            WordField.HASBEENMODIFIED,
            WordField.HASMODIFIEDANCESTOR,
            WordField.VERSIONHISTORY,
            WordField.RESOLVEDHISTORYITEMS,
            WordField.UID]

        self._data = {
            "translated_word": new_garbage_string(),
            "translated_word_components": [],
            "in_language_components": "",
            "etymological_symbology": "",
            "compiled_symbology": "",
            "symbol_mapping": "",
            "symbol_selection": "",
            "symbol_pattern_selected": "",
            "rules_applied": "",
            "in_language_word": "",
            "version_history": [],
            "has_been_modified_since_last_resolve": None,  # "Ripple" resolution
            "has_modified_ancestor": "",
            "resolved_history_items": [],
            "is_related_to": "",
            "uid": uuid.uuid4().hex}
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
        return len(self._unresolved_changes_to_self) > 0

    @property
    def has_modified_ancestor(self) -> bool:
        """Boolean - Does this Word have an ancestor that has been modified."""
        return len(self._unresolved_changes_to_ancestor) > 0

    def has_resolved_change_with_id(self, change_id: str) -> bool:
        """Returns true if change_id has been resolved. Otherwise False."""
        resolved_items: list = self.find_data_on(WordField.RESOLVEDHISTORYITEMS)
        if resolved_items.count(change_id) > 0:
            return True
        return False

    def resolve_change_with_id(self, change_id: str) -> None:
        """Logs the change specified by change_id as being resolved"""
        self._data["resolved_history_items"].append(change_id)

    def identify_unresolved_modifications(self, changehistory: LexiconChangeHistory) -> None:
        """Maps internally resolved changes onto all changes to the Lexicon"""
        logger = logging.getLogger('etym_logger')
        self._unresolved_changes_to_self = []
        self._unresolved_changes_to_ancestor = []
        logger.debug("START Determining Changes for : %s", self._data["translated_word"])
        for change_id in self._data["version_history"]:
            if self._data["resolved_history_items"].count(change_id) > 0:
                logger.debug("%s already resolved.", change_id)
            else:
                change_item = changehistory.find_item_with_id(change_id)
                if change_item is None:
                    logger.debug("Change item with id %s is not found.", change_id)
                else:
                    if change_item.originator == self._data["uid"]:
                        self._unresolved_changes_to_self.append(change_id)
                        logger.debug(
                            "Item with id %s is an unresolved changed to %s.",
                            change_id, self._data["translated_word"])
                    else:
                        self._unresolved_changes_to_ancestor.append(change_id)
                        logger.debug(
                            "Item with id %s is an unresolved ancestral change to %s.",
                            change_id, self._data["translated_word"])
        logger.debug("END Determining Changes for : %s", self._data["translated_word"])

    def acknowledge_ancestor_modification_status_of(self, ancestor_status: bool) -> None:
        """Acts on supplied status of ancestor nodes."""
        self._data["has_modified_ancestor"] = ancestor_status

    def acknowledge_ancestor_modification_of(self, ancestor_change_id: str) -> None:
        """Acts on supplied changes of ancestor nodes."""
        self._data["version_history"].append(ancestor_change_id)

    def find_data_on(self, field_name: Union[str, WordField]) -> Union[Any, ValueError]:
        """Returns data for field_name, or ValueError if there is no entry"""
        if isinstance(field_name, WordField):
            field_name = self.fields[field_name]
            if field_name in self._data:
                return self._data[field_name]
        raise ValueError(f"Specified field {field_name} not recognised as a member of Word")

    def set_field_to(self, field_name: WordField, new_value: Any) -> Union[ChangeHistoryItem, None]:
        """Sets data for field_name to new_value"""
        if isinstance(field_name, WordField):
            if field_name in self._protected:
                return None
            field_name = self.fields[field_name]
        else:
            return None
        if self._data[field_name] == new_value:
            return None
        if field_name == "version_history":
            return None
        old_value = self._data[field_name]
        self._data[field_name] = new_value

        new_change_history_item = self._add_version_history_entry(field_name, old_value, new_value)
        return new_change_history_item

    def _add_version_history_entry(
            self,
            field_name: str,
            old_value: Any,
            new_value: Any) -> ChangeHistoryItem:
        if not self._data["version_history"]:
            self._data["version_history"] = []
        word_for_entry = self.find_data_on(WordField.TRANSLATEDWORD)
        log_entry = f"{field_name} ON {word_for_entry} FROM {old_value} TO {new_value}"
        change_history_item = ChangeHistoryItem(log_entry, self._data["uid"])
        self._data["version_history"].append(change_history_item.uid)
        return change_history_item

    def data_for_export(self) -> dict:
        """Surfaces stored data for export"""
        return self._data
