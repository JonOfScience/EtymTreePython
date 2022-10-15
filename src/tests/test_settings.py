"""Tests for configuration Settings."""
import sys
import pytest
from core.core import DataFormat
from src.configuration.settings import Settings
from src.services.settings_io_service import SettingsIOService


def _write_testdata_data_file():
    parts = sys.path[0].split(sep="\\")
    parts.extend(["src", "tests", "data"])
    testdatapath = "/".join(parts)
    with open(f"{testdatapath}/testdata.data", 'w', encoding='UTF-8') as file:
        file.writelines(['{"A": "B", "C": 1}'])
    return testdatapath


class TestGivenEmptySettings:
    """Test operations on an empty settings store"""
    def test_set_ist_00_can_be_constructed_empty(self):
        """State Test"""
        empty_settings = Settings()
        assert empty_settings

    def test_set_ist_01_can_be_constructed_with_data(self):
        """State Test"""
        config_data = {"ABCDE": "FGHIJ", "KLMNO": 1}
        settings_with_data = Settings(configuration=config_data)
        assert settings_with_data

    def test_set_ist_02_can_be_constructed_with_a_context(self):
        """State Test"""
        settings_with_context = Settings(context=SettingsIOService(data_format=DataFormat.JSON))
        assert settings_with_context

    def test_set_inc_00_will_integrate_clean_values_into_settings(self):
        """State Test"""
        empty_settings = Settings()
        empty_settings.integrate_config({"A": "B", "C": 1})
        assert empty_settings.find_by_id("A") == "B"
        assert empty_settings.find_by_id("C") == 1

    def test_set_inc_03_will_throw_when_trying_to_integrate_none(self):
        """State Test?"""
        empty_settings = Settings()
        with pytest.raises(Exception) as e_info:
            empty_settings.integrate_config(None)
        assert e_info.type == TypeError

    def test_set_inc_04_will_throw_when_trying_to_integrate_a_non_dictonary(self):
        """State Test?"""
        empty_settings = Settings()
        with pytest.raises(Exception) as e_info:
            empty_settings.integrate_config(["NotADict", "StillNotADict"])
        assert e_info.type == TypeError

    # LINKED TO FIND_BY_ID
    # def test_when_any_setting_is_requested_then_none_is_returned(self):
    #     """State Test"""
    #     empty_settings = Settings()
    #     assert empty_settings.find_by_id("ABCDE") is None

    # def test_cm_ic_11_the_manager_calls_integrate_config(self, mocker):
    #     """Behaviour Test"""
    #     _ = mocker.patch(
    #         "src.services.settings_io_service.SettingsIOService.import_config",
    #         return_value={"ABCDE": "Updated", "FGHIJ": "Added"})
    #     mock_service = mocker.patch(
    #         "src.configuration.settings.Settings.integrate_config",
    #         return_value=True)
    #     empty_settings = Settings()
    #     empty_settings.import_config("testconfig")
    #     mock_service.assert_called_once()

    # def test_when_item_is_specified_then_the_value_is_created(self):
    #     """The Settings object should now contain the id"""
    #     new_settings = Settings()
    #     new_settings.set_option_to("ABCDE", "FGHIJ")
    #     assert new_settings.find_by_id("ABCDE")

    # def test_when_an_item_created_then_the_value_is_correct(self):
    #     """The value of the specified key should be correct"""
    #     new_settings = Settings()
    #     new_settings.set_option_to("ABCDE", "FGHIJ")
    #     assert new_settings.find_by_id("ABCDE") == "FGHIJ"


class TestGivenAnExistingConfiguration:
    """Test if configuration options can be read and (over)written."""
    def test_when_a_valid_id_is_specified_then_the_setting_value_is_returned(self):
        """State Test"""
        config = Settings({"ABCDE": "Pass"})
        assert config.find_by_id("ABCDE") == "Pass"

    def test_set_inc_01_integrates_empty_config_without_deletion(self):
        """State Test"""
        empty_settings = Settings(configuration={"A": "B", "C": 1})
        empty_settings.integrate_config({})
        assert empty_settings.find_by_id("A") == "B"
        assert empty_settings.find_by_id("C") == 1

    def test_set_inc_02_integrates_config_with_overwriting(self):
        """State Test"""
        empty_settings = Settings(configuration={"A": "B", "C": 1})
        empty_settings.integrate_config({"C": "D"})
        assert empty_settings.find_by_id("A") == "B"
        assert empty_settings.find_by_id("C") == "D"

    def test_set_imc_00_base_entries_are_overwritten_when_importing_config(self):
        """State Test"""
        testdatapath = _write_testdata_data_file()
        config = Settings({"A": "Pass"})
        config.import_config(f"{testdatapath}/testdata")
        assert config.find_by_id("A") == "B"
        assert config.find_by_id("C") == 1
