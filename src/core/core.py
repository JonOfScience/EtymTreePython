"""Location for project-wide values and interfaces."""
from typing import Callable, Sequence
import os
import uuid
import logging
from enum import Enum, auto
from abc import ABCMeta, abstractmethod
from PyQt5.QtCore import QObject, pyqtSignal, QEvent


# Build this programmatically from files rather than hard coding and then adding items to io_service
# import enum
# DynamicEnum = enum.Enum('DynamicEnum', {'foo':42, 'bar':24})
class DataFormat(Enum):
    """Registered serialisation formats."""
    JSON = "json"


class ProjectStatus(str, Enum):
    """Registered status for active projects."""
    EMPTY = "empty"
    LOADING = "loading"
    MODIFIED = "modified"
    NEW = "new"
    SAVED = "saved"

class WordField(Enum):
    """External field mapping contract for Word fields"""
    TRANSLATEDWORD = auto()
    TRANSLATEDCOMPONENTS = auto()
    INLANGUAGECOMPONENTS = auto()
    ETYMOLOGICALSYMBOLOGY = auto()
    COMPILEDSYMBOLOGY = auto()
    SYMBOLMAPPING = auto()
    SYMBOLSELECTION = auto()
    SYMBOLPATTERNSELECTED = auto()
    RULESAPPLIED = auto()
    INLANGUAGEWORD = auto()
    VERSIONHISTORY = auto()
    HASBEENMODIFIED = auto()
    HASMODIFIEDANCESTOR = auto()
    RESOLVEDHISTORYITEMS = auto()

def new_garbage_string():
    """Helper method to produce a random string from uuid"""
    return ''.join([x for x in uuid.uuid4().hex if x.isalpha()])


class SerialiserInterface(metaclass=ABCMeta):
    """Interface for all serialisers for IO operations"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'serialise') and
                callable(subclass.serialise))

    @staticmethod
    @abstractmethod
    def serialise(object_to_serialise):
        """Serialise object data into specified format"""
        raise NotImplementedError


class DeserialiserInterface(metaclass=ABCMeta):
    """Interface for all deserialisers for IO operations"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'deserialise') and
                callable(subclass.deserialise))

    @staticmethod
    @abstractmethod
    def deserialise(string_to_deserialise):
        """Deserialise object from specified format"""
        raise NotImplementedError


def double_clickable(widget):
    """Helper method to add an event filter for Double Click"""
    class Filter(QObject):
        """Permits double click on an element that doesn't have a Double Click slot"""
        clicked = pyqtSignal()

        # pylint: disable-next=invalid-name
        def eventFilter(self,
                        obj: 'QObject',
                        event: 'QEvent') -> bool:
            """Catch Dbl-Click if triggered within the bounds of the element"""
            if obj == widget:
                if event.type() == QEvent.MouseButtonDblClick:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False
    dbl_filter = Filter(widget)
    widget.installEventFilter(dbl_filter)
    return dbl_filter.clicked


def id_project_files_in(file_location: str, validator: Callable) -> Sequence:
    """Collects data about Projects stored in the specified location."""
    logger = logging.getLogger('etym_logger')
    proj_files_found = {}
    for path, dirnames, filenames in os.walk(file_location):
        logger.debug("Path     : %s", path)
        logger.debug("Dirnames : %s", dirnames)
        logger.debug("Filenames: %s", filenames)
        proj_files_found[path] = {}
        if dirnames:
            for dirname in dirnames:
                proj_files_found[path][dirname] = [x for x in filenames if validator(x)]
        else:
            proj_files_found[path][''] = [x for x in filenames if validator(x)]
    return proj_files_found
