"""Tests for a Project that will contain Lexicons of Words."""
from core.project import Project
from core.lexicon import Lexicon


class TestANewEmptyProjectShould:
    """Tests for a newly created Project"""
    def test_be_able_to_be_instantiated_empty(self):
        """Placeholder: State Test"""
        assert Project()

    def test_have_a_default_project_name(self):
        """Placeholder: State Test"""
        assert Project().name

    def test_have_a_default_output_filename(self):
        """Placeholder: State Test"""
        assert Project().filename

    def test_have_a_base_lexicon(self):
        """Placeholder: State Test"""
        assert Project().list_lexicons()

    def test_be_able_to_retrieve_a_lexicon_by_identifier(self):
        """Placeholder: State Test"""
        empty_project = Project()
        base_lexicon: Lexicon = empty_project.list_lexicons()[0]
        assert empty_project.find_lexicon_by_id(base_lexicon.uuid)


class TestANewProjectWithDefinedSettingsShould:
    """Tests for a Project created with predefined settings"""
    def test_be_able_to_be_instantiated(self):
        """Placeholder: State Test"""
        assert Project(settings={"Name": "TestProjectSettings"})

    def test_import_a_defined_name(self):
        """Placeholder: State Test"""
        assert Project(settings={"Name": "TestProjectSettings"}).name == "TestProjectSettings"
