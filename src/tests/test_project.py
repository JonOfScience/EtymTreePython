"""Tests for a Project that will contain Lexicons of Words."""
from core.project import Project
from core.lexicon import Lexicon


class TestANewEmptyProjectShould:
    """Tests for a newly created Project"""
    def test__prj_ist_00__be_able_to_be_instantiated_empty(self):
        """Placeholder: State Test"""
        assert Project()

    def test__prj_ist_01__have_a_default_project_name(self):
        """Placeholder: State Test"""
        assert Project().name

    def test__prj_ist_02__have_a_default_output_filename(self):
        """Placeholder: State Test"""
        assert Project().filename

    def test__prj_ist_03__have_a_base_lexicon(self):
        """Placeholder: State Test"""
        assert Project().list_lexicons()

    def test__prj_ler_01__be_able_to_retrieve_a_lexicon_by_identifier(self):
        """Placeholder: State Test"""
        empty_project = Project()
        base_lexicon: Lexicon = empty_project.list_lexicons()[0]
        assert empty_project.find_lexicon_by_id(base_lexicon.uuid)

    def test__prj_sto_00__be_able_to_be_stored_locally(self, mocker):
        """Placeholder: State Test"""
        empty_project = Project({"Filename": "TestProject"})
        mock_method = mocker.patch("builtins.open")
        empty_project.store()
        assert mock_method.called

    def test__prj_sto_01__store_three_files_locally_for_an_empty_project(self, mocker):
        """Placeholder: State Test"""
        empty_project = Project({"Filename": "TestProject"})
        mock_method = mocker.patch("builtins.open")
        empty_project.store()
        assert mock_method.call_count == 3


class TestANewProjectWithDefinedSettingsShould:
    """Tests for a Project created with predefined settings"""
    def test__prj_ist_04__be_able_to_be_instantiated(self):
        """Placeholder: State Test"""
        assert Project(settings={"Name": "TestProjectSettings"})

    def test__prj_ist_05__import_a_defined_name(self):
        """Placeholder: State Test"""
        assert Project(settings={"Name": "TestProjectSettings"}).name == "TestProjectSettings"
