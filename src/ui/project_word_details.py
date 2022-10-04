"""Word details GUI module"""
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QVBoxLayout
)
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


class WordDetails:
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
            "translated_Components",
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

        self.details_group.setLayout(details_layout)

    def get_layout(self):
        """Returns layout"""
        return self.details_group

    def get_controls(self):
        """Returns registered controls"""
        return self.controls
