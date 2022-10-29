"""Test Core functionality available to all parts of the application"""
from core.core import id_project_files_in


def project_filename_validator(filename: str):
    return filename.startswith("PROJ-")


class TestGivenExtantProjectFiles:
    def test_an_empty_directory_produces_an_empty_list(self):
        """Placeholder: State Test - Brittle"""
        assert not id_project_files_in("tests/nodata/", project_filename_validator)

    def test_extant_files_will_be_returned(self):
        """Placeholder: State Test"""
        assert id_project_files_in("data/", project_filename_validator)
