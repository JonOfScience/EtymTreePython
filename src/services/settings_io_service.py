"""Service Layer between Settings and IOService"""
from core.core import DataFormat
from .io_service import IOService


class SettingsIOService:
    """API service layer for IO methods"""
    def __init__(self, io_service: IOService = None, data_format: DataFormat = None) -> None:
        if io_service is not None:
            self._io_service = io_service
        elif data_format is not None:
            self._io_service = IOService(data_format=data_format)
        else:
            raise ValueError("Either IOService or a DataFormat must not be None.")

    def import_config(self, file_id: str):
        """Request and return object deserialised from file storage"""
        return self._io_service.deserialise_stored(file_id)

    def export_config(self, file_id: str, settings_data: dict):
        """Pass Settings data to be serialised and stored"""
        self._io_service.serialise_and_store(settings_data, file_id)
