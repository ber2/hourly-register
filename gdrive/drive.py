from pathlib import Path

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from gdrive.config import GDriveConfig


class GDrive:
    def __init__(self, target_location_id: str):
        self.auth = GoogleAuth(settings_file="gdrive_config.yaml")
        self.auth.LocalWebserverAuth()
        self.target_location_id = target_location_id

        self.drive = GoogleDrive(self.auth)

    def push_file(self, local_file_path: str):
        file = self._create_file(local_file_path)
        file.Upload()

    def _create_file(self, local_file_path: str):
        file_name = _extract_file_name(local_file_path)

        request_body = {
            "title": file_name,
            "parents": [{"kind": "drive#fileLink", "id": self.target_location_id}],
        }
        file = self.drive.CreateFile(request_body)
        file.SetContentFile(local_file_path)

        return file

    @staticmethod
    def from_config(config: GDriveConfig):
        return GDrive(config.destination_folder_id)


def _extract_file_name(path: str) -> str:
    local_path = Path(path)

    if not local_path.is_file():
        raise ValueError(f"Input path must be an existing file path! Got '{path}'")

    return local_path.name


def upload_file(local_file: str, gdrive_destination_folder_id: str):
    drive = GDrive(gdrive_destination_folder_id)
    drive.push_file(local_file)
