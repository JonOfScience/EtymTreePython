from lib.managers.configurationmanager import ConfigurationManager


class Test_GivenANewConfigManager:
    def test_WhenAnInvalidConfigIdIsSpecified_ThenGetConfigFromIdReturnsNone(self):
        new_manager = ConfigurationManager()
        assert new_manager.getconfigfromid("ABCDE") is None

    def test_CM_IC_1_TheManagerCallsImportConfigOnTheService(self, mocker):
        m = mocker.patch(
            "lib.services.configurationservice.ConfigurationService.import_config",
            return_value={"ABCDE": "Updated", "FGHIJ": "Added"})
        new_manager = ConfigurationManager()
        new_manager.import_config("testconfig")
        m.assert_called_once()

    # def test_CM_IC_10_ImportConfigReturnsAConfigDictionary(self, mocker):
    #     _ = mocker.patch(
    #         "lib.services.configurationservice.ConfigurationService.import_config",
    #         return_value={"ABCDE": "Updated", "FGHIJ": "Added" })
    #     new_manager = ConfigurationManager()
    #     result = new_manager.import_config("testconfig")
    #     assert isinstance(result, dict)

    def test_CM_IC_11_TheManagerCallsIntegrateConfig(self, mocker):
        _ = mocker.patch(
            "lib.services.configurationservice.ConfigurationService.import_config",
            return_value={"ABCDE": "Updated", "FGHIJ": "Added"})
        m = mocker.patch(
            "lib.managers.configurationmanager.ConfigurationManager.integrate_config",
            return_value=True)
        new_manager = ConfigurationManager()
        new_manager.import_config("testconfig")
        m.assert_called_once()


class Test_GivenAManagerWithBaseConfig:
    def test_WhenAValidConfigIdIsSpecified_ThenGetConfigFromIdReturnsAValue(self):
        new_manager = ConfigurationManager({"ABCDE": "Pass"})
        assert new_manager.getconfigfromid("ABCDE") == "Pass"

    # def test_WhenLoadingAUserConfigFromAFile_ThenTheConfigServiceIsAccessed(self, mocker):

    def test_CM_IC_12_WhenLoadingAUserConfigFromAFile_ThenBaseOptionsAreOverwritten(self, mocker):
        # NEED TO MOCK THE INTERNAL CALL HERE
        _ = mocker.patch(
            "lib.services.configurationservice.ConfigurationService.import_config",
            return_value={"ABCDE": "Updated", "FGHIJ": "Added"})
        new_manager = ConfigurationManager({"ABCDE": "Pass"})
        new_manager.import_config("testconfig")
        assert new_manager.getconfigfromid("FGHIJ") == "Added"
        assert new_manager.getconfigfromid("ABCDE") == "Updated"
