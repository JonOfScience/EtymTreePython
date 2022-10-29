"""Test properties and methods of the SplashWindow UI class"""
from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import QModelIndex
from src.configuration.settings import Settings
from src.ui.splash import SplashWindow
from core.core import ProjectStatus


class TestGivenANewSplashWindow:
    """Tests for a newly instantiated window"""
    def test_it_has_an_attribute_called_options(self, qtbot):
        """Each window should have an options property on instantiation"""
        new_window = SplashWindow(Settings({"ProjectFilePrefix": "TEST-"}))
        qtbot.addWidget(new_window)
        assert hasattr(new_window, "options")


class TestGivenAnEmptyProjectsListInASplashWindow:
    """Example cases for unpopulated Project lists"""
    def test_bork(self, qtbot):
        """1_2_1 - When there are no existing projects, display 'No Projects Available'"""
        new_window = SplashWindow(Settings({"ProjectFilePrefix": "TEST-"}))
        qtbot.addWidget(new_window)
        project_list: QListView = new_window.findChild(QListView, "past_projects")
        project_index: QModelIndex = project_list.model().index(0, 0)
        project_model: QStandardItemModel = project_list.model()
        assert project_model.itemFromIndex(project_index).text() == "No Projects Available"

    # 1_2_2 - When there are no projects then nothing in the list can be selected
    # 1_2_3 - When there are no existing projects in the list then Open Project is disabled.


class TestGivenAPopulatedProjectsListInASplashWindow:
    """Example cases for populated (1+) Project lists"""
    # 1_2_1 - When there are existing projects, display the names of those projects
    # 1_2_2 - When there is at least one project it can be selected
    # 1_2_2 - Not more than one project can be selected
    # 1_2_3 - When there are projects in the list but none are selected,
    #   then clicking Open Project will display an error.
    # 1_2_3 - When there are projects in the list and one is selected,
    #   then click Open Project will open the Project Window with the Project.
