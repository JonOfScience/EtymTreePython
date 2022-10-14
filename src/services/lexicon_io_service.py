"""Service Layer between Lexicon and IOService"""
from typing import Sequence
from lib.core import DataFormat
from .io_service import IOService


class LexiconIOService:
    """API service layer for IO methods"""
    def __init__(self, io_service: IOService = None, data_format: DataFormat = None) -> None:
        if io_service is not None:
            self._io_service = io_service
        elif data_format is not None:
            self._io_service = IOService(data_format=data_format)
        else:
            raise ValueError("Either IOService or a DataFormat must not be None.")

    def store_to(self, filename: str, word_data: Sequence[dict]):
        """Serialiser Word data and pass to I/O servoce for storage"""
        output_data = []
        for word_dict in word_data:
            output_data.append(self._io_service.serialise_obj_to_string(word_dict) + "\n")
        self._io_service.store(filename, output_data)
