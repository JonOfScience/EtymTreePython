"""Repository for Change History Items"""
from typing import Sequence
from core.change_history_item import ChangeHistoryItem


class LexiconChangeHistory:
    """Repository for ChangeHistoryItems."""
    def __init__(self) -> None:
        self._items = Sequence[ChangeHistoryItem]
