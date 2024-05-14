import aiofiles
import json
import models.dataset as DS


class MetadataFile:
    def __init__(self, filename: str, dataset_metadata: DS.DatasetMetadata = None, column_metadata: DS.ColumnMetadata = None):
        self.filename = filename
        self.dataset_metadata = dataset_metadata
        self.column_metadata = column_metadata

    def get_dataset_metadata(self) -> DS.DatasetMetadata:
        return self.dataset_metadata

    def get_column_metadata(self) -> DS.ColumnMetadata:
        return self.column_metadata

    def get_dataset_metadata_json(self) -> dict:
        return self.dataset_metadata.model_dump(mode='json')

    def get_column_metadata_json(self) -> dict:
        return self.column_metadata.model_dump(mode='json')

    def read_file(self) -> None:
        with open(self.filename) as f:
            is_dataset_metadata = True
            for line in f:
                json_line = json.loads(line)
                if is_dataset_metadata:
                    is_dataset_metadata = False
                    self.dataset_metadata = DS.DatasetMetadata(**json_line)
                else:
                    columns = []
                    for column in json_line["columns"]:
                        columns.append(DS.Column(**column))
                    self.column_metadata = DS.ColumnMetadata(columns=columns)

    def write_file(self, filename: str = None) -> None:
        if not filename:
            filename = self.filename
        with open(filename, mode='w') as f:
            f.write(f"{json.dumps(self.dataset_metadata.model_dump(mode='json', exclude_none=True))}\n")
            f.write(f"{json.dumps(self.column_metadata.model_dump(mode='json', exclude_none=True))}\n")
            f.flush()

    def show_file(self) -> None:
        print(f"{self.dataset_metadata.model_dump(mode='json', exclude_none=True)}")
        print(f"{self.column_metadata.model_dump(mode='json', exclude_none=True)}")
