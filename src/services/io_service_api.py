"""Standard IO API to use low level IOService"""
from typing import Sequence
from core.core import DataFormat
from .io_service import IOService


class IOServiceAPI:
    """API service layer for low level IO methods"""
    def __init__(
            self,
            prefix: str,
            io_service: IOService = None,
            data_format: DataFormat = None) -> None:
        self._file_prefix = prefix.upper()
        if io_service is not None:
            self._io_service = io_service
        elif data_format is not None:
            self._io_service = IOService(data_format=data_format)
        else:
            raise ValueError("Either IOService or a DataFormat must not be None.")

    def _modify_filename_for_structure_type(self, filename: str):
        return f"data/{self._file_prefix}-" + filename

    def store_to(self, filename: str, item_data: Sequence[dict]):
        """Serialise item_data and pass to I/O service for storage"""
        output_data = []
        for item_dict in item_data:
            output_data.append(self._io_service.serialise_obj_to_string(item_dict) + "\n")
        self._io_service.store(self._modify_filename_for_structure_type(filename), output_data)

    def load_from(self, filename: str):
        """Read data from storage using I/O service and clean"""
        input_data = []
        input_string = self._io_service.read(self._modify_filename_for_structure_type(filename))
        input_strings = input_string.split(sep="\n")
        for serialised_string in input_strings:
            if serialised_string:
                deserialised_data = self._io_service.deserialise_string_to_obj(serialised_string)
                input_data.append(deserialised_data)
        return input_data
