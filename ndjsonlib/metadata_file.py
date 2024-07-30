import json
import ndjsonlib.models.dataset as DS


class MetadataFile:
    # def __init__(self, filename: str, dataset_metadata: DS.DatasetMetadata = None, column_metadata: DS.ColumnMetadata = None):
    def __init__(self, filename: str, dataset_metadata: DS.DatasetMetadata = None):
        self.filename = filename
        self.metadata = dataset_metadata
        # self.column_metadata = column_metadata

    def get_metadata(self) -> DS.DatasetMetadata:
        return self.metadata

    def get_column_metadata(self) -> list:
        return self.metadata["columns"]

    def get_metadata_json(self) -> dict:
        return self.metadata.model_dump(mode='json')

    def get_column_metadata_json(self) -> dict:
        return self.metadata["columns"].model_dump(mode='json')

    def read_file(self) -> None:
        with open(self.filename) as f:
            json_line = json.loads(f.read())
            self.metadata = DS.DatasetMetadata(**json_line)

    def write_file(self, filename: str = None) -> None:
        if not filename:
            filename = self.filename
        with open(filename, mode='w') as f:
            f.write(f"{json.dumps(self.metadata.model_dump(mode='json', exclude_none=True))}\n")
            # f.write(f"{json.dumps(self.column_metadata.model_dump(mode='json', exclude_none=True))}\n")
            f.flush()

    def show_file(self) -> None:
        print(f"{self.metadata.model_dump(mode='json', exclude_none=True)}")
        # print(f"{self.column_metadata.model_dump(mode='json', exclude_none=True)}")
