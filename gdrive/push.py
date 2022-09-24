from pathlib import Path

from gdrive.config import GDriveConfig
from gdrive.drive import GDrive


def push_to_gdrive(file_path: Path):
    gdrive_config = GDriveConfig.from_yaml_file("gdrive_config.yaml")
    gdrive = GDrive.from_config(gdrive_config)
    gdrive.push_file(str(file_path))
