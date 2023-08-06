"""Utility classes for mapping source filenames to target filenames."""

from collections.abc import MutableMapping
from typing import List, Dict


class FileTransformation(MutableMapping):
    """Wrapper class as dictionary or mapping of source filename to target filename."""

    def __init__(self, transformations: dict):
        """Constructor

        :param dict transformations: mapping of source to target filenames
        :raises TypeError: type of parameter given is not a dict
        """
        if type(transformations) == dict:
            self.transformations = transformations
        else:
            raise TypeError("An object type other than dict was passed to FileTransformation constructor.")

    def __setitem__(self, key, value):
        self.transformations[key] = value

    def __getitem__(self, key):
        return self.transformations[key]

    def __delitem__(self, key):
        del self.transformations[key]

    def __iter__(self):
        return iter(self.transformations)

    def __len__(self):
        return len(self.transformations)

    def __str__(self):
        output = ''
        for k, v in self.transformations.items():
            output += k + " ----> " + v + "\n"
        return output

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.transformations)})"

    @classmethod
    def from_list(cls, filenames: List[str]) -> "FileTransformation":
        """Construct FileTransformation instance from a list of filenames by mapping each filename to itself.

        :param List[str] filenames: list of filenames to wrap as a transformation
        :return: mapping of filenames to themselves
        :rtype: FileTransformation
        """
        return cls({name: name for name in filenames})

    def get_reversed(self) -> Dict[str, List[str]]:
        """Reverse mapping of source to target filenames, while maintain information on duplicate target filenames

        :return: mapping of target to list of source filenames
        :rtype: Dict[str: List[str]]
        """
        reversed_transformations = {}
        for k, v in self.transformations.items():
            reversed_transformations.setdefault(v, []).append(k)
        return reversed_transformations

    def has_duplicates(self) -> bool:
        """Check if target filenames contain duplicates.

        :return: truth value whether some target filenames are duplicates
        :rtype: bool
        """
        for v in self.get_reversed().values():
            if len(v) > 1:
                return True
        return False
