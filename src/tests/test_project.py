"""Test properties and methods of the ProjectWindow UI class"""
from configuration.settings import Settings
from ui.project import ProjectWindow

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
