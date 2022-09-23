"""Project screen showing project overview"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QVBoxLayout,
    QWidget)

# Replace this with an interface
from lib.core import ProjectStatus, double_clickable, Lexicon
import networkx as nx
from configuration.settings import Settings
# import matplotlib.pyplot as plt


class ProjectWindow(QWidget):
    """Window to display project overview and controls to the user"""
    def __init__(self, configuration: Settings) -> None:
        super().__init__()
        self._configuration = configuration
        self.options = Settings()
        self.lexicon_overview = None
        self.setWindowTitle("EtymTree - Project Overview - (Undefined)")

        layout = QHBoxLayout()
        layout = self._add_tree_overview(layout)
        layout = self._add_side_panel(layout)
        self.setLayout(layout)

        QtWidgets.QApplication.instance().focusChanged.connect(self._check_focus)

    def _add_tree_overview(self, layout: QLayout):
        tree_group = QGroupBox("Tree Overview")
        tree_layout = QVBoxLayout()
        tree_group.setLayout(tree_layout)
        layout.addWidget(tree_group)

        tree_overview = QLabel("Empty")
        self.lexicon_overview = tree_overview
        double_clickable(tree_overview).connect(self._tree_overview_double_clicked)
        # tree_overview.clicked.connect(self._tree_overview_double_clicked)

        tree_layout.addWidget(tree_overview)
        # layout.addWidget(tree_overview)
        return layout

    def _add_side_panel(self, layout: QLayout):
        side_panel = QVBoxLayout()
        new_project = QPushButton("New Project")
        side_panel.addWidget(new_project, 1)
        layout.addLayout(side_panel)
        return layout

    def _tree_overview_double_clicked(self):
        lexicon = self.options.find_by_id("CurrentProject")
        lexicon.create_entry()
        self._window_update()

    def _tree_overview_update(self, lexicon: Lexicon):
        lex_graph = nx.Graph()
        for word in lexicon.get_all_words():
            lex_graph.add_node("BORK")

        self.lexicon_overview.setText(f"Lexicon contains {len(lexicon.members)} entries")
        if lexicon.members:
            print(lexicon.members[0])

    def _check_focus(self):
        if self.isActiveWindow():
            if self.options.find_by_id("IsLaunching"):
                self.options.set_option_to("IsLaunching", False)
                self._window_launch(self.options.find_by_id("ProjectStatus"))
                self._window_update()

    def _window_launch(self, project_status: ProjectStatus):
        _behaviour_refs = {
            ProjectStatus.NEW: self._create_new_project
        }
        _behaviour_refs[project_status]()

    def _window_update(self):
        this_lexicon: Lexicon = self.options.find_by_id("CurrentProject")
        self._tree_overview_update(this_lexicon)

    def _create_new_project(self):
        self.options.set_option_to("ProjectStatus", ProjectStatus.EMPTY)
        self.options.set_option_to("CurrentProject", Lexicon())
