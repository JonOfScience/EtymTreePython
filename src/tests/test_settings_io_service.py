"""Tests for service layer between configuration settings and IO operations"""
from lib.core import DataFormat
from services.settings_io_service import SettingsIOService
from services.io_service import IOService


class TestGivenANewSettingsIOService:
    """For a newly created/empty service object with a valid data format."""
    def test_cm_ic_2_calls_io_level_operation_on_import_call(self, mocker):
        """Accurately translates import calls to lower level services."""
        mock = mocker.patch("services.io_service.IOService.deserialise_stored", return_value="")
        new_config_service = SettingsIOService(IOService(DataFormat.JSON))
        _ = new_config_service.import_config("TestConfig")
        mock.assert_called_once()

    def test_cm_ic_9_returns_object_in_expected_format_for_settings(self, mocker):
        """Returns deserialised objects in expected format"""
        _ = mocker.patch(
            "services.io_service.IOService.deserialise_stored",
            return_value={"A": "B", "C": 1})
        new_config_service = SettingsIOService(IOService(DataFormat.JSON))
        config_object = new_config_service.import_config("TestConfig")
        assert config_object == {"A": "B", "C": 1}
