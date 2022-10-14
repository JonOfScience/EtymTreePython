"""Word details GUI module"""
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QTableView,
    QVBoxLayout
)
from PyQt5.QtGui import QStandardItemModel
from ui.interfaces import Controls


class DisplayAndEditElement:
    """Generic paired elements for labelling and displaying a data element"""
    def __init__(self,
                 label_text: str,
                 object_name: str,
                 element_class,
                 element_set_method) -> None:
        self._layout = QHBoxLayout()
        self._label = QLabel(text=label_text)
        self._layout.addWidget(self._label)
        self._data: QObject = element_class()
        self._data.setObjectName(object_name)
        element_set_method(self._data, "No Word Selected")
        self._layout.addWidget(self._data)

    @property
    def layout(self):
        """The filled QHBoxLayout for this pair of elements"""
        return self._layout

    @property
    def control(self):
        """The reference to the data field"""
        return self._data


class WordDetailsOld:
    """Container class for display and editing of Word fields"""
    def __init__(self) -> None:
        self.controls = Controls()

        self.details_group = QGroupBox("Word Details")
        self.details_group.setMinimumWidth(500)
        details_layout = QVBoxLayout()

        word_label = DisplayAndEditElement(
            "Translated Word",
            "translated_word",
            QPlainTextEdit,
            QPlainTextEdit.setPlaceholderText)
        details_layout.addLayout(word_label.layout)
        self.controls.register_control(word_label.control)

        word_components = DisplayAndEditElement(
            "Translated Components",
            "translated_components",
            QPlainTextEdit,
            QPlainTextEdit.setPlaceholderText)
        details_layout.addLayout(word_components.layout)
        self.controls.register_control(word_components.control)

        in_language_components = DisplayAndEditElement(
            "In Language Components",
            "in_language_components",
            QPlainTextEdit,
            QPlainTextEdit.setPlaceholderText)
        details_layout.addLayout(in_language_components.layout)
        self.controls.register_control(in_language_components.control)

        etymological_symbology = DisplayAndEditElement(
            "Etymological Symbology",
            "etymological_symbology",
            QPlainTextEdit,
            QPlainTextEdit.setPlaceholderText)
        details_layout.addLayout(etymological_symbology.layout)
        self.controls.register_control(etymological_symbology.control)

        compiled_symbology = DisplayAndEditElement(
            "Compiled Symbology",
            "compiled_symbology",
            QPlainTextEdit,
            QPlainTextEdit.setPlaceholderText)
        details_layout.addLayout(compiled_symbology.layout)
        self.controls.register_control(compiled_symbology.control)

        symbol_mapping = DisplayAndEditElement(
            "Symbol Mapping",
            "symbol_mapping",
            QPlainTextEdit,
            QPlainTextEdit.setPlaceholderText)
        details_layout.addLayout(symbol_mapping.layout)
        self.controls.register_control(symbol_mapping.control)

        symbol_selection = DisplayAndEditElement(
            "Symbol Selection",
            "symbol_selection",
            QPlainTextEdit,
            QPlainTextEdit.setPlaceholderText)
        details_layout.addLayout(symbol_selection.layout)
        self.controls.register_control(symbol_selection.control)

        symbol_pattern_selected = DisplayAndEditElement(
            "Symbol Pattern Selected",
            "symbol_pattern_selected",
            QPlainTextEdit,
            QPlainTextEdit.setPlaceholderText)
        details_layout.addLayout(symbol_pattern_selected.layout)
        self.controls.register_control(symbol_pattern_selected.control)

        # rules_applied: Mapping[Enum, str] = None
        # in_language_word: str = None

        self.details_group.setLayout(details_layout)

    def get_layout(self):
        """Returns layout"""
        return self.details_group

    def get_controls(self):
        """Returns registered controls"""
        return self.controls


class WordDetails:
    """Container class for display and editing of Word fields"""
    def __init__(self) -> None:
        self.controls = Controls()

        self.details_group = QGroupBox("Word Details")
        self.details_group.setMinimumWidth(500)
        details_layout = QVBoxLayout()
        details_table = QTableView()
        details_table.setObjectName("WordDetailsTable")
        details_model = QStandardItemModel()
        details_table.setModel(details_model)
        details_layout.addWidget(details_table)
        self.controls.register_control(details_table)
        self.details_group.setLayout(details_layout)

    def get_layout(self):
        """Returns layout"""
        return self.details_group

    def get_controls(self):
        """Returns registered controls"""
        return self.controls
