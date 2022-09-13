"""Project screen showing project overview"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget)

# Replace this with an interface
from lib.core import ProjectStatus
from configuration.settings import Settings


class ProjectWindow(QWidget):
    """Window to display project overview and controls to the user"""
    def __init__(self, configuration: Settings) -> None:
        super().__init__()
        self._configuration = configuration
        self.options = Settings()
        self.setWindowTitle("EtymTree - Project Overview")

        layout = QHBoxLayout()

        tree_overview = QLabel()
        layout.addWidget(tree_overview)

        side_panel = QVBoxLayout()
        layout.addLayout(side_panel)

        new_project = QPushButton("New Project")
        side_panel.addWidget(new_project, 1)

        self.setLayout(layout)
        QtWidgets.QApplication.instance().focusChanged.connect(self._check_focus)

    def _check_focus(self):
        if self.isActiveWindow():
            if self.options.find_by_id("IsLaunching"):
                self.options.set_option_to("IsLaunching", False)
                self._window_launch(self.options.find_by_id("ProjectStatus"))

    def _window_launch(self, project_status: ProjectStatus):
        _behaviour_refs = {
            ProjectStatus.NEW: self._create_new_project
        }
        _behaviour_refs[project_status]()

    def _create_new_project(self):
        self.options.set_option_to("ProjectStatus", ProjectStatus.EMPTY)
