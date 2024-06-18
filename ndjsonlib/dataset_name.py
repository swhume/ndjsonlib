import os
from pathlib import Path


class DatasetName:
    def __init__(self, directory: str = None, dataset_name: str = None, full_name: str = None):
        if directory and dataset_name:
            self.path = directory
            self.ds_name = dataset_name
        elif full_name:
            self.ds_name = Path(full_name).stem
            self.path = str(Path(full_name).parent)
        else:
            raise ValueError('Either a directory and dataset name or a full name (path with filename is required.')
        self.metadata_filename = self._create_metadata_filename()
        self.data_filename = self._create_data_filename()
        self.dataset_filename = self._create_full_dataset_filename()

    def get_metadata_filename(self):
        return self.metadata_filename

    def get_data_filename(self):
        return self.data_filename

    def get_full_dataset_filename(self):
        return self.dataset_filename

    def get_path(self):
        return self.path

    def get_ds_name(self):
        return self.ds_name

    def _create_metadata_filename(self) -> str:
        filename = os.path.join(self.path, self.ds_name + "_metadata.ndjson")
        return filename

    def _create_data_filename(self) -> str:
        filename = os.path.join(self.path, self.ds_name + "_data.ndjson")
        return filename

    def _create_full_dataset_filename(self) -> str:
        filename = os.path.join(self.path, self.ds_name + ".ndjson")
        return filename
