from lib.managers.configurationmanager import ConfigurationManager

class Test_GivenANewManager:
    def test_WhenAnInvalidConfigIdIsSpecified_ThenGetConfigFromIdReturnsNone(self):
        new_manager = ConfigurationManager()
        assert new_manager.getconfigfromid("ABCDE") is None

class Test_GivenAManagerWithBaseConfig:
    def test_WhenAValidConfigIdIsSpecified_ThenGetConfigFromIdReturnsAValue(self):
        new_manager = ConfigurationManager({"ABCDE": "Pass"})
        assert new_manager.getconfigfromid("ABCDE") == "Pass"
    
    # def test_WhenLoadingAUserConfigFromAFile_ThenTheConfigServiceIsAccessed(self, mocker):

    # def test_CM_IC_12_WhenLoadingAUserConfigFromAFile_ThenBaseOptionsAreOverwritten(self):
    #     # NEED TO MOCK THE INTERNAL CALL HERE
    #     new_manager = ConfigurationManager({"ABCDE": "Pass"})
    #     new_manager.import_config("testconfig")
    #     assert new_manager.getconfigfromid("FGHIJ") == "Added"
    #     assert new_manager.getconfigfromid("ABCDE") == "Updated"
