import pytest
from lib.core import DataFormat
from lib.services.io_service import IOService, Serialiser


class Test_GivenANewSerialser:
    def test_WhenNoFormatIsSpecified_AnErrorWillBeThrown(self):
        with pytest.raises(Exception) as e_info:
            Serialiser()
        assert e_info.type == TypeError

    def test_WhenAValidFormatIsSpecified_SerialiserCanBeConstructed(self):
        assert Serialiser(DataFormat.JSON)


class Test_GivenASerialiserInJSONFormat:
    # Call the serialise associated with the right Serialiser class?

    def test_TheSerialiserWillSerialiseAnObjectIntoJSON(self):
        JSON_Serialiser = Serialiser(DataFormat.JSON)
        testobject = {"A": "B", "C": 1}
        serialised_string = JSON_Serialiser.serialise(testobject)
        assert serialised_string == '{"A": "B", "C": 1}'


class Test_GivenANewIOService:
    def test_IOServiceCanBeConstructed(self):
        assert IOService()

    # Set format after creation

    # setting an invalid format throws an error on serialization

    def test_CM_IC_3_TheServiceCallsReadOnDeserialise(self, mocker):
        m = mocker.patch("lib.services.io_service.IOService.read", return_value="")
        _ = mocker.patch(
            "lib.services.io_service.IOService.deserialise_string_to_obj",
            return_value="")
        JSON_IO_service = IOService(DataFormat.JSON)
        _ = JSON_IO_service.deserialise_stored("NotAFileName")
        m.assert_called_once()

    def test_CM_IC_4_TheServiceCallsDeserialiseStringToObjectOnDeserialise(self, mocker):
        _ = mocker.patch("lib.services.io_service.IOService.read", return_value="")
        m = mocker.patch(
            "lib.services.io_service.IOService.deserialise_string_to_obj",
            return_value="")
        JSON_IO_service = IOService(DataFormat.JSON)
        _ = JSON_IO_service.deserialise_stored("NotAFileName")
        m.assert_called_once()


class Test_GivenAnIOServiceInJSONFormat:
    def test_WhenPassedARegisteredFormat_IOServiceCanBeConstructed(self):
        assert IOService(DataFormat.JSON)

    def test_TheServiceHasTheCorrectFormat(self):
        JSON_IO_service = IOService(DataFormat.JSON)
        assert JSON_IO_service.data_format == DataFormat.JSON

    def test_TheServiceWillCallSerializeObject(self, mocker):
        m = mocker.patch("lib.services.io_service.Serialiser.serialise", return_value="")
        JSON_IO_service = IOService(DataFormat.JSON)
        testobject = {"A": "B", "C": 1}
        _ = JSON_IO_service.serialise_obj_to_string(testobject)
        m.assert_called_once()

    def test_CM_IC_5_TheServiceWillCallDeserializeString(self, mocker):
        m = mocker.patch("lib.services.io_service.Deserialiser.deserialise", return_value="")
        JSON_IO_service = IOService(DataFormat.JSON)
        teststring = '{"A": "B", "C": 1}'
        _ = JSON_IO_service.deserialise_string_to_obj(teststring)
        m.assert_called_once()

    def test_TheServiceWillCallStoreForAnObjectInJSON(self, mocker):
        m = mocker.patch("lib.services.io_service.IOService.store")
        JSON_IO_service = IOService(DataFormat.JSON)
        testobject = {"A": "B", "C": 1}
        _ = JSON_IO_service.serialise_and_store(testobject, "testobject")
        m.assert_called_once_with("testobject.data", '{"A": "B", "C": 1}')

    def test_TheServiceWillWriteToAFileForAnObjectInJSON(self, mocker):
        m = mocker.patch("builtins.open")
        JSON_IO_service = IOService(DataFormat.JSON)
        testobject = {"A": "B", "C": 1}
        _ = JSON_IO_service.serialise_and_store(testobject, "testobject")
        m.assert_called_once_with("testobject.data", "w")

    def test_CM_IC_8_TheServiceWillDeserialiseAStoredString(self, mocker):
        _ = mocker.patch(
            "lib.services.io_service.IOService.read",
            return_value='{"A": "B", "C": 1}')
        JSON_IO_service = IOService(DataFormat.JSON)
        deserialised_object = JSON_IO_service.deserialise_stored("NotAFileName")
        assert deserialised_object == {"A": "B", "C": 1}

# Serialize object to JSON? XML? YAML?

# Write serialized object to file
