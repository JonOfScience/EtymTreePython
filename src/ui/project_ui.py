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

from core.core import ProjectStatus
from core.project import Project, ProjectBuilder
from core.lexicon import Lexicon, Word
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
        _tree_overview.clicked.connect(
            self._tree_overview_selection_changed)
        # self._tree_overview.doubleClicked.connect(self._tree_overview_double_clicked)
        _tree_model = QStandardItemModel(_tree_overview)
        _tree_overview.setModel(_tree_model)
        tree_layout.addWidget(_tree_overview)

        self.controls.register_control(_tree_overview)

        _word_details = WordDetails()
        layout.addWidget(_word_details.get_layout())
        self.controls.merge_controls_from(_word_details.get_controls())
        details_table: QTableView = self.controls.control_from_id("WordDetailsTable")
        details_model: QStandardItemModel = details_table.model()
        details_model.itemChanged.connect(self._details_model_data_changed)
        self._col_info = {
            "Translated Word": None,
            "Translated Word Components": None,
            "In Language Components": None,
            "Etymological Symbology": None,
            "Compiled Symbology": None,
            "Symbol Mapping": None,
            "Symbol Selection": None,
            "Symbol Pattern Selected": None,
            "Rules Applied": None,
            "In Language Word": None,
            "Version History": None,
            "Has Been Modified Since Last Resolve": None,
            "Has Modified Ancestor": None}

        return layout

    def _add_side_panel(self, layout: QLayout):
        side_panel = QVBoxLayout()
        new_project = QPushButton("New Project")
        new_word = QPushButton("New Word")
        new_word.clicked.connect(self._new_word_clicked)
        side_panel.addWidget(new_project, 1)
        side_panel.addWidget(new_word, 1)
        layout.addLayout(side_panel)
        return layout

    def _tree_overview_selection_changed(self):
        _tree_overview: QTreeView = self.controls.control_from_id("LexiconOverview")
        selected_cell = _tree_overview.selectionModel().selectedIndexes()[0]
        self._selected_item = _tree_overview.model().itemFromIndex(selected_cell)
        self._selected_node: Word = self._selected_item.data()
        # The data formatting & field selection needs to be in a controller (MVC)
        # Don't pass OUT a control, pass IN the text that needs to be set.
        self._word_details_table_populate()

    def _details_model_data_changed(self, item: QStandardItem):
        details_table: QTreeView = self.controls.control_from_id("WordDetailsTable")
        details_model: QStandardItemModel = details_table.model()
        field_label: QStandardItem = details_model.verticalHeaderItem(item.row()).text()
        associated_word: Word = item.data()
        this_project: Project = self.options.find_by_id("CurrentProject")
        this_lexicon: Lexicon = self.options.find_by_id("CurrentLexicon")
        this_lexicon.set_field_to_value(field_label, associated_word, item.text())
        this_project.store()
        # this_lexicon.store_to(f"{this_lexicon.uuid}")
        self._word_details_table_update()
        self._tree_overview_update(this_lexicon)

    def _new_word_clicked(self):
        lexicon: Lexicon = self.options.find_by_id("CurrentLexicon")
        lexicon.create_entry()
        self._window_update()

    def _tree_overview_update(self, lexicon: Lexicon):
        _tree_overview: QTreeView = self.controls.control_from_id("LexiconOverview")
        _tree_model: QStandardItemModel = _tree_overview.model()
        _tree_model.clear()
        _tree_overview.setHeaderHidden(True)
        root = _tree_model.invisibleRootItem()
        for word in lexicon.members:
            new_item = QStandardItem(lexicon.get_field_for_word("Translated Word", word))
            new_item.setData(word)
            root.appendRow(new_item)
        _tree_overview.expandAll()
        _tree_model.sort(0)

    def _word_details_table_update(self):
        word_details_table: QTableView = self.controls.control_from_id("WordDetailsTable")
        word_details_table.horizontalHeader().setHidden(True)
        word_details_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        word_details_table.verticalHeader().setSectionResizeMode(
            # QHeaderView.ResizeToContents
            QHeaderView.Stretch
        )
        word_details_model: QStandardItemModel = word_details_table.model()
        # word_details_model.clear()
        word_details_model.setVerticalHeaderLabels(
            [row_label for (row_label, _) in self._col_info.items()])

    def _word_details_table_populate(self):
        word_details_table: QTableView = self.controls.control_from_id("WordDetailsTable")
        word_details_model: QStandardItemModel = word_details_table.model()
        if self._selected_node:
            this_lexicon: Lexicon = self.options.find_by_id("CurrentLexicon")
            for idx, (col_title, _) in enumerate(self._col_info.items()):
                item_string = this_lexicon.get_field_for_word(
                    col_title,
                    self._selected_node)
                new_item = QStandardItem(item_string)
                new_item.setData(self._selected_node)
                word_details_model.setItem(idx, 0, new_item)

    def _check_focus(self):
        if self.isActiveWindow():
            if self.options.find_by_id("IsLaunching"):
                self.options.set_option_to("IsLaunching", False)
                self._window_launch(self.options.find_by_id("ProjectStatus"))
                self._window_update()

    def _window_launch(self, project_status: ProjectStatus):
        _behaviour_refs = {
            ProjectStatus.LOADING: self._load_existing_project,
            ProjectStatus.NEW: self._create_new_project
        }
        _behaviour_refs[project_status]()

    def _window_update(self):
        project_title = "Undefined"
        this_project: Project = self.options.find_by_id("CurrentProject")
        if this_project:
            project_title = this_project.name
        self.setWindowTitle("EtymTree - Project Overview - (" + project_title + ")")

        this_lexicon: Lexicon = self.options.find_by_id("CurrentLexicon")
        self._tree_overview_update(this_lexicon)
        self._word_details_table_update()

    def _create_new_project(self):
        self.options.set_option_to("ProjectStatus", ProjectStatus.EMPTY)
        new_project = Project()
        new_lexicon = new_project.find_lexicon_by_id(new_project.list_lexicons()[0].uuid)
        self.options.set_option_to("CurrentProject", new_project)
        self.options.set_option_to("CurrentLexicon", new_lexicon)

    def _load_existing_project(self):
        self.options.set_option_to("ProjectStatus", ProjectStatus.SAVED)
        loaded_project = ProjectBuilder.project_from_file(
            self.options.find_by_id("CurrentProjectFile"))
        self.options.set_option_to("CurrentProject", loaded_project)
        self.options.set_option_to("CurrentLexicon", loaded_project.list_lexicons()[0])
