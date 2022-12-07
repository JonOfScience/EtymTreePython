"""Repository for Change History Items"""
from typing import Sequence
from core.change_history_item import ChangeHistoryItem


class LexiconChangeHistory:
    """Repository for ChangeHistoryItems."""
    def __init__(self) -> None:
        self._items = Sequence[ChangeHistoryItem]

    # def store_to(self, filename: str):
    #     """Serialise and store Word entries locally"""
    #     storage_service: LexiconIOService = LexiconIOService(IOService(DataFormat.JSON))
    #     output_dicts = self.retrieve_export_data_for()
    #     storage_service.store_to(filename + ".json", output_dicts)
