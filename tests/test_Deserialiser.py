import pytest
from lib.core import DataFormat
from lib.services.io_service import Deserialiser, JSONDeserialiser

class Test_GivenANewDeserialiser:
    def test_WhenNoFormatIsSpecified_AnErrorWillBeThrown(self):
        with pytest.raises(Exception) as e_info:
            Deserialiser()
        assert e_info.type == TypeError

    def test_WhenAValidFormatIsSpecified_DeserialiserCanBeConstructed(self):
        assert Deserialiser(DataFormat.JSON)

class Test_GivenADeserialiserWithUnrecognisefFormat:
    def test_WhenDeserialiseIsCalled_AnErrorWillBeThrown(self):
        with pytest.raises(Exception) as e_info:
            Deserialiser("ThisIsNotAFormat").deserialise('{"Any": "String}')
        assert e_info.type == KeyError

class Test_GivenADeserialiserInJSONFormat:
    def test_CM_IC_6_AJSONDeserialiserIsCalled(self, mocker):
        # Behavioural test
        m = mocker.patch("lib.services.io_service.JSONDeserialiser.deserialise", return_data={"A": "B", "C": 1 })
        deserialiser = Deserialiser(DataFormat.JSON)
        teststring = '{"A": "B", "C": 1}'
        _ = deserialiser.deserialise(teststring)
        m.assert_called_once()

    def test_CM_IC_7_AJSONStringCanBeDeserialised(self):
        # State test
        # Integration Test: Deserialiser <- to/from -> JSON_Deserialiser
        JSON_Deserialiser = Deserialiser(DataFormat.JSON)
        teststring = '{"A": "B", "C": 1}'
        deserialised_object = JSON_Deserialiser.deserialise(teststring)
        assert deserialised_object == {"A": "B", "C": 1 }