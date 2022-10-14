"""Tests for serialisers for objects to strings in various formats."""
from enum import Enum
import pytest
from lib.core import DataFormat
from src.services.io_service import Serialiser


class TestGivenASerialiserWithInvalidSettings:
    """Test operations for a serialiser initialised with invalid format"""
    def test__ser_ist_01__empty_instantiation_will_throw(self):
        """A serialiser cannot exist without a specified format"""
        with pytest.raises(Exception) as e_info:
            Serialiser()  # pylint: disable=no-value-for-parameter
        assert e_info.type == TypeError

    def test__ser_ser_00__serialiser_will_throw_on_serialise(self):
        """Serialiser will throw as it cannot find the format for the specified string"""
        class _NotAFormat(Enum):
            NOTAFORMAT = "NotAFormat"
        with pytest.raises(Exception) as e_info:
            Serialiser(_NotAFormat.NOTAFORMAT).serialise('{"Any": "String}')
        assert e_info.type == KeyError


class TestGivenAValidSerialiserFormat:
    """Instantiation for correctly defined serialisers"""
    def test__ser_ist_00__a_serialiser_in_json_format_can_be_constructed(self):
        """JSON is a recognised format"""
        assert Serialiser(DataFormat.JSON)


class TestGivenASerialiserInJSONFormat:
    """Operations for a serialiser in JSON format"""
    def test__ser_ser_01__serialise_produces_a_json_string(self):
        """Input dictionary object serialises to a JSON string"""
        json_serialiser = Serialiser(DataFormat.JSON)
        testobject = {"A": "B", "C": 1}
        serialised_string = json_serialiser.serialise(testobject)
        assert serialised_string == '{"A": "B", "C": 1}'

    def test__ser_ser_02__an_empty_object_serialises_to_an_empty_string(self):
        """Returns empty string for empty object"""
        json_serialiser = Serialiser(DataFormat.JSON)
        testobject = {}
        assert json_serialiser.serialise(testobject) == ''

    def test__ser_ser_03__will_throw_with_input_of_none(self):
        """Throws with None input"""
        json_serialiser = Serialiser(DataFormat.JSON)
        testobject = None
        with pytest.raises(Exception) as e_info:
            json_serialiser.serialise(testobject)
        assert e_info.type == ValueError
