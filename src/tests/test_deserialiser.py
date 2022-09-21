"""Tests for deserialisers for converting strings to various formats."""
from enum import Enum
import pytest
from src.lib.core import DataFormat
from src.services.io_service import Deserialiser


class TestGivenADeserialiserWithInvalidSettings:
    """Test operations for a deserialiser initialised with invalid format"""
    def test_empty_instantiation_will_throw(self):
        """Instantiation requires a format to be specified """
        with pytest.raises(Exception) as e_info:
            Deserialiser()  # pylint: disable=no-value-for-parameter
        assert e_info.type == TypeError

    def test_deserialiser_will_throw_on_deserialise(self):
        """Deserialiser will throw as it cannot find the format for the specified string"""
        class NotAFormat(Enum):
            NOTAFORMAT = "NotAFormat"
        with pytest.raises(Exception) as e_info:
            Deserialiser(NotAFormat.NOTAFORMAT).deserialise('{"Any": "String}')
        assert e_info.type == KeyError


class TestGivenAValidDeserialiserFormat:
    """Instantiation for correctly defined deserialisers"""
    def test_a_deserialiser_in_json_format_can_be_constructed(self):
        """JSON is a recognised format"""
        assert Deserialiser(DataFormat.JSON)


class TestGivenADeserialiserInJSONFormat:
    """Operations for a deserialiser in JSON format"""
    # Behavioural test - Brittle - What if we change the name of "deserialise?"
    def test_cm_ic_6_a_json_deserialise_method_is_called(self, mocker):
        """Calls to deserialise will call the JSON method"""
        mock_deserialise = mocker.patch(
            "src.services.io_service.JSONDeserialiser.deserialise",
            return_data={"A": "B", "C": 1})
        deserialiser = Deserialiser(DataFormat.JSON)
        teststring = '{"A": "B", "C": 1}'
        _ = deserialiser.deserialise(teststring)
        mock_deserialise.assert_called_once()

    def test_cm_ic_7_a_valid_string_will_deserialise(self):
        """State test
        Integration Test: Deserialiser <- to/from -> JSON_Deserialiser"""
        json_deserialiser = Deserialiser(DataFormat.JSON)
        teststring = '{"A": "B", "C": 1}'
        deserialised_object = json_deserialiser.deserialise(teststring)
        assert deserialised_object == {"A": "B", "C": 1}

    def test_a_none_input_returns_an_empty_dict(self):
        """State test
        Integration Test: Deserialiser <- to/from -> JSON_Deserialiser"""
        json_deserialiser = Deserialiser(DataFormat.JSON)
        teststring = None
        deserialised_object = json_deserialiser.deserialise(teststring)
        assert deserialised_object == {}
