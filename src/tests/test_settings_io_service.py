"""Tests for service layer between configuration settings and IO operations"""
import sys
import pytest
from lib.core import DataFormat
from src.services.settings_io_service import SettingsIOService
from src.services.io_service import IOService


def _write_testdata_data_file():
    parts = sys.path[0].split(sep="\\")
    parts.extend(["src", "tests", "data"])
    testdatapath = "/".join(parts)
    with open(f"{testdatapath}/testdata.data", 'w', encoding='UTF-8') as file:
        file.writelines(['{"A": "B", "C": 1}'])
    return testdatapath


class TestGivenANewSettingsIOService:
    """For a newly created/empty service object with a valid data format."""

    def test_sio_ist_00_instantiates_when_ioservice_is_provided(self):
        """Returns deserialised objects in expected format"""
        new_config_service = SettingsIOService(io_service=IOService(DataFormat.JSON))
        assert new_config_service

    def test_sio_ist_01_instantiates_when_dataformat_is_provided(self):
        """Returns deserialised objects in expected format"""
        new_config_service = SettingsIOService(data_format=DataFormat.JSON)
        assert new_config_service

    def test_sio_ist_02_instantiation_throws_without_ioservice_or_dataformat(self):
        """Returns deserialised objects in expected format"""
        with pytest.raises(Exception) as e_info:
            SettingsIOService()
        assert e_info.type == ValueError

    def test_sio_imc_00_returns_deserialised_object_in_expected_format_for_valid_filename(self):
        """Import from stored source"""
        new_config_service = SettingsIOService(IOService(DataFormat.JSON))
        testdatapath = _write_testdata_data_file()
        config_object = new_config_service.import_config(f"{testdatapath}/testdata")
        assert config_object == {"A": "B", "C": 1}
