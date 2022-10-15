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
        """Serialise Word data and pass to I/O service for storage"""
        output_data = []
        for word_dict in word_data:
            output_data.append(self._io_service.serialise_obj_to_string(word_dict) + "\n")
        self._io_service.store(filename, output_data)

    def load_from(self, filename: str):
        """Read data from storage using I/O service and clean"""
        input_data = []
        input_string = self._io_service.read(filename)
        input_strings = input_string.split(sep="\n")
        for serialised_string in input_strings:
            if serialised_string:
                deserialised_data = self._io_service.deserialise_string_to_obj(serialised_string)
                input_data.append(deserialised_data)
        return input_data
