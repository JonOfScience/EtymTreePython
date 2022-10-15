"""Splash screen shown on load"""
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QListView,
    QPushButton,
    QDesktopWidget,
    QVBoxLayout,
    QWidget)

# Replace this with an interface
from core.core import ProjectStatus
from configuration.settings import Settings
from ui.interfaces import EtymWindow


class SplashWindow(QWidget):
    """Window to display project entry options to the user"""
    def __init__(self, configuration: Settings) -> None:
        super().__init__()
        self._configuration = configuration
        self.options = Settings()
        self.setWindowTitle("EtymTree - Splash")
        self.setGeometry(0, 0, 800, 500)
        center_point = QDesktopWidget().availableGeometry().center()
        self.move(center_point.x() - 400, center_point.y() - 250)

        layout = QHBoxLayout()

        past_projects = QListView()
        past_projects.setObjectName("past_projects")
        past_projects_model = QStandardItemModel()
        past_projects.setModel(past_projects_model)
        past_projects_model.appendRow(QStandardItem("No Projects Available"))
        layout.addWidget(past_projects)

        options_buttons = QVBoxLayout()
        layout.addLayout(options_buttons)

        new_project = QPushButton("New Project")
        options_buttons.addWidget(new_project, 1)
        new_project.clicked.connect(self._click_on_new_project)
        open_project = QPushButton("Open Project")
        options_buttons.addWidget(open_project, 1)
        exit_program = QPushButton("Exit Program")
        options_buttons.addWidget(exit_program, 1)
        user_settings = QPushButton("User Settings")
        options_buttons.addWidget(user_settings, 1)

        self.setLayout(layout)

    def _click_on_new_project(self):
        project_overview_window: EtymWindow = self._configuration.find_by_id("MainWindow")
        project_overview_window.options.set_option_to("ProjectStatus", ProjectStatus.NEW)
        project_overview_window.options.set_option_to("IsLaunching", True)
        project_overview_window.showMaximized()
        self.close()
