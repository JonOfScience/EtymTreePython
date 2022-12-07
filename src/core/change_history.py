"""Repository for Change History Items"""
from typing import Sequence
from core.change_history_item import ChangeHistoryItem


class LexiconChangeHistory:
    """Repository for ChangeHistoryItems."""
    def __init__(self) -> None:
        self._items: Sequence[ChangeHistoryItem] = []

    def get_all_items(self) -> Sequence[ChangeHistoryItem]:
        """List all ChangeHistoryItems currently registered in the History"""
        return self._items

    def retrieve_export_data_for(self, items: Sequence[ChangeHistoryItem] = None) -> Sequence[dict]:
        """Translate internal data of ChangeHistoryItem instances into serialisable format."""
        if items is not None:
            return [x.data_for_export() for x in items]
        return [x.data_for_export() for x in self.get_all_items()]

    # def store_to(self, filename: str):
    #     """Serialise and store Word entries locally"""
    #     storage_service: LexiconIOService = LexiconIOService(IOService(DataFormat.JSON))
    #     output_dicts = self.retrieve_export_data_for()
    #     storage_service.store_to(filename + ".json", output_dicts)
