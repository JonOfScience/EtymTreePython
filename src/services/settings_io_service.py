"""Service Layer between Settings and IOService"""
from lib.core import DataFormat
from .io_service import IOService


class SettingsIOService:
    """API service layer for IO methods"""
    def __init__(self, io_service: IOService = None, data_format: DataFormat = None) -> None:
        if io_service is not None:
            self._io_service = io_service
        else:
            self._io_service = IOService(data_format=data_format)

    def import_config(self, file_id):
        """Request and return object deserialised from file storage"""
        return self._io_service.deserialise_stored(file_id)
