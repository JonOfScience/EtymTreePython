"""Common UI interfaces"""
from __future__ import annotations
from typing import Protocol
from PyQt5.QtCore import QObject
from configuration.settings import Settings


class EtymWindow(Protocol):
    """Base window protocol class identifying common properties"""
    options: Settings


class Controls:
    """Container for instanced controls in a window"""
    def __init__(self) -> None:
        self._control_library = {}

    def register_control(self, control_object: QObject):
        """Add an existing QObject instance to the list of existing controls"""
        if not control_object.objectName():
            raise ValueError("ObjectName cannot be empty.")
        self._control_library[control_object.objectName()] = control_object

    def merge_controls_from(self, control_container: Controls):
        """Incorporate controls in another Controls instance into this one"""
        for reg_control in control_container.controls_registered():
            self.register_control(reg_control)

    def controls_registered(self):
        """Return a List containing references to all registered controls"""
        return [control for (_, control) in self._control_library.items()]

    def control_from_id(self, object_name: str):
        """Return a registered instance using its name"""
        return self._control_library.get(object_name)
