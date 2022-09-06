import sys
from PyQt5.QtWidgets import (QApplication)
from ui.splash import SplashWindow
from lib.managers.configurationmanager import ConfigurationManager

# BASE CONFIG IS HARDCODED - USER CONFIG IS IN FILES (i.e. can start without user config if need be)
BASE_CONFIG = {"LaunchBehaviour": "Splash"}

if __name__ == '__main__':

    configuration = ConfigurationManager(BASE_CONFIG)

    app = QApplication(sys.argv)
    window = SplashWindow(configuration)
    window.show()

    sys.exit(app.exec_())
