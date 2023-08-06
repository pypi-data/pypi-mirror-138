"""Utility classes for executing renaming on filesystem."""

import itertools
import logging
import os
from typing import List, Optional
from renamerename.handlers.handlers import FilenameHandler, FileTransformation
from renamerename.executor.encoder_decoder import TransformationEncoder, TransformationDecoder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


class DuplicateFilenamesError(RuntimeError):
    """RuntimeError wrapper for loaded mapping with common values"""
    pass


class RenameExecutor:
    """Renaming executor on the filesystem."""

    def __init__(self, directory: str, save_renaming=False):
        """Constructor

        :param str directory: directory containing the files to be renamed
        :param save_renaming: save source and target filenames to disk , defaults to False
        :type save_renaming: bool, optional
        """
        self.directory = directory
        self.is_renaming_saved = save_renaming
        self.actual_transformation = None

    def execute(self, names: List[str], filetransformation: FileTransformation):
        """Rename files on filesystem based on provided specification.

        :param List[str] names: list of all filenames in :py:attr:`~directory`
        :param FileTransformation filetransformation: FileTransformation instance
        :raises FileNotFoundError: source filename does not exist
        :raises FileExistsError: target filename already exists
        """
        filetransformation = self.adjust_duplicates(names, filetransformation)

        for i, (k, v) in enumerate(filetransformation.items()):
            source_file_path = os.path.join(self.directory, k)
            target_file_path = os.path.join(self.directory, v)
            source_filename_exists = os.path.exists(source_file_path)
            target_filename_exists = os.path.exists(target_file_path)
            if not source_filename_exists or target_filename_exists:
                self.actual_transformation = FileTransformation(dict(itertools.islice(filetransformation.items(), i)))
                if self.is_renaming_saved:
                    TransformationEncoder.save_transformation_to_json(self.directory, self.actual_transformation)
                if not source_filename_exists:
                    raise FileNotFoundError(f"The source filename {source_file_path} does not exist.")
                if target_filename_exists:
                    raise FileExistsError(f"The target filename {target_file_path} already exists.")
            else:
                os.rename(source_file_path, target_file_path)

        self.actual_transformation = filetransformation
        if self.is_renaming_saved:
            TransformationEncoder.save_transformation_to_json(self.directory, self.actual_transformation)

    def display_output(self, names: List[str], filetransformation: FileTransformation):
        """Display output of renaming to STDOUT without actual execution.

        :param List[str] names: list of all filenames in :py:attr:`~directory`
        :param FileTransformation filetransformation: FileTransformation instance
        """
        filetransformation = self.adjust_duplicates(names, filetransformation)
        print(filetransformation)

    def adjust_duplicates(self, names: List[str], filetransformation: FileTransformation) -> FileTransformation:
        """Resolve duplicate filenames in list of target filenames.

        :param List[str] names: list of all filenames in :py:attr:`~directory`
        :param FileTransformation filetransformation: FileTransformation instance
        :return: FileTransformation instance
        :rtype: FileTransformation
        """
        # files not part of filter
        untouched_files = set(names) - set(filetransformation)

        # reverse the transformations dict
        reversed_transformations = filetransformation.get_reversed()

        for k, v in reversed_transformations.items():
            if len(v) > 1:
                # more than one filename is transformed to the same name
                for i, name in enumerate(v):
                    filetransformation[name] = FilenameHandler.add_suffix(filetransformation[name], f" ({str(i+1)})")
            elif len(v) == 1:
                # check if a transformed filename and an unfiltered file are duplicates
                if k in untouched_files:
                    filetransformation[next(iter(v))] = FilenameHandler.add_suffix(filetransformation[next(iter(v))], " (1)")

        return filetransformation

    def execute_from_file(self, names: List[str], filepath: str, undo: Optional[bool] = False):
        """Rename files on filesystem based on provided mapping from file.

        :param List[str] names: list of all filenames in :py:attr:`~directory`
        :param str filepath: path to file with source to target filename mapping
        :param undo: reverse loaded mapping, defaults to False
        :type undo: bool, optional
        :raises DuplicateFilenamesError: found duplicated among target filenames in loaded file
        """
        filetransformation = TransformationDecoder.decode_from_json_file(filepath)

        if undo:
            # TODO: use FileTransformation methods for get_reversed() and has_duplicate() instead
            reversed_transformation = {}
            for k, v in filetransformation.items():
                if v not in reversed_transformation:
                    reversed_transformation[v] = k
                else:
                    raise DuplicateFilenamesError(f"Two or more of the target filenames "
                                                  f"{os.path.join(self.directory, v)} imported from the "
                                                  f"JSON file were identical.")

            filetransformation = FileTransformation(reversed_transformation)

        self.execute(names, filetransformation)

    @property
    def actual_transformation(self) -> FileTransformation:
        """Getter for actual renaming as FileTransformation.

        :return: Actual transformation
        :rtype: FileTransformation
        """
        return self._actual_transformation

    @actual_transformation.setter
    def actual_transformation(self, val: FileTransformation):
        """Setter for actual renaming as FileTransformation.

        :param FileTransformation val: FileTransformation instance
        """
        self._actual_transformation = val
