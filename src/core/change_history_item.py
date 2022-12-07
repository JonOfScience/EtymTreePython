"""Definition of Change History Items and their operations"""
import datetime
import uuid


class ChangeHistoryItem:
    """Item recording a single change made to a single word."""
    def __init__(self, description_of_change: str) -> None:
        self._uid = uuid.uuid4().hex
        self._description_of_change = description_of_change
        self._creation_time = int(datetime.datetime.now().timestamp())

    @property
    def uid(self) -> str:
        """Provides the unique identifier for the ChangeHistoryItem"""
        return self._uid[:]

    @property
    def description(self) -> str:
        """Provides description of the change"""
        return self._description_of_change[:]

    @property
    def created_utc(self) -> int:
        """Provides the naieve UTC timestamp of when the Item was created"""
        return self._creation_time

    def set_description_to(self, new_description: str) -> None:
        """Sets the change item description to the value specified by new_description"""
        self._description_of_change = new_description
