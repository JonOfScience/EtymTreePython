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

    def test__generate_an_export_dto(self):
        """Ready for serialisation and storage"""
        new_item = ChangeHistoryItem("A test Item relating to a test change.")
        export_dto = new_item.data_for_export()
        assert export_dto["UId"] == new_item.uid
        assert export_dto["DescriptionOfChange"] == new_item.description
        assert export_dto["CreationTimeUTC"] == new_item.created_utc


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


class TestGivenANewLexiconChangeHistory:
    """Test operations on a new instance related to records and I/O"""
    def test__when_getting_all_items_then_provide_an_empty_list(self):
        """Should not be None, but Empty list"""
        empty_lch_items = LexiconChangeHistory().get_all_items()
        assert isinstance(empty_lch_items, list)
        assert not empty_lch_items

    def test__when_getting_export_data_then_provide_an_empty_list(self):
        """Should not be None, but Empty list"""
        empty_lch_export_data = LexiconChangeHistory().retrieve_export_data_for()
        assert isinstance(empty_lch_export_data, list)
        assert not empty_lch_export_data

    def test__a_new_item_can_be_added(self):
        """The number of items registered should be 1 more after than before"""
        new_lch = LexiconChangeHistory()
        items_before = len(new_lch.get_all_items())
        new_item = ChangeHistoryItem("A test item to be added.")
        new_lch.add_item(new_item)
        assert len(new_lch.get_all_items()) == items_before + 1


class TestGivenALexiconChangeHistoryWithOneItem:
    """Test operations on a LexiconChangeHistory related to records and I/O"""
    def test__when_getting_all_items_then_provide_a_list_with_one_item(self):
        """A list containing the one entry"""
        new_item = ChangeHistoryItem("A test item.")
        lch = LexiconChangeHistory()
        lch.add_item(new_item)
        assert lch.get_all_items() == [new_item]

    def test__when_getting_export_data_then_provide_a_list_with_data_matching_the_item(self):
        """A list containing the dictionary represantation of the one entry"""
        new_item = ChangeHistoryItem("A test item.")
        lch = LexiconChangeHistory()
        export_dto = new_item.data_for_export()
        lch.add_item(new_item)
        assert lch.retrieve_export_data_for() == [export_dto]
