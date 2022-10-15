"""Location for project-wide values and interfaces."""
import uuid
from enum import Enum
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
    MODIFIED = "modified"
    NEW = "new"
    SAVED = "saved"


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
