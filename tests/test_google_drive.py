import os
import pytest
import tempfile
import yaml

from gdrive import config
from gdrive import drive


@pytest.fixture
def file_name():
    return "file.py"


@pytest.fixture
def file_path(file_name):
    folder = tempfile.gettempdir()
    path = f"{folder}/{file_name}"

    f = open(path, "w")
    f.write("asdf")

    yield path

    f.close
    os.remove(path)


def test__extract_file_name_gets_the_filename_of_a_complete_path(file_path, file_name):
    result = drive._extract_file_name(file_path)
    assert result == file_name


def test__extract_file_name_crashes_on_non_existing_path():
    invalid_path = "/hoome/asdf"

    with pytest.raises(ValueError) as err:
        drive._extract_file_name(invalid_path)

    assert (
        err.value.args[0]
        == f"Input path must be an existing file path! Got '{invalid_path}'"
    )


@pytest.fixture
def config_destination_folder_id():
    return "my-target-google-drive-folder-id"


@pytest.fixture
def yaml_config_str(config_destination_folder_id):
    yaml_string = f"""
app:
  destination_folder_id: {config_destination_folder_id}

client_config_backend: settings
client_config:
  client_id: <your-google-drive-api-client-id>
  client_secret: <your-google-drive-api-client-secret>

save_credentials: True
save_credentials_backend: file
save_credentials_file: credentials.json
"""
    return yaml.safe_load(yaml_string)


def test_config_extracts_correct_values_from_yaml(
    yaml_config_str, config_destination_folder_id
):
    configuration = config.GDriveConfig.extract_config_from_yaml_object(yaml_config_str)
    assert configuration.destination_folder_id == config_destination_folder_id
