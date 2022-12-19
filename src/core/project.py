"""Library for Project level functionality"""
from __future__ import annotations
import os
import json
from typing import Union, Sequence
from configuration.settings import Settings
from core.lexicon import Lexicon
from core.change_history import LexiconChangeHistory


class ProjectBuilder:
    """Returns Project instances if provided with valid Project data file locations."""
    @staticmethod
    def projects_from_files(location_tree: dict):
        """Given a directory structure as a nested dictionary will return Project instances"""
        proj_files_found = {}
        for (path, directory_data) in location_tree.items():
            for (directory_name, file_names) in directory_data.items():
                for file_name in file_names:
                    rebuilt_proj = ProjectBuilder.project_from_file(
                        os.path.join(path, directory_name, file_name))
                    proj_files_found[rebuilt_proj.name] = rebuilt_proj
        return proj_files_found

    @staticmethod
    def project_from_file(file_location: str) -> Project:
        """Given a Project file path will return an instance of that Project"""
        # REFACTOR - Knows about JSON
        with open(file_location, 'r', encoding='UTF-8') as proj_file:
            proj_data = json.load(proj_file)
        return Project(proj_data)


class Project:
    """Class that contains Project level settings and Lexicons"""
    def __init__(self, settings: Union[dict, Settings] = None) -> None:
        self._settings = Settings(
            {"Name": "ANewProject",
             "Filename": "ANewProjectFile"})
        self._lexicons = {}
        if isinstance(settings, dict):
            self._settings = Settings(settings)
        if isinstance(settings, Settings):
            self._settings = settings
        self._lexicons: Sequence[str, Lexicon] = {}
        self._changehistories: Sequence[str, LexiconChangeHistory] = {}
        registered_lexicons = self._settings.find_by_id("RegisteredLexicons")
        if not registered_lexicons:
            base_blank_lexicon = Lexicon()
            self._lexicons[base_blank_lexicon.uuid] = base_blank_lexicon
            base_blank_change_history = LexiconChangeHistory()
            self._changehistories[base_blank_lexicon.uuid] = base_blank_change_history
            self._settings.set_option_to(
                "RegisteredLexicons",
                [lexicon_id for (lexicon_id, _) in self._lexicons.items()])
            base_blank_lexicon.changehistory = base_blank_change_history
            base_blank_lexicon.resolve_modification_flags()
        else:
            for lexicon_id in registered_lexicons:
                new_lexicon = Lexicon()
                # IS IT DOING FILENAMES CORRECTLY?
                new_lexicon.load_from(lexicon_id)
                self._lexicons[lexicon_id] = new_lexicon
                new_changehistory = LexiconChangeHistory()
                new_changehistory.load_from(lexicon_id)
                self._changehistories[lexicon_id] = new_changehistory
                new_lexicon.changehistory = new_changehistory
                new_lexicon.resolve_modification_flags()

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
        """If identifier exists then a Lexicon is returned, otherwise None"""
        return self._lexicons.get(identifier)

    def find_changehistory_by_id(self, identifier: str) -> LexiconChangeHistory:
        """If identifier exists then a LexiconChangeHistory is returned, otherwise None"""
        return self._changehistories.get(identifier)

    def store(self) -> None:
        """Store Project Files and then Included Lexicon and Change History Files (separately)"""
        # Store Project Settings file "Proj-<ProjID>"
        self._settings.export_config(f"data/PROJ-{self._settings.find_by_id('Filename')}")
        # Store Project Lexicon files "Lex-<LexID>"
        lexicon: Lexicon
        for (lex_id, lexicon) in self._lexicons.items():
            lexicon.store_to(lex_id)
        # Store Project Lexicon Change History files "CHI-<LexID>"
        changehistory: LexiconChangeHistory
        for (lex_id, changehistory) in self._changehistories.items():
            changehistory.store_to(lex_id)
