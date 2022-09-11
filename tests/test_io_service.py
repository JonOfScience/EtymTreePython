"""Tests for low level file i/o operations"""
from lib.core import DataFormat
from lib.services.io_service import IOService


class TestGivenANewIOService:
    """Test instantiation operations for an IO Service"""
    def test_an_empty_io_service_can_be_constructed(self):
        """IOService can have the data format specified after instantiation"""
        assert IOService()

    def test_a_json_io_service_can_be_constructed(self):
        """IOService can have valid data formats specified on instantiation"""
        assert IOService(DataFormat.JSON)


class TestGivenAnIOServiceInAnyFormat:
    """Test format independent operations for any IO Service"""
    def test_cm_ic_3_will_call_read_on_deserialise_stored(self, mocker):
        """IOService will read from a file"""
        mock = mocker.patch("lib.services.io_service.IOService.read", return_value="")
        _ = mocker.patch(
            "lib.services.io_service.IOService.deserialise_string_to_obj",
            return_value="")
        json_io_service = IOService(DataFormat.JSON)
        _ = json_io_service.deserialise_stored("NotAFileName")
        mock.assert_called_once()

    def test_cm_ic_4_will_call_deserialise_string_to_object_on_deserialise(self, mocker):
        """IOService will attempt to deserialise a read string"""
        _ = mocker.patch("lib.services.io_service.IOService.read", return_value="")
        mock = mocker.patch(
            "lib.services.io_service.IOService.deserialise_string_to_obj",
            return_value="")
        json_io_service = IOService(DataFormat.JSON)
        _ = json_io_service.deserialise_stored("NotAFileName")
        mock.assert_called_once()


class TestGivenAnIOServiceInJSONFormat:
    """Operations relating to an IOService with a specified JSON format"""
    def test_the_service_data_format_is_accurate(self):
        """The format specified on instantiation is reflected in property values"""
        json_io_service = IOService(DataFormat.JSON)
        assert json_io_service.data_format == DataFormat.JSON

    def test_the_serialise_method_on_the_serialiser_is_called(self, mocker):
        """The calls are passed through to subordinate serialiser objects correctly"""
        mock = mocker.patch("lib.services.io_service.Serialiser.serialise", return_value="")
        json_io_service = IOService(DataFormat.JSON)
        testobject = {"A": "B", "C": 1}
        _ = json_io_service.serialise_obj_to_string(testobject)
        mock.assert_called_once()

    def test_cm_ic_5_the_deserialise_method_on_the_deserialiser_is_called(self, mocker):
        """Behaviour Test: Calls are passed to subordinate deserialiser objects correctly"""
        mock = mocker.patch("lib.services.io_service.Deserialiser.deserialise", return_value="")
        json_io_service = IOService(DataFormat.JSON)
        teststring = '{"A": "B", "C": 1}'
        _ = json_io_service.deserialise_string_to_obj(teststring)
        mock.assert_called_once()

    def test_serialise_and_store_will_call_store_on_the_service(self, mocker):
        """Behaviour Test: Subordinate methods are called"""
        mock = mocker.patch("lib.services.io_service.IOService.store")
        json_io_service = IOService(DataFormat.JSON)
        testobject = {"A": "B", "C": 1}
        _ = json_io_service.serialise_and_store(testobject, "testobject")
        mock.assert_called_once_with("testobject.data", '{"A": "B", "C": 1}')

    def test_the_service_will_write_a_string_to_a_file(self, mocker):
        """Behaviour Test: File write operations are carried out"""
        mock = mocker.patch("builtins.open")
        json_io_service = IOService(DataFormat.JSON)
        testobject = {"A": "B", "C": 1}
        _ = json_io_service.serialise_and_store(testobject, "testobject")
        mock.assert_called_once_with("testobject.data", "w", encoding="UTF-8")

    def test_cm_ic_8_a_stored_string_can_be_deserialised(self, mocker):
        """Behaviour: Test: File read operations are carried out"""
        _ = mocker.patch(
            "lib.services.io_service.IOService.read",
            return_value='{"A": "B", "C": 1}')
        json_io_service = IOService(DataFormat.JSON)
        deserialised_object = json_io_service.deserialise_stored("NotAFileName")
        assert deserialised_object == {"A": "B", "C": 1}

# Serialize object to JSON? XML? YAML?

# Write serialized object to file
