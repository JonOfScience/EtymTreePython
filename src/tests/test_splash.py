"""Test properties and methods of the SplashWindow UI class"""
from configuration.settings import Settings
from ui.splash import SplashWindow

class TestGivenANewSplashWindow:
    """Tests for a newly instantiated window"""
    def test_it_has_an_attribute_called_options(self, qtbot):
        """Each window should have an options property on instantiation"""
        new_window = SplashWindow(Settings())
        qtbot.addWidget(new_window)
        assert hasattr(new_window, "options")

    def test_the_options_attribute_is_a_settings_object(self, qtbot):
        """The options a window-level Settings object"""
        new_window = SplashWindow(Settings())
        qtbot.addWidget(new_window)
        assert isinstance(new_window.options, Settings)
