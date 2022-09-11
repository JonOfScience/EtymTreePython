"""Splash screen shown on load"""
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QListView,
    QPushButton,
    QDesktopWidget,
    QVBoxLayout,
    QWidget)

# Replace this with an interface
from configuration.settings import Settings


class SplashWindow(QWidget):
    """Window to display project entry options to the user"""
    def __init__(self, configuration: Settings) -> None:
        super().__init__()
        self._configuration = configuration
        self.setWindowTitle("EtymTree - Splash")
        self.setGeometry(0, 0, 800, 500)
        center_point = QDesktopWidget().availableGeometry().center()
        self.move(center_point.x() - 400, center_point.y() - 250)

        layout = QHBoxLayout()

        past_projects = QListView()
        layout.addWidget(past_projects)

        options_buttons = QVBoxLayout()
        layout.addLayout(options_buttons)

        new_project = QPushButton("New Project")
        options_buttons.addWidget(new_project, 1)
        open_project = QPushButton("Open Project")
        options_buttons.addWidget(open_project, 1)
        exit_program = QPushButton("Exit Program")
        options_buttons.addWidget(exit_program, 1)
        user_settings = QPushButton("User Settings")
        options_buttons.addWidget(user_settings, 1)

        self.setLayout(layout)
