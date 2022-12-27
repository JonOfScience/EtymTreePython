"""Project screen showing project overview"""
from typing import Sequence
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
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
from core.change_history import LexiconChangeHistory
from core.change_history_item import ChangeHistoryItem
from core.lexicon import Lexicon
from core.word import Word
# Replace this with an interface
from configuration.settings import Settings
from ui.interfaces import Controls
from ui.project_word_details import WordDetails


class ProjectUIController:
    """Static class to provide Controller functions to ProjectWindow"""
    @staticmethod
    def clean_and_split_string(target: str, excluded: Sequence[str]=None, separator: str='+'):
        """Removes all instances of excluded characters and then splits by separator

        excluded: default value [' ']
        separator: default value '+'
        """
        if excluded is None:
            excluded = [' ']
        if not target:
            return []
        target = target.lower()
        for character in excluded:
            target = target.replace(character, '')
        return target.split(sep = separator)

    @staticmethod
    def split_and_trim_string(target: str, separator: str='+'):
        """Splits a string by a separator and trims the fragments"""
        if not target:
            return []
        fragments = target.split(sep=separator)
        trimmed = [" "] * len(fragments)
        for ind, value in enumerate(fragments):
            trimmed[ind] = str.strip(value)
        return trimmed

    @staticmethod
    def update_component_mapping(mapping: dict, component_id: str, components: Sequence[str]):
        """Updates component mapping with split component data.
        Components are in order.
        Component values are True if the component word exists in the mapping."""
        mapping[component_id] = components
        return mapping


class ProjectWindow(QWidget):
    """Window to display project overview and controls to the user"""
    def __init__(self, configuration: Settings) -> None:
        super().__init__()
        self._configuration = configuration
        self.options = Settings()
        self.controls = Controls()

        self._selected_node = None
        self._selected_change_node = None

        self._translated_component_mapping = {}

        modified_status_colours = {
            True: QBrush(QColor(255, 0, 0)),
            False: QBrush(QColor(0, 0, 0))}
        ancestor_status_colours = {
            True: QBrush(QColor(243, 207, 198)),
            False: QBrush(QColor(255, 255, 255))}
        self.options.set_option_to("ModStatusColours", modified_status_colours)
        self.options.set_option_to("AncStatusColours", ancestor_status_colours)

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
        # COL INFO CONTAINS TYPE OF COLUMN
        # "Translated Word": ColType.FIELD  ->  A field of the Word object
        # "Translated Word Component Status": ColType.INVIEW  ->  Calculated in the view (a fn?)
        self._col_info = {
            "Translated Word":
                {"ColType": None},
            "Translated Word Components":
                {"ColType": None, "ColFormatter": self._format_twc},
            "In Language Components":
                {"ColType": None},
            "Etymological Symbology":
                {"ColType": None},
            "Compiled Symbology":
                {"ColType": None},
            "Symbol Mapping":
                {"ColType": None},
            "Symbol Selection":
                {"ColType": None},
            "Symbol Pattern Selected":
                {"ColType": None},
            "Rules Applied":
                {"ColType": None},
            "In Language Word":
                {"ColType": None},
            "Is Related To":
                {"ColType": None}}

        history_table: QTableView = self.controls.control_from_id("ChangeHistoryTable")
        history_table.clicked.connect(
            self._change_history_selection_changed)

        _resolve_btn: QPushButton = self.controls.control_from_id("ResolveChangeBtn")
        _resolve_btn.clicked.connect(self._resolve_change_btn_clicked)

        return layout

    def _format_twc(self, twc_list: Sequence[str]) -> str:
        return " + ".join(twc_list)

    def _format_vh(self, vh_list: Sequence[str]) -> str:
        this_changehistory: LexiconChangeHistory = self.options.find_by_id("CurrentChangeHistory")
        return_items = []
        for list_item in vh_list:
            found_item = this_changehistory.find_item_with_id(list_item)
            if found_item is not None:
                return_items.append(found_item.description)
        return "\n".join(return_items)

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
        _selected_item = _tree_overview.model().itemFromIndex(selected_cell)
        self._selected_node: Word = _selected_item.data()
        # The data formatting & field selection needs to be in a controller (MVC)
        # Don't pass OUT a control, pass IN the text that needs to be set.
        self._word_details_table_populate()
        self._changehistory_table_populate()

    def _change_history_selection_changed(self):
        _change_history: QTreeView = self.controls.control_from_id("ChangeHistoryTable")
        selected_row = _change_history.selectionModel().selectedIndexes()[0]
        _selected_change_item = _change_history.model().itemFromIndex(selected_row)
        self._selected_change_node: ChangeHistoryItem = _selected_change_item.data()
        _resolve_btn: QPushButton = self.controls.control_from_id("ResolveChangeBtn")
        if self._selected_change_node and not _resolve_btn.isEnabled():
            _resolve_btn.setEnabled(True)
        else:
            _resolve_btn.setEnabled(False)

    def _resolve_change_btn_clicked(self):
        if self._selected_change_node and self._selected_node:
            self.current_lexicon.resolve_change_for(self._selected_change_node, self._selected_node)
            self._tree_overview_update()
            self._changehistory_table_populate()
            this_project: Project = self.options.find_by_id("CurrentProject")
            this_project.store()
            self.controls.control_from_id("ResolveChangeBtn").setEnabled(False)

    def _details_model_data_changed(self, item: QStandardItem):
        details_table: QTreeView = self.controls.control_from_id("WordDetailsTable")
        details_model: QStandardItemModel = details_table.model()
        field_label: QStandardItem = details_model.verticalHeaderItem(item.row()).text()
        associated_word: Word = item.data()
        this_project: Project = self.options.find_by_id("CurrentProject")
        this_lexicon = self.current_lexicon
        this_changehistory: LexiconChangeHistory = self.options.find_by_id("CurrentChangeHistory")
        new_value = item.text()
        if field_label == "Translated Word Components":
            word_components = ProjectUIController.split_and_trim_string(target=new_value)
            new_value = word_components

        change_history_item = this_lexicon.set_field_to_value(
            field_label,
            associated_word,
            new_value)
        this_changehistory.add_item(change_history_item)
        this_project.store()

        if field_label == "Translated Word":
            self._build_translated_component_mappings()
        if field_label == "Translated Word Components":
            self._translated_component_mapping = ProjectUIController.update_component_mapping(
                mapping=self._translated_component_mapping,
                component_id=this_lexicon.get_field_for_word("Translated Word", associated_word),
                components=word_components)
        if field_label == "Etymological Symbology":
            item.setText(this_lexicon.get_field_for_word("Etymological Symbology", associated_word))

        self._word_details_table_update()
        self._tree_overview_update()
        self._changehistory_table_populate()

    def _new_word_clicked(self):
        self.current_lexicon.create_entry()
        self._build_translated_component_mappings()
        self._window_update()

    def _get_item_status_colour(self, palette_name: str, colour_key):
        return self.options.find_by_id(palette_name).get(colour_key)

    def _tree_overview_update(self, lexicon: Lexicon = None):
        _root_char = '\N{seedling}'

        if lexicon is None:
            lexicon = self.current_lexicon

        # Get View, Model and Root - Clear Model, Set Header to Hidden
        _tree_overview: QTreeView = self.controls.control_from_id("LexiconOverview")
        _tree_model: QStandardItemModel = _tree_overview.model()
        _tree_model.clear()
        _tree_overview.setHeaderHidden(True)
        root = _tree_model.invisibleRootItem()

        # For each Word
        for word in lexicon.members:
            # Get data about the Word
            translated_word = lexicon.get_field_for_word("Translated Word", word)
            word_components = self._translated_component_mapping[translated_word]
            _display_char = '\N{herb}'
            if len(lexicon.get_field_for_word("Translated Word Components", word)) < 1:
                _display_char = _root_char
            display_text = _display_char + f" {translated_word}"
            if word_components:
                display_text += f" [{', '.join(word_components)}]"

            # Use data from thw Word to create the Item
            new_item = QStandardItem(display_text)
            new_item.setData(word)

            foreground_colour = self._get_item_status_colour(
                "ModStatusColours",
                word.has_unresolved_modification)
            if foreground_colour is not None:
                new_item.setForeground(foreground_colour)

            background_colour = self._get_item_status_colour(
                "AncStatusColours",
                word.has_modified_ancestor)
            if background_colour is not None:
                new_item.setBackground(background_colour)

            # Add new Item to the model
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
            this_lexicon = self.current_lexicon
            for idx, (col_title, col_settings) in enumerate(self._col_info.items()):
                item_data = this_lexicon.get_field_for_word(
                    col_title,
                    self._selected_node)
                if "ColFormatter" in col_settings:
                    item_data = col_settings["ColFormatter"](item_data)
                else:
                    if isinstance(item_data, list):
                        item_data = "\n".join(item_data)
                new_item = QStandardItem(item_data)
                new_item.setData(self._selected_node)
                word_details_model.setItem(idx, 0, new_item)

    def _changehistory_table_update(self):
        table: QTableView = self.controls.control_from_id("ChangeHistoryTable")
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        table.verticalHeader().setSectionResizeMode(
            # QHeaderView.ResizeToContents
            QHeaderView.Stretch
        )
        model: QStandardItemModel = table.model()
        model.setHorizontalHeaderLabels(["Change Description", "Resolved"])

    def _changehistory_table_populate(self):
        changes_table: QTableView = self.controls.control_from_id("ChangeHistoryTable")
        changes_model: QStandardItemModel = changes_table.model()
        changes_model.clear()
        self._changehistory_table_update()

        change_history = self.current_changehistory
        if self._selected_node:
            this_lexicon = self.current_lexicon
            item_data = this_lexicon.get_field_for_word(
                "Version History",
                self._selected_node)
            for idx, change_data in enumerate(item_data):
                logged_item = change_history.find_item_with_id(change_data)
                resolved = self._selected_node.has_resolved_change_with_id(change_data)
                resolve_description = QStandardItem(str(resolved))
                resolve_description.setData(logged_item)
                if logged_item is not None:
                    change_description = QStandardItem(logged_item.description)
                else:
                    change_description = QStandardItem(change_data)
                change_description.setData(logged_item)
                changes_model.setItem(idx, 0, change_description)
                changes_model.setItem(idx, 1, resolve_description)
        changes_model.sort(1)

    def _check_focus(self):
        if self.isActiveWindow():
            if self.options.find_by_id("IsLaunching"):
                self.options.set_option_to("IsLaunching", False)
                self._window_launch(self.options.find_by_id("ProjectStatus"))
                self._window_update()

    def _build_translated_component_mappings(self):
        this_lexicon = self.current_lexicon
        all_words = this_lexicon.get_all_words()
        for word in all_words:
            translated_word = this_lexicon.get_field_for_word("Translated Word", word)
            translated_components = this_lexicon.get_field_for_word(
                "Translated Word Components",
                word)
            components = translated_components
            self._translated_component_mapping = ProjectUIController.update_component_mapping(
                mapping=self._translated_component_mapping,
                component_id=translated_word,
                components=components)

    def _window_launch(self, project_status: ProjectStatus):
        _behaviour_refs = {
            ProjectStatus.LOADING: self._load_existing_project,
            ProjectStatus.NEW: self._create_new_project
        }
        _behaviour_refs[project_status]()

        self._build_translated_component_mappings()

    def _window_update(self):
        project_title = "Undefined"
        this_project: Project = self.options.find_by_id("CurrentProject")
        if this_project:
            project_title = this_project.name
        self.setWindowTitle("EtymTree - Project Overview - (" + project_title + ")")

        self._tree_overview_update(self.current_lexicon)
        self._word_details_table_update()
        self._changehistory_table_update()

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
        self.options.set_option_to(
            "CurrentChangeHistory",
            loaded_project.find_changehistory_by_id(loaded_project.list_lexicons()[0].uuid))

    @property
    def current_lexicon(self) -> Lexicon:
        """The currently active Lexicon in the Window"""
        return self.options.find_by_id("CurrentLexicon")

    @property
    def current_changehistory(self) -> LexiconChangeHistory:
        """The change history attached to the active Lexicon"""
        return self.options.find_by_id("CurrentChangeHistory")
