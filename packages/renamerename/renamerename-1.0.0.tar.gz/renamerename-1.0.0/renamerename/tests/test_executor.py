import pytest
from pathlib import Path
from pytest_mock import mocker
from renamerename.executor.executor import RenameExecutor, DuplicateFilenamesError
from renamerename.handlers.filetransformation import FileTransformation


class RenameMock:
    def __init__(self):
        self.dirfiles = set(['aaa', 'bbb', 'ccc.py', 'ddd.tar.gz', 'eee.txt', 'fff', 'ggg'])

    def __call__(self, src, dst):
        self.dirfiles.remove(Path(src).name)
        self.dirfiles.add(Path(dst).name)

    def exists(self, name):
        return Path(name).name in self.dirfiles


class TestRenameExecutor:

    @pytest.fixture
    def rename_executor(self):
        return RenameExecutor(".")

    @pytest.fixture
    def rename_executor_with_saved_renaming(self):
        return RenameExecutor(".", save_renaming=True)

    @pytest.fixture
    def get_filenames(self):
        return ['aaa', 'bbb', 'ccc.py', 'ddd.tar.gz', 'eee.txt']

    @pytest.fixture
    def get_names(self, get_filenames):
        return get_filenames + ['fff', 'ggg']

    # TODO: mock FileTransformation
    def test_adjust_duplicates_none(self, rename_executor, get_names):
        filetransformation = FileTransformation({
            'aaa': 'foo_aaa',
            'bbb': 'foo_bbb',
            'ccc.py': 'foo_ccc.py',
            'ddd.tar.gz': 'foo_ddd.tar.gz',
            'eee.txt': 'foo_eee.txt',
        })
        assert not filetransformation.has_duplicates()
        actual_transformation = rename_executor.adjust_duplicates(get_names, filetransformation)
        assert actual_transformation == filetransformation
        assert not actual_transformation.has_duplicates()

    def test_adjust_duplicates_one(self, rename_executor, get_names):
        # duplicates are exclusively in filetransformation
        filetransformation = FileTransformation({
            'aaa': 'dup',  # duplicate
            'bbb': 'foo_bbb',
            'ccc.py': 'foo_ccc.py',
            'ddd.tar.gz': 'foo_ddd.tar.gz',
            'eee.txt': 'dup'  # duplicate
        })
        assert filetransformation.has_duplicates()
        actual_transformation = rename_executor.adjust_duplicates(get_names, filetransformation)
        assert actual_transformation == {
            'aaa': 'dup (1)',
            'bbb': 'foo_bbb',
            'ccc.py': 'foo_ccc.py',
            'ddd.tar.gz': 'foo_ddd.tar.gz',
            'eee.txt': 'dup (2)'
        }

    def test_adjust_duplicates_two(self, rename_executor, get_names):
        # duplicates reside in names and filetransformation
        filetransformation = FileTransformation({
            'aaa': 'fff',  # duplicate with entry in names
            'bbb': 'foo_bbb',
            'ccc.py': 'foo_ccc.py',
            'ddd.tar.gz': 'foo_ddd.tar.gz',
            'eee.txt': 'foo_eee.txt',
        })
        assert not filetransformation.has_duplicates()
        actual_transformation = rename_executor.adjust_duplicates(get_names, filetransformation)
        assert actual_transformation == {
            'aaa': 'fff (1)',
            'bbb': 'foo_bbb',
            'ccc.py': 'foo_ccc.py',
            'ddd.tar.gz': 'foo_ddd.tar.gz',
            'eee.txt': 'foo_eee.txt'
        }

    def test_execute(self, rename_executor, mocker):
        mocked_filesys = mocker.patch('os.rename', new_callable=RenameMock)
        mocker.patch('os.path.exists', mocked_filesys.exists)

        filetransformation = FileTransformation({
            'aaa': 'fff',  # duplicate with file in filesystem
            'bbb': 'foo_bbb',
            'ccc.py': 'foo_ccc.py',
            'ddd.tar.gz': 'foo_ddd',  # duplicate with below
            'eee.txt': 'foo_ddd'  # duplicate with above
        })
        rename_executor.execute(mocked_filesys.dirfiles, filetransformation)
        assert mocked_filesys.dirfiles == set(['fff (1)', 'foo_bbb', 'foo_ccc.py', 'foo_ddd (1)', 'foo_ddd (2)', 'fff', 'ggg'])
        assert rename_executor.actual_transformation == filetransformation
        mocker.resetall()

    def test_save_renaming(self, rename_executor_with_saved_renaming, get_names, mocker):
        mocked_filesys = mocker.patch('os.rename', new_callable=RenameMock)
        mocker.patch('os.path.exists', mocked_filesys.exists)
        encoder_mock = mocker.patch('renamerename.executor.encoder_decoder.TransformationEncoder.save_transformation_to_json')

        filetransformation = FileTransformation({
            'aaa': 'fff',  # duplicate with file in filesystem
            'bbb': 'foo_bbb',
            'ccc.py': 'foo_ccc.py',
            'ddd.tar.gz': 'foo_ddd',  # duplicate with below
            'eee.txt': 'foo_ddd'  # duplicate with above
        })
        rename_executor_with_saved_renaming.execute(get_names, filetransformation)
        encoder_mock.assert_called_once_with(rename_executor_with_saved_renaming.directory,
                                             rename_executor_with_saved_renaming.actual_transformation)
        assert mocked_filesys.dirfiles == set(['fff (1)', 'foo_bbb', 'foo_ccc.py', 'foo_ddd (1)', 'foo_ddd (2)', 'fff', 'ggg'])
        mocker.resetall()

    def test_save_renaming_with_duplicates(self, rename_executor_with_saved_renaming, get_names, get_filenames, mocker):
        mocked_filesys = mocker.patch('os.rename', new_callable=RenameMock)
        mocker.patch('os.path.exists', mocked_filesys.exists)
        encoder_mock = mocker.patch('renamerename.executor.encoder_decoder.TransformationEncoder.save_transformation_to_json')

        filetransformation = FileTransformation.from_list(get_filenames)
        filetransformation['aaa'] = '111'

        with pytest.raises(FileExistsError):
            rename_executor_with_saved_renaming.execute(get_names, filetransformation)

        assert rename_executor_with_saved_renaming.actual_transformation == {'aaa': '111'}
        encoder_mock.assert_called_once_with(rename_executor_with_saved_renaming.directory,
                                             rename_executor_with_saved_renaming.actual_transformation)
        assert mocked_filesys.dirfiles == set(['111', 'bbb', 'ccc.py', 'ddd.tar.gz', 'eee.txt', 'fff', 'ggg'])

    def test_execute_with_existing_file(self, rename_executor, get_filenames, mocker):
        mocked_filesys = mocker.patch('os.rename', new_callable=RenameMock)
        mocker.patch('os.path.exists', mocked_filesys.exists)
        filetransformation = FileTransformation.from_list(get_filenames)
        filetransformation['aaa'] = '111'

        with pytest.raises(FileExistsError):
            rename_executor.execute(mocked_filesys.dirfiles, filetransformation)

        assert rename_executor.actual_transformation == {'aaa': '111'}
        mocker.resetall()

    def test_execute_with_all_existing_targets(self, rename_executor, get_filenames, mocker):
        mocked_filesys = mocker.patch('os.rename', new_callable=RenameMock)
        mocker.patch('os.path.exists', mocked_filesys.exists)
        filetransformation = FileTransformation.from_list(get_filenames)

        with pytest.raises(FileExistsError):
            rename_executor.execute(mocked_filesys.dirfiles, filetransformation)

        assert len(rename_executor.actual_transformation) == 0

    def test_execute_with_non_existing_sources(self, rename_executor, mocker):
        mocked_filesys = mocker.patch('os.rename', new_callable=RenameMock)
        mocker.patch('os.path.exists', mocked_filesys.exists)
        filetransformation = FileTransformation({
            "nonexisting": "foo_nonexisting",
            "something_else.txt": "something_else_bar.txt"
        })

        with pytest.raises(FileNotFoundError):
            rename_executor.execute(mocked_filesys.dirfiles, filetransformation)

        assert len(rename_executor.actual_transformation) == 0
        mocker.resetall()

    def test_execute_from_file(self, rename_executor, get_names, mocker):
        decode_mock = mocker.patch('renamerename.executor.encoder_decoder.TransformationDecoder.decode_from_json_file')
        filetransformation = FileTransformation({
            'aaa': 'foo_aaa',
            'bbb': 'bbb_bar'
        })
        decode_mock.return_value = filetransformation
        import renamerename
        execute_mocker = mocker.patch.object(renamerename.executor.executor.RenameExecutor, 'execute')
        filepath = "dir/file.json"
        rename_executor.execute_from_file(get_names, filepath)
        decode_mock.assert_called_once_with(filepath)
        execute_mocker.assert_called_once_with(get_names, filetransformation)
        mocker.resetall()

    def test_undo_from_file(self, rename_executor, get_names, mocker):
        decode_mock = mocker.patch('renamerename.executor.encoder_decoder.TransformationDecoder.decode_from_json_file')
        filetransformation = FileTransformation({
            'aaa': 'foo_aaa',
            'bbb': 'bbb_bar'
        })
        decode_mock.return_value = filetransformation
        import renamerename
        execute_mock = mocker.patch.object(renamerename.executor.executor.RenameExecutor, 'execute')
        filepath = "dir/file.json"
        rename_executor.execute_from_file(get_names, filepath, undo=True)
        decode_mock.assert_called_once_with(filepath)
        reversed_transformation = FileTransformation({
            'foo_aaa': 'aaa',
            'bbb_bar': 'bbb'
        })
        execute_mock.assert_called_once_with(get_names, reversed_transformation)
        mocker.resetall()

    def test_undo_from_file_with_duplicates(self, rename_executor, get_names, mocker):
        decode_mock = mocker.patch('renamerename.executor.encoder_decoder.TransformationDecoder.decode_from_json_file')
        filetransformation = FileTransformation({
            'aaa': 'foo',
            'bbb': 'foo'
        })
        decode_mock.return_value = filetransformation
        import renamerename
        mocker.patch.object(renamerename.executor.executor.RenameExecutor, 'execute')
        filepath = "dir/file.json"
        with pytest.raises(DuplicateFilenamesError):
            rename_executor.execute_from_file(get_names, filepath, undo=True)

        decode_mock.assert_called_once_with(filepath)
        mocker.resetall()

    def test_display_output(self, rename_executor, get_names, mocker):
        filetransformation = FileTransformation({
            'aaa': 'foo_aaa',
            'bbb': 'foo_bbb',
            'ccc.py': 'foo_ccc.py',
            'ddd.tar.gz': 'foo_ddd.tar.gz',
            'eee.txt': 'foo_eee.txt',
        })
        import renamerename
        adjust_duplicates_mock = mocker.patch.object(renamerename.executor.executor.RenameExecutor, 'adjust_duplicates')
        adjust_duplicates_mock.return_value = filetransformation
        print_mocker = mocker.patch('builtins.print')
        rename_executor.display_output(get_names, filetransformation)
        adjust_duplicates_mock.assert_called_once_with(get_names, filetransformation)
        print_mocker.assert_called_once_with(filetransformation)
