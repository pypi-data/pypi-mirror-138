import pytest
from renamerename.handlers.handlers import FilenameHandler


class TestFilenameHandler:

    @pytest.fixture
    def GetFilenameHandler(self):
        return FilenameHandler

    def test_add_prefix_raw(self, GetFilenameHandler):
        assert GetFilenameHandler.add_prefix("file", "sub") == "subfile"

    def test_add_prefix_ext(self, GetFilenameHandler):
        assert GetFilenameHandler.add_prefix("file.txt", "sub") == "subfile.txt"

    def test_add_prefix_multiple_ext(self, GetFilenameHandler):
        assert GetFilenameHandler.add_prefix("file.tar.gz", "sub") == "subfile.tar.gz"

    def test_add_prefix_empty(self, GetFilenameHandler):
        assert GetFilenameHandler.add_prefix("file.py", "") == "file.py"

    def test_add_suffix_raw(self, GetFilenameHandler):
        assert GetFilenameHandler.add_suffix("file", "_final") == "file_final"

    def test_add_suffix_ext(self, GetFilenameHandler):
        assert GetFilenameHandler.add_suffix("file.txt", "_final") == "file_final.txt"

    def test_add_suffix_multiple_ext(self, GetFilenameHandler):
        assert GetFilenameHandler.add_suffix("file.tar.gz", "_final") == "file_final.tar.gz"

    def test_add_suffix_empty(self, GetFilenameHandler):
        assert GetFilenameHandler.add_suffix("file.py", "") == "file.py"

    def test_change_extension_raw(self, GetFilenameHandler):
        assert GetFilenameHandler.change_extension("file", ".txt") == "file.txt"

    def test_change_extension_ext(self, GetFilenameHandler):
        assert GetFilenameHandler.change_extension("file.txt", ".md") == "file.md"

    def test_change_extension_multiple_ext(self, GetFilenameHandler):
        assert GetFilenameHandler.change_extension("file.tar.gz", ".zip") == "file.zip"

    def test_change_extension_without_dot(self, GetFilenameHandler):
        assert GetFilenameHandler.change_extension("file.tar.gz", "zip") == "file.zip"

    def test_remove_extension(self, GetFilenameHandler):
        assert GetFilenameHandler.change_extension("file.tar.gz", "") == "file"

    def test_change_name_raw(self, GetFilenameHandler):
        assert GetFilenameHandler.change_name("file", "archive") == "archive"

    def test_change_name_ext(self, GetFilenameHandler):
        assert GetFilenameHandler.change_name("file.py", "archive") == "archive.py"

    def test_change_name_multiple_ext(self, GetFilenameHandler):
        assert GetFilenameHandler.change_name("file.tar.gz", "archive") == "archive.tar.gz"

    def test_get_components_raw(self, GetFilenameHandler):
        assert GetFilenameHandler.get_components("file") == ("file", "")

    def test_get_components_ext(self, GetFilenameHandler):
        assert GetFilenameHandler.get_components("file.txt") == ("file", ".txt")

    def test_get_components_multiple_ext(self, GetFilenameHandler):
        assert GetFilenameHandler.get_components("file.tar.gz") == ("file", ".tar.gz")
