import json
import ndjsonlib.dataset_name as DN

METADATA = 1
# DATASET_METADATA = 1
# COLUMNS = 2

class NdjsonDataFile:
    def __init__(self, ds_name: str, directory: str, chunk_size: int = 1000):
        dsn = DN.DatasetName(directory, ds_name)
        self.dataset_filename = dsn.get_full_dataset_filename()
        self.chunk_size = chunk_size
        self.current_row = 0
        self.number_of_rows = 0
        # self.columns = None
        self.metadata = None
        self.rows = []

    def get_row_count(self):
        return len(self.rows)

    def get_metadata(self):
        return self.metadata

    def get_columns(self):
        return self.metadata["columns"]

    def get_rows(self):
        return self.rows

    def read_dataset(self) -> json:
        # TODO will need to create a memory efficient means to transform large datasets
        with open(self.dataset_filename) as f:
            for line_num, line in enumerate(f, 1):
                dataset_line = json.loads(line)
                if line_num > METADATA:
                    self.rows.append(dataset_line)
                else:
                    self.metadata = dataset_line

    def write_dataset_json(self, dataset_filename: str) -> None:
        dataset = self.metadata
        dataset["rows"] = self.rows
        with open(dataset_filename, "w") as f:
            json.dump(dataset, f)

