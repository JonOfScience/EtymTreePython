"""Repository for Change History Items"""
from typing import Sequence
from core.core import DataFormat
from core.change_history_item import ChangeHistoryItem
from services.io_service import IOService
from services.change_history_io_service import LexiconChangeHistoryIOService


class LexiconChangeHistory:
    """Repository for ChangeHistoryItems."""
    def __init__(self) -> None:
        self._items: Sequence[ChangeHistoryItem] = []

    def add_item(self, item_to_add: ChangeHistoryItem) -> None:
        """Add a ChangeHistoryItem that has not already been registered."""
        if item_to_add not in self._items:
            self._items.extend([item_to_add])

    def get_all_items(self) -> Sequence[ChangeHistoryItem]:
        """List all ChangeHistoryItems currently registered in the History"""
        return self._items

    def retrieve_export_data_for(self, items: Sequence[ChangeHistoryItem] = None) -> Sequence[dict]:
        """Translate internal data of ChangeHistoryItem instances into serialisable format."""
        if items is not None:
            return [x.data_for_export() for x in items]
        return [x.data_for_export() for x in self.get_all_items()]

    def store_to(self, filename: str):
        """Serialise and store ChangeHistoryItem entries locally"""
        storage_service: LexiconChangeHistoryIOService = LexiconChangeHistoryIOService(
            IOService(DataFormat.JSON))
        output_dicts = self.retrieve_export_data_for()
        storage_service.store_to(filename + ".json", output_dicts)

    def load_from(self, filename: str):
        """Read and deserialise LexiconChangeHistory entries from local store"""
        storage_service: LexiconChangeHistoryIOService = LexiconChangeHistoryIOService(
            IOService(DataFormat.JSON))
        input_data = storage_service.load_from(filename + ".json")
        for item_data in input_data:
            self.add_item(ChangeHistoryItem(item_data))
