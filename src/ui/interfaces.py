"""Common UI interfaces"""
from typing import Protocol
from configuration.settings import Settings


class EtymWindow(Protocol):
    """Base window protocol class identifying common properties"""
    options: Settings
