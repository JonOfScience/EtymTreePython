"""A project to allow the tracking, mapping, and modification of vocabulary."""

import logging
import sys
from PyQt5.QtWidgets import (QApplication)
from configuration.settings import Settings
from ui.splash import SplashWindow
from ui.project_ui import ProjectWindow

# BASE CONFIG IS HARDCODED
# USER CONFIG IS IN FILES (i.e. can start without user config if need be)

BASE_CONFIG = {
    "LaunchBehaviour": "Splash",
    "DataFileFormat": "JSON",
    "DefaultUserConfig": "UserConfig",
    "ProjectFilePrefix": "PROJ-",
    "LexiconFilePrefix": "LEX-",
    "SplashWindow": None,
    "MainWindow": None}

if __name__ == '__main__':

    logger = logging.getLogger('etym_logger')
    logger.setLevel(logging.DEBUG)
    f_handler = logging.FileHandler('app.log', 'w')
    f_format = logging.Formatter(
        '%(asctime)s - %(levelname)s: Location [%(module)s -> %(funcName)s] - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)

    configuration = Settings(BASE_CONFIG)
    configuration.import_config(BASE_CONFIG["DefaultUserConfig"])

    logger.debug("Application Start")

    app = QApplication(sys.argv)
    splashwindow = SplashWindow(configuration)
    mainwindow = ProjectWindow(configuration)
    configuration.integrate_config({
        "SplashWindow": splashwindow,
        "MainWindow": mainwindow})
    splashwindow.show()

    sys.exit(app.exec_())
