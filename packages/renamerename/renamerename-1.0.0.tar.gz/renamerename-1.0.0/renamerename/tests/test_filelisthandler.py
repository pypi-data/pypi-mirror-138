import pytest
from renamerename.handlers.handlers import FileListHandler, FilenameHandler
from renamerename.handlers.filetransformation import FileTransformation


class TestFileListHandler:

    @pytest.fixture
    def filelist_handler_basic(self):
        names = ['file.txt', 'file.py', 'archive.tar.gz']
        return FileListHandler(names)

    @pytest.fixture
    def filelist_handler(self):
        names = ['aaa.png', 'bbb.txt', 'ccc.tar.gz', 'ddd.png',
                 'eee.txt', 'fff', 'ggg', 'hhh.png', 'iii.tar.zip', 'jjj.pnj']
        handler = FileListHandler(names)
        handler.filter_names("*.png")
        return handler

    def test_basic_init(self, filelist_handler_basic):
        assert filelist_handler_basic.names == ['file.txt', 'file.py', 'archive.tar.gz']
        assert filelist_handler_basic.filenames == ['file.txt', 'file.py', 'archive.tar.gz']
        assert type(filelist_handler_basic.filenamehandler) == FilenameHandler
        assert isinstance(filelist_handler_basic.filetransformations, FileTransformation)

    def test_filter_by_none(self, filelist_handler_basic):
        filelist_handler_basic.filter_names(filter=None)
        assert filelist_handler_basic.filenames == ['file.txt', 'file.py', 'archive.tar.gz']

    def test_filter_names(self, filelist_handler_basic):
        filelist_handler_basic.filter_names(filter="file*")
        assert filelist_handler_basic.filenames == ['file.txt', 'file.py']

    def test_filtered_names(self, filelist_handler):
        assert filelist_handler.filenames == ['aaa.png', 'ddd.png', 'hhh.png']

    def test_add_prefix(self, filelist_handler):
        filelist_handler.add_prefix("foo_")
        assert filelist_handler.filetransformations == {
            'aaa.png': 'foo_aaa.png',
            'ddd.png': 'foo_ddd.png',
            'hhh.png': 'foo_hhh.png'
        }

    def test_add_suffix(self, filelist_handler):
        filelist_handler.add_suffix("_bar")
        assert filelist_handler.filetransformations == {
            'aaa.png': 'aaa_bar.png',
            'ddd.png': 'ddd_bar.png',
            'hhh.png': 'hhh_bar.png'
        }

    def test_change_extension(self, filelist_handler):
        filelist_handler.change_extension(".jpeg")
        assert filelist_handler.filetransformations == {
            'aaa.png': 'aaa.jpeg',
            'ddd.png': 'ddd.jpeg',
            'hhh.png': 'hhh.jpeg'
        }

    def test_add_numbering(self, filelist_handler):
        filelist_handler.add_numbering("me")
        assert filelist_handler.filetransformations == {
            'aaa.png': 'me0.png',
            'ddd.png': 'me1.png',
            'hhh.png': 'me2.png'
        }

    def test_multiple_actions(self, filelist_handler):
        filelist_handler.add_numbering("img")
        filelist_handler.add_prefix("pre_")
        filelist_handler.change_extension(".jpeg")
        filelist_handler.add_suffix("_post")
        assert filelist_handler.filetransformations == {
            'aaa.png': 'pre_img0_post.jpeg',
            'ddd.png': 'pre_img1_post.jpeg',
            'hhh.png': 'pre_img2_post.jpeg'
        }
