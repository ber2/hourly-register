import yaml

from dataclasses import dataclass


@dataclass
class GDriveConfig:
    destination_folder_id: str

    @staticmethod
    def from_yaml_file(config_path: str) -> "GDriveConfig":
        yaml_config = _load_yaml(config_path)
        return GDriveConfig.extract_config_from_yaml_object(yaml_config)

    @staticmethod
    def extract_config_from_yaml_object(yaml_object) -> "GDriveConfig":
        destination_folder_id = yaml_object["app"]["destination_folder_id"]
        return GDriveConfig(destination_folder_id)


def _load_yaml(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)
