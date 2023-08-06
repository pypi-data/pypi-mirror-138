import pytest
from renamerename.handlers.filetransformation import FileTransformation


class TestFileTransformation:

    @pytest.fixture
    def file_transformation_basic(self):
        return FileTransformation({
            'one.py': 'one.py',
            'two.txt': 'two.txt',
            'three.tar.gz': 'three.tar.gz'
        })

    @pytest.fixture
    def file_transformation(self):
        return FileTransformation({
            'one.py': 'foo_one.py',
            'two.txt': 'two_bar.txt',
            'three.tar.gz': 'three.zip',
        })

    @pytest.fixture
    def file_transformation_with_duplicates(self):
        return FileTransformation({
            'file.py': 'file',
            'file.txt': 'file',
            'three.tar.gz': 'three.zip',
            'three': 'three.zip',
            'something': 'foo',
        })

    def test_init(self, file_transformation_basic):
        assert file_transformation_basic.transformations == {
            'one.py': 'one.py',
            'two.txt': 'two.txt',
            'three.tar.gz': 'three.tar.gz'
        }

    def test_init_invalid_arg(self):
        with pytest.raises(TypeError):
            FileTransformation(object)

    def test_from_list(self, file_transformation_basic):
        names = ['one.py', 'two.txt', 'three.tar.gz']
        assert file_transformation_basic.transformations == FileTransformation.from_list(names).transformations

    def test_get_set_item(self, file_transformation_basic):
        assert file_transformation_basic['one.py'] == 'one.py'
        file_transformation_basic['one.py'] = 'something_else'
        assert file_transformation_basic['one.py'] == 'something_else'

    def test_str_output(self, file_transformation):
        expected_str = "one.py ----> foo_one.py\n"\
                       "two.txt ----> two_bar.txt\n"\
                       "three.tar.gz ----> three.zip\n"
        assert str(file_transformation) == expected_str

    def test_get_reversed(self, file_transformation):
        assert file_transformation.get_reversed() == {
            'foo_one.py': ['one.py'],
            'two_bar.txt': ['two.txt'],
            'three.zip': ['three.tar.gz']
        }

    def test_get_reversed_with_duplicates(self, file_transformation_with_duplicates):
        assert file_transformation_with_duplicates.get_reversed() == {
            'file': ['file.py', 'file.txt'],
            'three.zip': ['three.tar.gz', 'three'],
            'foo': ['something']
        }

    def test_has_no_duplicates(self, file_transformation):
        assert not file_transformation.has_duplicates()

    def test_has_duplicates(self, file_transformation_with_duplicates):
        assert file_transformation_with_duplicates.has_duplicates()

    def test_repr(self, file_transformation_basic):
        content = r"FileTransformation({'one.py': 'one.py', 'two.txt': 'two.txt', 'three.tar.gz': 'three.tar.gz'})"
        assert repr(file_transformation_basic) == content

    def test_delitem(self, file_transformation_basic):
        del file_transformation_basic['one.py']
        assert file_transformation_basic.transformations == {
            'two.txt': 'two.txt',
            'three.tar.gz': 'three.tar.gz'
        }
