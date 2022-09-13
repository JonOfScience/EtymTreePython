"""A project to allow the tracking, mapping, and modification of vocabulary."""

import sys
from PyQt5.QtWidgets import (QApplication)
from configuration.settings import Settings
from ui.splash import SplashWindow
from ui.project import ProjectWindow

# BASE CONFIG IS HARDCODED
# USER CONFIG IS IN FILES (i.e. can start without user config if need be)

BASE_CONFIG = {
    "LaunchBehaviour": "Splash",
    "DefaultFormat": "JSON",
    "DefaultUserConfig": "UserConfig",
    "SplashWindow": None,
    "MainWindow": None}

if __name__ == '__main__':
    configuration = Settings(BASE_CONFIG)
    configuration.import_config(BASE_CONFIG["DefaultUserConfig"])

    app = QApplication(sys.argv)
    splashwindow = SplashWindow(configuration)
    mainwindow = ProjectWindow(configuration)
    configuration.integrate_config({
        "SplashWindow": splashwindow,
        "MainWindow": mainwindow})
    splashwindow.show()

    sys.exit(app.exec_())
