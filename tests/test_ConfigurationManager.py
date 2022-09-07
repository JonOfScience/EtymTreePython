"""Tests for the Configuration Manager class."""
from lib.managers.configurationmanager import ConfigurationManager


class TestGivenANewConfigManager:
    """Test cases for when the Configuration Manager is empty (new)."""
    def test_when_an_invalid_config_id_is_specified_then_get_config_from_id_returns_none(self):
        new_manager = ConfigurationManager()
        assert new_manager.getconfigfromid("ABCDE") is None

    def test_cm_ic_1_the_manager_calls_import_config_on_the_service(self, mocker):
        mock_service = mocker.patch(
            "lib.services.configurationservice.ConfigurationService.import_config",
            return_value={"ABCDE": "Updated", "FGHIJ": "Added"})
        new_manager = ConfigurationManager()
        new_manager.import_config("testconfig")
        mock_service.assert_called_once()

    # def test_CM_IC_10_ImportConfigReturnsAConfigDictionary(self, mocker):
    #     _ = mocker.patch(
    #         "lib.services.configurationservice.ConfigurationService.import_config",
    #         return_value={"ABCDE": "Updated", "FGHIJ": "Added" })
    #     new_manager = ConfigurationManager()
    #     result = new_manager.import_config("testconfig")
    #     assert isinstance(result, dict)

    def test_cm_ic_11_the_manager_calls_integrate_config(self, mocker):
        _ = mocker.patch(
            "lib.services.configurationservice.ConfigurationService.import_config",
            return_value={"ABCDE": "Updated", "FGHIJ": "Added"})
        mock_service = mocker.patch(
            "lib.managers.configurationmanager.ConfigurationManager.integrate_config",
            return_value=True)
        new_manager = ConfigurationManager()
        new_manager.import_config("testconfig")
        mock_service.assert_called_once()


class TestGivenAManagerWithBaseConfig:
    """Tests for a Configuration Manager that is instantiated with values."""
    def test_when_a_valid_config_id_is_specified_then_get_config_from_id_returns_a_value(self):
        new_manager = ConfigurationManager({"ABCDE": "Pass"})
        assert new_manager.getconfigfromid("ABCDE") == "Pass"

    # def test_WhenLoadingAUserConfigFromAFile_ThenTheConfigServiceIsAccessed(self, mocker):

    def test_cm_ic_12_when_loading_a_user_config_from_a_file_then_base_options_are_overwritten(self, mocker):
        # NEED TO MOCK THE INTERNAL CALL HERE
        _ = mocker.patch(
            "lib.services.configurationservice.ConfigurationService.import_config",
            return_value={"ABCDE": "Updated", "FGHIJ": "Added"})
        new_manager = ConfigurationManager({"ABCDE": "Pass"})
        new_manager.import_config("testconfig")
        assert new_manager.getconfigfromid("FGHIJ") == "Added"
        assert new_manager.getconfigfromid("ABCDE") == "Updated"
