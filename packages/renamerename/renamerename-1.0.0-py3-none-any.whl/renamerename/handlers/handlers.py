"""Utility classes for filename manipulators."""

import fnmatch
from pathlib import Path
from typing import List, Tuple, Optional
from renamerename.handlers.filetransformation import FileTransformation


class FilenameHandler:
    """Utility class for manipulating a filename."""

    @staticmethod
    def add_prefix(name: str, prefix: str) -> str:
        """Add a prefix to a filename.

        :param str name: filename with extension
        :param str prefix: prefix to be prepended to filename
        :return: filename with prepended prefix
        :rtype: str
        """
        return prefix + name

    @staticmethod
    def add_suffix(name: str, suffix: str) -> str:
        """Add a suffix to a filename.

        :param str name: filename with extension
        :param str suffix: suffix to be appended to filename
        :return: filename with appended suffix
        :rtype: str
        """
        filename, ext = FilenameHandler.get_components(name)
        return filename + suffix + ext

    @staticmethod
    def change_extension(name: str, new_ext: str) -> str:
        """Change the extension of a filename.

        :param name: filename with extension
        :param new_ext: desired extension of filename
        :return: filename with new extension
        :rtype: str
        """
        filename, _ = FilenameHandler.get_components(name)
        if not new_ext.startswith(".") and len(new_ext) != 0:
            new_ext = "." + new_ext
        return filename + new_ext

    @staticmethod
    def change_name(name: str, new_filename: str) -> str:
        """Change filename to new name.

        :param str name: filename with extension
        :param str new_filename: desired filename
        :return: changed filename (while preserving extension)
        :rtype: str
        """
        _, ext = FilenameHandler.get_components(name)
        return new_filename + ext

    @staticmethod
    def get_components(name: str) -> Tuple[str]:
        """Split pure filename and extension.

        :param str name: filename with extension
        :return: tuple of pure filename and extension
        :rtype: Tuple[str]
        """
        extensions = Path(name).suffixes
        filename = Path(name)
        for i, _ in enumerate(extensions):
            filename = Path(filename.stem)
        return str(filename), ''.join(extensions)


class FileListHandler:
    """Utility class for basic actions on a set of filenames."""

    def __init__(self, names: List[str]):
        """Constructor

        :param List[str] names: list of filenames
        """
        self.names = names
        self.filenames = self.names
        self.filenamehandler = FilenameHandler()
        self.filetransformations = FileTransformation.from_list(self.filenames)

    def filter_names(self, filter: Optional[str] = None):
        """Filter filenames based on a Unix pattern filter.

        :param str filter: pattern by which filenames are filtered out, defaults to None
        """
        if filter is None:
            self.filenames = self.names
        else:
            self.filenames = fnmatch.filter(self.names, filter)

    def add_prefix(self, prefix: str):
        """Add prefixes to filtered filenames.

        :param str prefix: prefix to be prepended to filtered filenames
        """
        for name in self.filenames:
            self.filetransformations[name] = self.filenamehandler.add_prefix(self.filetransformations[name], prefix)

    def add_suffix(self, suffix: str):
        """Add suffixes to filtered filenames.

        :param str suffix: suffix to be appended to filtered filenames
        """
        for name in self.filenames:
            self.filetransformations[name] = self.filenamehandler.add_suffix(self.filetransformations[name], suffix)

    def change_extension(self, new_ext: str):
        """Change extensions of filtered filenames.

        :param str new_ext: extension to be set for filtered filenames
        """
        for name in self.filenames:
            self.filetransformations[name] = self.filenamehandler.change_extension(self.filetransformations[name], new_ext)

    def add_numbering(self, prefix: str):
        """Change filtered filenames to same name with numbered suffixes.

        :param str prefix: new filename prepended to counter
        """
        for i, name in enumerate(self.filenames):
            new_name = self.filenamehandler.change_name(self.filetransformations[name], prefix)
            self.filetransformations[name] = self.filenamehandler.add_suffix(new_name, str(i))

    @property
    def filetransformations(self) -> FileTransformation:
        """Getter for mapping of source to target filenames.

        :return: FileTransformation instance
        :rtype: FileTransformation
        """
        return self._filetransformations

    @filetransformations.setter
    def filetransformations(self, val: FileTransformation):
        """Setter for mapping of source to target filenames.

        :param FileTransformation val: FileTransformation instance
        """
        self._filetransformations = val

    @property
    def filenames(self) -> List[str]:
        """Getter for filtered filenames.

        :return: filtered filenames
        :rtype: List[str]
        """
        return self._filenames

    @filenames.setter
    def filenames(self, val: List[str]):
        """Setter for filtered filenames.

        :param List[str] val: list of filenames
        """
        self._filenames = val
        self.filetransformations = FileTransformation.from_list(self._filenames)
