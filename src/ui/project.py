"""Project screen showing project overview"""
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QWidget)

from lib.core import ProjectStatus, Lexicon, Word
# Replace this with an interface
from configuration.settings import Settings
from ui.interfaces import Controls


class ProjectWindow(QWidget):
    """Window to display project overview and controls to the user"""
    def __init__(self, configuration: Settings) -> None:
        super().__init__()
        self._configuration = configuration
        self.options = Settings()
        self.controls = Controls()
        self.setWindowTitle("EtymTree - Project Overview - (Undefined)")

        self._selected_item = None
        self._selected_node = None

        layout = QHBoxLayout()
        layout = self._add_tree_overview(layout)
        layout = self._add_side_panel(layout)
        self.setLayout(layout)

        QtWidgets.QApplication.instance().focusChanged.connect(self._check_focus)

    def _add_tree_overview(self, layout: QLayout):
        tree_group = QGroupBox("Tree Overview")
        tree_layout = QHBoxLayout()
        tree_group.setLayout(tree_layout)
        layout.addWidget(tree_group)

        _tree_overview = QTreeView()
        _tree_overview.setObjectName("LexiconOverview")
        _tree_overview.clicked.connect(self._tree_overview_selection_changed)
        # self._tree_overview.doubleClicked.connect(self._tree_overview_double_clicked)
        _tree_model = QStandardItemModel()
        _tree_overview.setModel(_tree_model)
        tree_layout.addWidget(_tree_overview)

        self.controls.register_control(_tree_overview)

        details_group = QGroupBox("Word Details")
        details_group.setMinimumWidth(500)
        details_layout = QVBoxLayout()

        word_label_layout = QHBoxLayout()
        translated_word_label = QLabel(text="Translated Word")
        word_label_layout.addWidget(translated_word_label)
        translated_word_data = QLabel(text="No Word Selected")
        word_label_layout.addWidget(translated_word_data)
        details_layout.addLayout(word_label_layout)

        self._details = {"translated_word": translated_word_data}
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)

        return layout

    def _add_side_panel(self, layout: QLayout):
        side_panel = QVBoxLayout()
        new_project = QPushButton("New Project")
        new_word = QPushButton("New Word")
        new_word.clicked.connect(self._tree_overview_double_clicked)
        side_panel.addWidget(new_project, 1)
        side_panel.addWidget(new_word, 1)
        layout.addLayout(side_panel)
        return layout

    def _tree_overview_double_clicked(self):
        lexicon = self.options.find_by_id("CurrentProject")
        lexicon.create_entry()
        print(lexicon)
        self._window_update()

    def _tree_overview_selection_changed(self):
        _tree_overview: QTreeView = self.controls.control_from_id("LexiconOverview")
        selected_cell = _tree_overview.selectionModel().selectedIndexes()[0]
        self._selected_item =  _tree_overview.model().itemFromIndex(selected_cell)
        self._selected_node: Word = self._selected_item.data()
        self._details["translated_word"].setText(self._selected_node.translated_word)
        print(self._selected_node)

    def _tree_overview_update(self, lexicon: Lexicon):
        _tree_overview: QTreeView = self.controls.control_from_id("LexiconOverview")
        _tree_model: QStandardItemModel = _tree_overview.model()
        for word in lexicon.members:
            new_item = QStandardItem(word.translated_word)
            new_item.setData(word)
            _tree_model.appendRow(new_item)

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
