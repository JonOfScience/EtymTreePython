"""Repository for Change History Items"""
from typing import Sequence, List
from core.core import DataFormat
from core.change_history_item import ChangeHistoryItem
from services.io_service import IOService
from services.change_history_io_service import LexiconChangeHistoryIOService


class LexiconChangeHistory:
    """Repository for ChangeHistoryItems."""
    def __init__(self) -> None:
        self._id_index = {}
        self._originator_index = {}
        self._items: Sequence[ChangeHistoryItem] = []

    def _build_indexes(self) -> None:
        self._originator_index = {}
        for item in self._items:
            self._id_index[item.uid] = item
            if item.originator in self._originator_index:
                self._originator_index[item.originator].append(item.uid)
            else:
                self._originator_index[item.originator] = [item.uid]


    def add_item(self, item_to_add: ChangeHistoryItem) -> None:
        """Add a ChangeHistoryItem that has not already been registered."""
        if item_to_add not in self._items and item_to_add is not None:
            self._items.extend([item_to_add])
        self._build_indexes()

    def get_all_items(self) -> Sequence[ChangeHistoryItem]:
        """List all ChangeHistoryItems currently registered in the History"""
        return self._items

    def find_item_with_id(self, item_id: str) -> ChangeHistoryItem:
        """Return a ChangeHistoryItem if the id exists, otherwise None."""
        return self._id_index.get(item_id)

    def find_items_with_originator(self, originator_id: str) -> List[str]:
        """Return a sequence of ChangeHistoryItem ids with the given originator, otherwise None."""
        return self._originator_index.get(originator_id)

    def retrieve_export_data_for(self, items: Sequence[ChangeHistoryItem] = None) -> Sequence[dict]:
        """Translate internal data of ChangeHistoryItem instances into serialisable format."""
        if items is not None:
            return [x.data_for_export() for x in items]
        if len(self._items) == 0:
            return []
        return [x.data_for_export() for x in self._items]

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
            self.add_item(ChangeHistoryItem("", "", item_data = item_data))
        self._build_indexes()
