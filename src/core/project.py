"""Library for Project level functionality"""
from typing import Union
from configuration.settings import Settings
from src.core.lexicon import Lexicon


class Project:
    def __init__(self, settings: Union[dict, Settings] = None) -> None:
        self._settings = Settings(
            {"Name": "ANewProject",
             "Filename": "ANewProjectFile"})
        if isinstance(settings, dict):
            self._settings = Settings(settings)
        if isinstance(settings, Settings):
            self._settings = settings
        base_blank_lexicon = Lexicon()
        self._lexicons = {base_blank_lexicon.uuid: base_blank_lexicon}

    @property
    def name(self) -> str:
        return self._settings.find_by_id("Name")

    @property
    def filename(self) -> str:
        return self._settings.find_by_id("Filename")

    def list_lexicons(self) -> list[Lexicon]:
        """A list of all registered Lexicons"""
        return [x for (_, x) in self._lexicons.items()]

    def find_lexicon_by_id(self, identifier: str) -> Lexicon:
        """If identifier exists then a Lexicon is return, otherwise None"""
        return self._lexicons.get(identifier)
