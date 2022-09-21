"""Test properties and methods of the ProjectWindow UI class"""
from src.configuration.settings import Settings
from src.ui.project import ProjectWindow


class TestGivenANewProjectWindow:
    """Tests for a newly instantiated Project window"""
    def test_it_has_an_attribute_called_options(self, qtbot):
        """Each Project window should have an options property on instantiation"""
        new_window = ProjectWindow(Settings())
        qtbot.addWidget(new_window)
        assert hasattr(new_window, "options")

    def test_the_options_attribute_is_a_settings_object(self, qtbot):
        """The options is a window-level Settings object"""
        new_window = ProjectWindow(Settings())
        qtbot.addWidget(new_window)
        assert isinstance(new_window.options, Settings)


class TestGivenAProjectWindowForANewProject:
    """Tests for the project overview window after a new Lexicon has been constructed"""
    def test_window_title_is_set(self, qtbot):
        """The window should always have a title that isn't 'Undefined'"""
        pass
