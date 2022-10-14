"""Tests for low level file i/o operations"""
import sys
import pytest
from lib.core import DataFormat
from src.services.io_service import IOService


def _write_testdata_data_file():
    parts = sys.path[0].split(sep="\\")
    parts.extend(["src", "tests", "data"])
    testdatapath = "/".join(parts)
    with open(f"{testdatapath}/testdata.data", 'w', encoding='UTF-8') as file:
        file.writelines(['{"A": "B", "C": 1}'])
    return testdatapath


class TestGivenANewIOService:
    """Test instantiation operations for an IO Service"""
    def test_ios_ist_00_an_empty_io_service_can_be_constructed(self):
        """IOService can have the data format specified after instantiation"""
        assert IOService()

    def test_ios_ist_01_a_json_io_service_can_be_constructed(self):
        """IOService can have valid data formats specified on instantiation"""
        assert IOService(DataFormat.JSON)


class TestGivenAnIOServiceInAnyFormat:
    """Test format independent operations for any IO Service"""

    def test_ios_rdf_00_data_can_be_read_from_a_correctly_formatted_file(self):
        """IOService will read from a UTF-8 file"""
        testdatapath = _write_testdata_data_file()
        json_io_service = IOService(DataFormat.JSON)
        assert json_io_service.read(f"{testdatapath}/testdata.data") == '{"A": "B", "C": 1}'

    def test_ios_rdf_01_reading_from_a_nonexistant_file_will_throw(self):
        """IOService can't read from a nonexistent file"""
        json_io_service = IOService(DataFormat.JSON)
        with pytest.raises(Exception) as e_info:
            json_io_service.read("NotAFile.NotAFile")
        assert e_info.type == FileNotFoundError


class TestGivenAnIOServiceInJSONFormat:
    """Operations relating to an IOService with a specified JSON format"""
    def test_the_service_data_format_is_accurate(self):
        """The format specified on instantiation is reflected in property values"""
        json_io_service = IOService(DataFormat.JSON)
        assert json_io_service.data_format == DataFormat.JSON

    def test__iso_ots_00__serialises_an_object_to_a_valid_json_string(self):
        """Placeholder: State Test"""
        json_io_service = IOService(DataFormat.JSON)
        testobject = {"A": "B", "C": 1}
        assert json_io_service.serialise_obj_to_string(testobject) == '{"A": "B", "C": 1}'

    def test__iso_ots_01__returns_empty_string_for_an_empty_object(self):
        """Placeholder: State Test"""
        json_io_service = IOService(DataFormat.JSON)
        testobject = {}
        assert json_io_service.serialise_obj_to_string(testobject) == ''

    def test__iso_ots_02__throws_with_none_argument(self):
        """Placeholder: State Test"""
        json_io_service = IOService(DataFormat.JSON)
        with pytest.raises(Exception) as e_info:
            json_io_service.serialise_obj_to_string(None)
        assert e_info.type == ValueError

    def test_iso_sto_00_deserialises_a_valid_json_string(self):
        """State Test"""
        json_io_service = IOService(DataFormat.JSON)
        teststring = '{"A": "B", "C": 1}'
        assert json_io_service.deserialise_string_to_obj(teststring) == {"A": "B", "C": 1}

    def test_iso_sto_01_returns_empty_for_an_empty_string(self):
        """State Test"""
        json_io_service = IOService(DataFormat.JSON)
        teststring = ''
        assert json_io_service.deserialise_string_to_obj(teststring) == {}

    def test_iso_sto_02_throws_with_none_argument(self):
        """State Test"""
        json_io_service = IOService(DataFormat.JSON)
        with pytest.raises(Exception) as e_info:
            json_io_service.deserialise_string_to_obj(None)
        assert e_info.type == TypeError

    def test_ios_dss_00_returns_deserialised_object_from_json_file(self):
        """State Test"""
        testdatapath = _write_testdata_data_file()
        json_io_service = IOService(DataFormat.JSON)
        deserialised_object = json_io_service.deserialise_stored(f"{testdatapath}/testdata")
        assert deserialised_object == {"A": "B", "C": 1}

    def test_the_service_will_write_a_string_to_a_file(self, mocker):
        """Behaviour Test: File write operations are carried out"""
        mock = mocker.patch("builtins.open")
        json_io_service = IOService(DataFormat.JSON)
        testobject = {"A": "B", "C": 1}
        json_io_service.serialise_and_store(testobject, "testobject")
        mock.assert_called_once_with("testobject.data", "w", encoding="UTF-8")

# Serialize object to JSON? XML? YAML?

# Write serialized object to file
