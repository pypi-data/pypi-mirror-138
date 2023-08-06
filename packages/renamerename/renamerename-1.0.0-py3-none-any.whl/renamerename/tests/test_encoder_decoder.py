import json
import pytest
from pytest_mock import mocker
from renamerename.executor.encoder_decoder import TransformationEncoder, TransformationDecoder
from renamerename.handlers.filetransformation import FileTransformation


@pytest.fixture
def file_transformation():
    return FileTransformation({
        "aaa": "foo_aaa",
        "bbb": "foo_bbb",
        "ccc": "foo_ccc"
    })


class TestEncoder:

    @pytest.fixture
    def transformation_encoder(self):
        return TransformationEncoder

    def test_encode_to_json_file(self, transformation_encoder, file_transformation, tmp_path):
        path = tmp_path / "renamed.json"
        transformation_encoder.encode_to_json_file(file_transformation, path)
        assert json.loads(path.read_text()) == {
            "aaa": "foo_aaa",
            "bbb": "foo_bbb",
            "ccc": "foo_ccc"
        }

    def test_save_transformation_to_json(self, transformation_encoder, file_transformation, mocker):
        date_mocker = mocker.patch('renamerename.executor.encoder_decoder.datetime')
        date_mocker.now().strftime.return_value = "DATE_TIME"
        import renamerename
        encode_mocker = mocker.patch.object(renamerename.executor.encoder_decoder.TransformationEncoder, 'encode_to_json_file')
        transformation_encoder.save_transformation_to_json(".", file_transformation)
        encode_mocker.assert_called_once_with(file_transformation, "./renaming_DATE_TIME.json")
        mocker.resetall()


class TestDecoder:

    @pytest.fixture
    def transformation_decoder(self):
        return TransformationDecoder

    def test_decode_from_json_file(self, transformation_decoder, tmp_path):
        path = tmp_path / "renamed.json"
        path.write_text(json.dumps({
            "aaa": "foo_aaa",
            "bbb": "foo_bbb",
            "ccc": "foo_ccc"
        }))
        actual_file_transformation = transformation_decoder.decode_from_json_file(path)
        assert actual_file_transformation.transformations == {
            "aaa": "foo_aaa",
            "bbb": "foo_bbb",
            "ccc": "foo_ccc"
        }
