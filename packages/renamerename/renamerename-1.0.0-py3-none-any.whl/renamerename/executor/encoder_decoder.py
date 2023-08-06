"""Serialization and Deserialization utility classes for FileTransformation"""

import json
import logging
import os
from datetime import datetime
from renamerename.handlers.filetransformation import FileTransformation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


class TransformationEncoder:
    """Serialization utility class for FileTransformation instance"""

    @staticmethod
    def encode_to_json_file(filetransformation: FileTransformation, path: str):
        """Serialize FileTransformation instance to JSON file.

        :param FileTransformation filetransformation: FileTransformation instance
        :param str path: serialization file path
        """
        with open(path, 'w') as f:
            json.dump(filetransformation.transformations, f, sort_keys=True, indent=0)

    @staticmethod
    def save_transformation_to_json(directory: str, filetransformation: FileTransformation):
        """Serialize FileTransformation instance to JSON file named renaming_DATE_TIME.json.

        :param str directory: parent directory where JSON file is saved
        :param filetransformation: FileTransformation instance
        """
        save_path = os.path.join(directory, "renaming_" + datetime.now().strftime("%d%m%Y_%H%M%S") + ".json")
        TransformationEncoder.encode_to_json_file(filetransformation, save_path)
        logging.info(f"Saved renaming to {save_path}")


class TransformationDecoder:
    """Deserialization utility class for FileTransformation instance"""

    @staticmethod
    def decode_from_json_file(path: str) -> FileTransformation:
        """Deserialize JSON file into FileTransformation instance.

        :param str path: path to JSON file
        :return: FileTransformation instance
        :rtype: FileTransformation
        """
        with open(path, 'r') as f:
            content = json.load(f)
        return FileTransformation(content)
