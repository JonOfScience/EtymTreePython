"""Library for Project level functionality"""
from typing import Union, Sequence
from configuration.settings import Settings
from src.core.lexicon import Lexicon


class Project:
    """Class that contains Project level settings and Lexicons"""
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
        """The descriptive name of the project"""
        return self._settings.find_by_id("Name")

    @property
    def filename(self) -> str:
        """The non-extension file name to which the Project will be saved"""
        return self._settings.find_by_id("Filename")

    def list_lexicons(self) -> Sequence[Lexicon]:
        """A list of all registered Lexicons"""
        return [x for (_, x) in self._lexicons.items()]

    def find_lexicon_by_id(self, identifier: str) -> Lexicon:
        """If identifier exists then a Lexicon is return, otherwise None"""
        return self._lexicons.get(identifier)
