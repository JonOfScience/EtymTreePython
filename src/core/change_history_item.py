"""Definition of Change History Items and their operations"""
import datetime
import uuid


class ChangeHistoryItem:
    """Item recording a single change made to a single word."""
    def __init__(self, description_of_change: str, originator: str, item_data: dict = None) -> None:
        self._uid = uuid.uuid4().hex
        self._description_of_change = description_of_change
        self._creation_time = int(datetime.datetime.now().timestamp())
        self._originator = originator
        if item_data is not None:
            stored_uid = item_data.get("UId")
            stored_description = item_data.get("DescriptionOfChange")
            stored_creation = item_data.get("CreationTimeUTC")
            stored_originator = item_data.get("Originator")
            if stored_uid is not None:
                self._uid = stored_uid
            if stored_description is not None:
                self._description_of_change = stored_description
            if stored_creation is not None:
                self._creation_time = stored_creation
            if stored_originator is not None:
                self._originator = stored_originator

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

    @property
    def originator(self) -> str:
        """Provides the unique ID for the word entry originating this change"""
        return self._originator

    def set_description_to(self, new_description: str) -> None:
        """Sets the change item description to the value specified by new_description"""
        self._description_of_change = new_description

    def data_for_export(self) -> dict:
        """Provides data object for serialisation and storage"""
        return {
            "UId": self._uid,
            "DescriptionOfChange": self._description_of_change,
            "CreationTimeUTC": self._creation_time,
            "Originator": self.originator}
