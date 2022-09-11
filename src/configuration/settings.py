"""Application configuration settings"""
from services.settings_io_service import SettingsIOService
from lib.core import DataFormat


class Settings:
    """Settings capable of Read and Import"""
    def __init__(self, configuration: dict = None, context: SettingsIOService = None) -> None:
        if configuration is not None:
            self._config_data = configuration
        else:
            self._config_data = dict()

        if context is not None:
            self._context = context
        else:
            new_service = SettingsIOService(data_format=DataFormat.JSON)
            self._context = new_service

    def find_by_id(self, value_id: str):
        """Returns configuration value for specified value_id or None"""
        return self._config_data.get(value_id)

    def import_config(self, filename: str):
        """Public method to import and then integrate external configuration settings"""
        config_updates = self._context.import_config(filename)
        return self.integrate_config(config_updates)

    def integrate_config(self, config_updates: dict):
        """Inclusively integrates and updates a dictionary of key/value pairs"""
        for config_id in config_updates:
            self._config_data[config_id] = config_updates[config_id]
        return len(config_updates)
