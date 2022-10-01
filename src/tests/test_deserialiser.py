"""Tests for deserialisers for converting strings to various formats."""
from enum import Enum
import pytest
from lib.core import DataFormat
from src.services.io_service import Deserialiser


class TestGivenADeserialiserWithInvalidSettings:
    """Test operations for a deserialiser initialised with invalid format"""
    def test_des_ist_01_empty_instantiation_will_throw(self):
        """Instantiation requires a format to be specified """
        with pytest.raises(Exception) as e_info:
            Deserialiser()  # pylint: disable=no-value-for-parameter
        assert e_info.type == TypeError

    def test_des_des_00_deserialiser_will_throw_on_deserialise(self):
        """Deserialiser will throw as it cannot find the format for the specified string"""
        class _NotAFormat(Enum):
            NOTAFORMAT = "NotAFormat"
        with pytest.raises(Exception) as e_info:
            Deserialiser(_NotAFormat.NOTAFORMAT).deserialise('{"Any": "String}')
        assert e_info.type == KeyError


class TestGivenAValidDeserialiserFormat:
    """Instantiation for correctly defined deserialisers"""
    def test_des_ist_00_a_deserialiser_in_json_format_can_be_constructed(self):
        """JSON is a recognised format"""
        assert Deserialiser(DataFormat.JSON)


class TestGivenADeserialiserInJSONFormat:
    """Operations for a deserialiser in JSON format"""
    def test_des_des_01_a_valid_string_will_deserialise(self):
        """State test
        Integration Test: Deserialiser <- to/from -> JSON_Deserialiser"""
        teststring = '{"A": "B", "C": 1}'
        deserialised_object = Deserialiser(DataFormat.JSON).deserialise(teststring)
        assert deserialised_object == {"A": "B", "C": 1}

    def test_des_des_02_an_empty_input_returns_an_empty_dict(self):
        """State test
        Integration Test: Deserialiser <- to/from -> JSON_Deserialiser"""
        assert Deserialiser(DataFormat.JSON).deserialise('') == {}

    def test_des_des_03_an_input_of_none_throws(self):
        """State test
        Integration Test: Deserialiser <- to/from -> JSON_Deserialiser"""
        with pytest.raises(Exception) as e_info:
            Deserialiser(DataFormat.JSON).deserialise(None)
        assert e_info.type == TypeError
