"""Project screen showing project overview"""
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLayout,
    QPushButton,
    QTableView,
    QTreeView,
    QVBoxLayout,
    QWidget)

from lib.core import ProjectStatus, Lexicon, Word
# Replace this with an interface
from configuration.settings import Settings
from ui.interfaces import Controls
from ui.project_word_details import WordDetails


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

        _word_details = WordDetails()
        layout.addWidget(_word_details.get_layout())
        self.controls.merge_controls_from(_word_details.get_controls())
        self._col_info = {
            "Translated Word": Word.translated_word,
            "Translated Word Components": Word.translated_word_components,
            "In Language Components": Word.in_language_components,
            "Etymological Symbology": Word.etymological_symbology,
            "Compiled Symbology": Word.compiled_symbology,
            "Symbol Mapping": Word.symbol_mapping,
            "Symbol Selection": Word.symbol_selection,
            "Symbol Pattern Selected": Word.symbol_pattern_selected,
            "Rules Applied": Word.rules_applied,
            "In Language Word": Word.in_language_word,
            "Version History": Word.version_history,
            "Has Been Modified Since Last Resolve": Word.has_been_modified_since_last_resolve,
            "Has Modified Ancestor": Word.has_modified_ancestor}

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

    def _tree_overview_selection_changed(self):
        _tree_overview: QTreeView = self.controls.control_from_id("LexiconOverview")
        selected_cell = _tree_overview.selectionModel().selectedIndexes()[0]
        self._selected_item =  _tree_overview.model().itemFromIndex(selected_cell)
        self._selected_node: Word = self._selected_item.data()
        this_lexicon: Lexicon = self.options.find_by_id("CurrentProject")
        # The data formatting & field selection needs to be in a controller (MVC)
        # Don't pass OUT a control, pass IN the text that needs to be set.
        word_details_table: QTableView = self.controls.control_from_id("WordDetailsTable")
        word_details_model: QStandardItemModel = word_details_table.model()
        title_item = QStandardItem(self._selected_node.translated_word)
        word_details_model.setItem(0, 1, title_item)
        for idx, (col_title, _) in enumerate(self._col_info.items()):
            item_string = this_lexicon.get_field_for_word(
                col_title,
                self._selected_node.translated_word)
            # print(col_title, col_function)
            # item_string = col_function(self._selected_node)
            new_item = QStandardItem(item_string)
            word_details_model.setItem(idx, 1, new_item)

    def _tree_overview_update(self, lexicon: Lexicon):
        _tree_overview: QTreeView = self.controls.control_from_id("LexiconOverview")
        _tree_model: QStandardItemModel = _tree_overview.model()
        for word in lexicon.members:
            new_item = QStandardItem(word.translated_word)
            new_item.setData(word)
            _tree_model.appendRow(new_item)

    def _word_details_table_update(self):
        word_details_table: QTableView = self.controls.control_from_id("WordDetailsTable")
        word_details_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        word_details_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        word_details_model: QStandardItemModel = word_details_table.model()
        word_details_model.clear()
        for idx, (row_label, row_function) in enumerate(self._col_info.items()):
            label_item = QStandardItem(row_label)
            word_details_model.setItem(idx, 0, label_item)
            data_item = QStandardItem(row_function)
            word_details_model.setItem(idx, 1, data_item)

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
        self._word_details_table_update()

    def _create_new_project(self):
        self.options.set_option_to("ProjectStatus", ProjectStatus.EMPTY)
        self.options.set_option_to("CurrentProject", Lexicon())
