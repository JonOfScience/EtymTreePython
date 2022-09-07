from lib.services.configurationservice import ConfigurationService
from lib.core import DataFormat

from lib.services.io_service import IOService


class Test_GivenANewConfigService:
    def test_CM_IC_2_AServiceWillCallDeserialiseStoredOnImport(self, mocker):
        m = mocker.patch("lib.services.io_service.IOService.deserialise_stored", return_value="")
        new_config_service = ConfigurationService(IOService(DataFormat.JSON))
        _ = new_config_service.import_config("TestConfig")
        m.assert_called_once()

    def test_CM_IC_9_AServiceReturnADeserialisedObjectOnImport(self, mocker):
        _ = mocker.patch(
            "lib.services.io_service.IOService.deserialise_stored",
            return_value={"A": "B", "C": 1})
        new_config_service = ConfigurationService(IOService(DataFormat.JSON))
        config_object = new_config_service.import_config("TestConfig")
        assert config_object == {"A": "B", "C": 1}
