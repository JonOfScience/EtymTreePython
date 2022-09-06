from PyQt5.QtWidgets import (
    QHBoxLayout,
    QListView,
    QPushButton,
    QDesktopWidget,
    QVBoxLayout,
    QWidget)

# Replace this with an interface
from lib.managers.configurationmanager import ConfigurationManager

class SplashWindow(QWidget):
    def __init__(self, configuration: ConfigurationManager) -> None:
        super().__init__()
        self.setWindowTitle("EtymTree - Splash")
        self.setGeometry(0, 0, 800, 500)
        cp = QDesktopWidget().availableGeometry().center()
        self.move(cp.x() - 400, cp.y() - 250)        
        
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
        
        self.setLayout(layout)
