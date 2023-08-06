import pytest
import os
import re
import json
from renamerename.executor.app import run, parse_args


class TestApp:

    @pytest.fixture
    def dir_files(self):
        return set(['wintercourse_doc.tar.gz', 'img.jpeg',
                    'summercourse_doc.tar.gz', 'icon.png',
                    'fallcourse_doc.tar.gz', 'file.py',
                    'script.sh', '.gitignore'])

    def test_basic_actions(self, dir_files, tmp_path):
        # create files in dir
        for file in dir_files:
            with open(tmp_path / file, 'w') as f:
                f.write("content...")

        # create some unuseful dir
        os.makedirs(tmp_path / "dir1")
        with open(tmp_path / "dir1/something.txt", 'w') as f:
            f.write("something_else")

        # check that files are created
        all_items = dir_files.union(set(["dir1"]))
        assert set(os.listdir(tmp_path)) == all_items
        assert set(os.listdir(tmp_path / "dir1")) == set(['something.txt'])

        # run renaming
        cli = f"--dir={tmp_path} --filter=*.tar.gz --prefix=foo_ --suffix=_bar --change-extension=.zip --save-renaming".split(" ")
        args = parse_args(args=cli)
        res = run(args=args)
        assert res == 0

        expected_files = set([
            'foo_wintercourse_doc_bar.zip', 'img.jpeg',
            'foo_summercourse_doc_bar.zip', 'icon.png',
            'foo_fallcourse_doc_bar.zip', 'file.py',
            'script.sh', '.gitignore'
        ])

        expected_items = set(['dir1'])
        expected_items.update(expected_files)

        current_dir = set(os.listdir(tmp_path))
        # check that new filenames were added
        assert all([file in current_dir for file in expected_items])

        # check that the new filenames replace the old ones
        assert len(current_dir - expected_items) == 1  # the missing file is the renaming JSON file

        # check that the renaming JSON file is valid
        renaming_file = list(current_dir - expected_items)[0]
        assert re.fullmatch(re.compile(r"renaming_\d{8}_\d{6}.json"), renaming_file) is not None
        with open(tmp_path / renaming_file, 'r') as f:
            renaming_content = json.loads(f.read())

        assert renaming_content == {
            "wintercourse_doc.tar.gz": "foo_wintercourse_doc_bar.zip",
            "summercourse_doc.tar.gz": "foo_summercourse_doc_bar.zip",
            "fallcourse_doc.tar.gz": "foo_fallcourse_doc_bar.zip"
        }

        # check if all files retain their contents
        for file in expected_files:
            with open(tmp_path / file, 'r') as f:
                assert f.read() == "content..."

        with open(tmp_path / "dir1/something.txt", 'r') as f:
            assert f.read() == "something_else"
