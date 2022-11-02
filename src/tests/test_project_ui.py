"""Test properties and methods of the ProjectWindow UI class"""
from src.configuration.settings import Settings
from src.ui.project_ui import ProjectWindow, ProjectUIController


class TestGivenANewProjectWindow:
    """Tests for a newly instantiated Project window"""
    def test_it_has_an_attribute_called_options(self, qtbot):
        """Each Project window should have an options property on instantiation"""
        new_window = ProjectWindow(Settings())
        qtbot.addWidget(new_window)
        assert hasattr(new_window, "options")


class TestGivenAProjectWindowForANewProject:
    """Tests for the project overview window after a new Lexicon has been constructed"""
    def test_window_title_is_set(self, qtbot):
        """The window should always have a title that isn't 'Undefined'"""
        new_window = ProjectWindow(Settings())
        qtbot.addWidget(new_window)


class TestAProjectUIControllerShould:
    """Tests for the project overview after loading a populated Project"""
    # 6_1_1 Editing "Translated Word Components" splits the input components
    def test_split_the_translated_word_components_string_into_parts(self):
        """Components should have no spaces or '+' characters and be in order"""
        components = ProjectUIController.clean_and_split_string(
            target="Test + multiple + Fragments",
            excluded=[' '],
            separator='+')
        assert components == ["test", "multiple", "fragments"]

    def test_update_component_mappings(self):
        """Only existing components should be found"""
        mapping = {"test": []}
        component_id = "TestFragments"
        components = ["test", "fragments"]

        new_mapping = ProjectUIController.update_component_mapping(
            mapping=mapping,
            component_id=component_id,
            components=components)

        assert new_mapping["TestFragments"] == ["test", "fragments"]
