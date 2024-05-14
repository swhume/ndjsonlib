import json
import services.metadata_file as MF
import services.data_file as DF
import os


class JsonDataFile:
    def __init__(self, ds_name: str, directory: str, chunk_size: int = 1000):
        self.metadata_filename = os.path.join(directory, ds_name + "_metadata.ndjson")
        self.data_filename = os.path.join(directory, ds_name + "_data.ndjson")
        self.chunk_size = chunk_size
        self.current_row = 0

    def read_dataset(self):
        mf = MF.MetadataFile(self.metadata_filename)
        mf.read_file()
        dataset = mf.get_dataset_metadata_json()
        columns = mf.get_column_metadata_json()
        dataset['columns'] = columns["columns"]
        df = DF.DataFile(self.data_filename)
        # dataset['rows'] = df.read_file_to_list()
        ds = df.read_file()
        dataset['rows'] = ds.model_dump(mode='json')
        return json.dumps(dataset, indent=4)
