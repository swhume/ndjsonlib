import json
# import ndjsonlib.metadata_file as MF
# import ndjsonlib.data_file as DF
import ndjsonlib.dataset_name as DN
# import ndjsonlib.models.dataset as DS
# import datetime

DATASET_METADATA = 1
COLUMNS = 2

class NdjsonDataFile:
    def __init__(self, ds_name: str, directory: str, chunk_size: int = 1000):
        dsn = DN.DatasetName(directory, ds_name)
        self.dataset_filename = dsn.get_full_dataset_filename()
        self.chunk_size = chunk_size
        self.current_row = 0
        self.number_of_rows = 0
        self.columns = None
        self.dataset_metadata = None
        self.rows = []

    def get_row_count(self):
        return len(self.rows)

    def get_dataset_metadata(self):
        return self.dataset_metadata

    def get_columns(self):
        return self.columns

    def get_rows(self):
        return self.rows

    def read_dataset(self) -> json:
        # TODO will need to create a memory efficient means to transform dataset
        with open(self.dataset_filename) as f:
            for line_num, line in enumerate(f, 1):
                dataset_line = json.loads(line)
                if line_num == DATASET_METADATA:
                    # self.dataset_metadata = DS.DatasetMetadata(**json_line)
                    self.dataset_metadata = dataset_line
                elif line_num == COLUMNS:
                    # columns = []
                    # for column in dataset_line["columns"]:
                    #     columns.append(DS.Column(**column))
                    # self.columns = DS.ColumnMetadata(columns=columns)
                    self.columns = dataset_line
                else:
                    self.rows.append(dataset_line)

    def write_dataset_json(self, dataset_filename: str) -> None:
        # TODO inefficient
        dataset = self.dataset_metadata
        dataset["columns"] = self.columns
        dataset["rows"] = self.rows
        with open(dataset_filename, "w") as f:
            json.dump(dataset, f)

