import json
import ndjsonlib.metadata_file as MF
import ndjsonlib.data_file as DF
import ndjsonlib.dataset_name as DN
import ndjsonlib.models.dataset as DS
import datetime


class JsonDataFile:
    def __init__(self, ds_name: str, directory: str, chunk_size: int = 1000):
        dsn = DN.DatasetName(directory, ds_name)
        self.metadata_filename = dsn.get_metadata_filename()
        self.data_filename = dsn.get_data_filename()
        self.dataset_filename = dsn.get_full_dataset_filename()
        self.dataset_json_filename = dsn.get_json_dataset_filename()
        self.creation_date_time = datetime.datetime.utcnow()
        self.chunk_size = chunk_size
        self.current_row = 0
        self.number_of_rows = 0

    def get_creation_date_time(self):
        return self.creation_date_time

    def get_number_of_rows(self):
        return self.number_of_rows

    def read_dataset(self) -> json:
        dataset = self._read_metadata()
        df = DF.DataFile(self.data_filename)
        ds = df.read_file()
        dataset['rows'] = ds.model_dump(mode='json')['rows']
        self.number_of_rows = dataset["records"]
        return dataset

    def read_dataset_chunk(self, offset: int) -> json:
        dataset = self._read_metadata()
        df = DF.DataFile(self.data_filename)
        ds = df.read_chunk(start_row=offset)
        dataset['rows'] = ds.model_dump(mode='json')['rows']
        self.number_of_rows = len(dataset["rows"])
        return dataset

    def read_full_json_dataset(self) -> json:
        """ utility method that reads a JSON dataset for converstion to ndjson """
        # TODO this will need to be enhanced for large datasets
        with open(self.dataset_json_filename) as f:
            dataset = json.load(f)
        return dataset

    def write_dataset(self, dataset: dict) -> None:
        ds = DS.RowData(rows=dataset["rows"])
        df = DF.DataFile(filename=self.dataset_filename, row_data=ds)
        del dataset['rows']
        # self.write_metadata(dataset, self.metadata_filename)
        self.write_metadata(dataset)
        df.write_file(self.data_filename)

    def write_full_dataset(self, dataset: dict) -> None:
        """ utility method that writes ndjson dataset as 1 combined file, metadata + data """
        ds = DS.RowData(rows=dataset["rows"])
        df = DF.DataFile(filename=self.data_filename, row_data=ds)
        del dataset['rows']
        # self.write_metadata(dataset, self.dataset_filename)
        self.write_metadata(dataset)
        rows_added = df.append_file(self.dataset_filename)
        return rows_added

    def append_dataset(self, dataset: dict) -> int:
        ds = DS.RowData(rows=dataset["rows"])
        df = DF.DataFile(filename=self.data_filename, row_data=ds)
        rows_added = df.append_file(self.data_filename)
        self.update_metadata_on_append(rows_added)
        return rows_added

    def update_metadata_on_append(self, rows_added) -> None:
        self.number_of_rows = 0
        mf = MF.MetadataFile(self.metadata_filename)
        mf.read_file()
        dataset = mf.get_metadata()
        # columns = mf.get_column_metadata()
        dataset.records += rows_added
        dataset.datasetJSONCreationDateTime = self.creation_date_time
        mf_out = MF.MetadataFile(self.metadata_filename, dataset)
        mf_out.write_file(self.metadata_filename)

    def read_metadata(self) -> dict:
        dataset = self._read_metadata()
        self.number_of_rows = 0
        # return json.dumps(dataset)
        return dataset

    def _read_metadata(self) -> dict:
        mf = MF.MetadataFile(self.metadata_filename)
        mf.read_file()
        dataset = mf.get_metadata_json()
        # columns = mf.get_column_metadata_json()
        # dataset['columns'] = columns["columns"]
        return dataset

    def write_metadata(self, metadata: dict) -> None:
        # columns = []
        # for column in metadata["columns"]:
        #     columns.append(DS.Column(**column))
        # column_metadata = DS.ColumnMetadata(columns=columns)
        # del metadata["columns"]
        metadata["datasetJSONCreateDateTime"] = datetime.datetime.utcnow()
        dataset_metadata = DS.DatasetMetadata(**metadata)
        # mf = MF.MetadataFile(self.metadata_filename, dataset_metadata=dataset_metadata, column_metadata=column_metadata)
        mf = MF.MetadataFile(self.metadata_filename, dataset_metadata=dataset_metadata)
        mf.write_file()

    def convert_json_metadata(self) -> dict:
        with open(self.metadata_filename) as f:
            metadata = json.load(f)
        # self.write_metadata(metadata, self.metadata_filename)
        self.write_metadata(metadata)
