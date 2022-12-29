"""Tests for UI associated interfaces and core functionality"""
import pytest
from PyQt5.QtCore import QObject
from ui.interfaces import Controls


class TestANewControlsInstance():
    """A new instance if the Controls() class should be able to..."""
    def test_can_be_constructed(self):
        """Controls() should accept a parameterless constructor"""
        assert Controls()

    def test_will_accept_a_new_control(self):
        """Existing named instances can be registered"""
        empty_controls = Controls()
        new_obj = QObject()
        new_obj.setObjectName("NotAnObject")
        empty_controls.register_control(new_obj)

    def test_will_throw_if_registering_a_nameless_control(self):
        """Controls are registered using <QObject>.ObjectName. Without this it should throw."""
        empty_controls = Controls()
        new_obj = QObject()
        with pytest.raises(Exception) as e_info:
            empty_controls.register_control(new_obj)
        print(e_info.type)
        assert e_info.type == ValueError


class TestAFilledControlsInstance():
    """An instance of the Controls class with items should be able to..."""
    def test_lists_all_registered_controls(self):
        """Return as a List without named identifiers"""
        win_controls = Controls()
        new_obj = QObject()
        new_obj.setObjectName("TestObject")
        win_controls.register_control(new_obj)
        assert win_controls.controls_registered() == [new_obj]

    def test_locates_the_correct_control_by_id(self):
        """Controls are registered using ObjectName. Element can be retrieved from this"""
        win_controls = Controls()
        new_obj = QObject()
        new_obj.setObjectName("TestObject")
        win_controls.register_control(new_obj)
        assert win_controls.control_from_id("TestObject") == new_obj

    def test_merges_in_elements_from_another_controls_class(self):
        """A Controls class should be able to register elements from another instance"""
        main_win_controls = Controls()
        sub_win_controls = Controls()
        sub_obj = QObject()
        sub_obj.setObjectName("TestObject")
        sub_win_controls.register_control(sub_obj)
        main_win_controls.merge_controls_from(sub_win_controls)
        assert main_win_controls.control_from_id("TestObject") == sub_obj
