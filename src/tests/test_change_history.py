"""Tests for a Lexicon level Change History Items and repository."""
import pytest
from core.change_history_item import ChangeHistoryItem
from core.change_history import LexiconChangeHistory


class TestAChangeHistoryItemShould:
    """Test operations related to instantiation."""
    def test__not_be_able_to_be_instantiated_without_a_description(self):
        """An item with no description is not a valid item."""
        with pytest.raises(Exception) as e_info:
            ChangeHistoryItem() #pylint: disable=no-value-for-parameter
        assert e_info.type == TypeError

    def test__have_an_id(self):
        """Unique ids are the way Items are referenced"""
        new_item = ChangeHistoryItem("A test Item relating to a test change.")
        assert new_item.uid

    def test__have_a_timestamp_from_when_it_was_created(self):
        """Changes are listed in timestamp order for resolution"""
        new_item = ChangeHistoryItem("A test Item relating to a test change.")
        assert new_item.created_utc


class TestGivenANewChangeHistoryItem:
    """Test operations on a new instance relating to simple data manipulation"""
    def test__when_set_description_to_is_called__then_the_description_is_changed(self):
        """Description is the only field that is modified by the user."""
        new_item = ChangeHistoryItem("DescriptionA")
        new_item.set_description_to("DescriptionB")
        assert new_item.description == "DescriptionB"


class TestALexiconChangeHistoryShould:
    """Test operations related to instantiation."""
    def test__instantiate_blank(self):
        """A blank Change History is a valid state."""
        assert LexiconChangeHistory()
