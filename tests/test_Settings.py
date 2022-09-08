"""Tests for configuration Settings."""
from lib.configuration.settings import Settings


class TestGivenEmptySettings:
    """Test operations on an empty settings store"""
    def test_when_any_setting_is_requested_then_none_is_returned(self):
        empty_settings = Settings()
        assert empty_settings.find_by_id("ABCDE") is None

    def test_cm_ic_1_a_request_to_import_configuration_options_is_passed_on(self, mocker):
        mock_service = mocker.patch(
            "lib.services.configurationservice.ConfigurationService.import_config",
            return_value={"ABCDE": "Updated", "FGHIJ": "Added"})
        empty_settings = Settings()
        empty_settings.import_config("testconfig")
        mock_service.assert_called_once()

    # def test_CM_IC_10_ImportConfigReturnsAConfigDictionary(self, mocker):
    #     _ = mocker.patch(
    #         "lib.services.configurationservice.ConfigurationService.import_config",
    #         return_value={"ABCDE": "Updated", "FGHIJ": "Added" })
    #     new_manager = Settings()
    #     result = new_manager.import_config("testconfig")
    #     assert isinstance(result, dict)

    def test_cm_ic_11_the_manager_calls_integrate_config(self, mocker):
        _ = mocker.patch(
            "lib.services.configurationservice.ConfigurationService.import_config",
            return_value={"ABCDE": "Updated", "FGHIJ": "Added"})
        mock_service = mocker.patch(
            "lib.configuration.settings.Settings.integrate_config",
            return_value=True)
        empty_settings = Settings()
        empty_settings.import_config("testconfig")
        mock_service.assert_called_once()


class TestGivenAnExistingConfiguration:
    """Test if configuration options can be read and (over)written."""
    def test_when_a_valid_id_is_specified_then_the_setting_value_is_returned(self):
        config = Settings({"ABCDE": "Pass"})
        assert config.find_by_id("ABCDE") == "Pass"

    def test_cm_ic_12_base_entries_are_overwritten_when_importing_config(self, mocker):
        _ = mocker.patch(
            "lib.services.configurationservice.ConfigurationService.import_config",
            return_value={"ABCDE": "Updated", "FGHIJ": "Added"})
        config = Settings({"ABCDE": "Pass"})
        config.import_config("testconfig")
        assert config.find_by_id("FGHIJ") == "Added"
        assert config.find_by_id("ABCDE") == "Updated"
