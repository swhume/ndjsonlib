import unittest
import json
import ndjsonlib.json_data_file as JF
import ndjsonlib.dataset_name as DN
from pathlib import Path


class TestJsonService(unittest.TestCase):
    def test_append_json_row(self):
        with open("../data/ae_append_data.json", mode='r') as file:
            data = json.load(file)
        jf = JF.JsonDataFile(ds_name="ae", directory="../data")
        rows_added = jf.append_dataset(data)
        self.assertEqual(first=1, second=rows_added)  # add assertion here

    def test_read_dataset(self):
        dsn = DN.DatasetName(directory="../data", dataset_name="ae")
        df = JF.JsonDataFile(ds_name="ae", directory="../data")
        dataset = df.read_dataset()
        self.assertEqual(len(dataset['rows']), 74)

    def test_read_metadata(self):
        dsn = DN.DatasetName(directory="../data", dataset_name="ae")
        df = JF.JsonDataFile(ds_name="ae", directory="../data")
        metadata = json.loads(df.read_metadata())
        self.assertEqual(metadata['fileOID'], "www.cdisc.org/StudyMSGv2/1/Define-XML_2.1.0/2023-06-28/ae")

    def test_write_dataset(self):
        self._delete_test_dd_datasets()
        with open("./data/DD.json", mode='r') as file:
            data = json.load(file)
        jf = JF.JsonDataFile(ds_name="dd", directory="../data")
        jf.write_dataset(data)
        is_datafile_exists = Path("../data/dd_data.ndjson").exists()
        is_metadatafile_exists = Path("../data/dd_metadata.ndjson").exists()
        self.assertTrue(is_datafile_exists and is_metadatafile_exists)

    def _delete_test_dd_datasets(self):
        data_file = Path("../data/dd_data.ndjson")
        if data_file.exists():
            data_file.unlink()
        metadata_file = Path("../data/dd_metadata.ndjson")
        if metadata_file.exists():
            metadata_file.unlink()

    def test_write_metadata(self):
        metadata_file = Path("../data/dd_metadata.ndjson")
        if metadata_file.exists():
            metadata_file.unlink()
        self._write_dd_metadata()
        self.assertTrue(metadata_file.exists())

    def test_update_metadata(self):
        metadata_file = Path("../data/dd_metadata.ndjson")
        if not metadata_file.exists():
            self._write_dd_metadata()
        with open("./data/DD.json", mode='r') as file:
            dataset = json.load(file)
        jf = JF.JsonDataFile(ds_name="dd", directory="../data")
        jf.update_metadata_on_append(creation_date_time="2024-05-25T08:30:15.019423", rows_added=7)
        mf = JF.JsonDataFile(ds_name="dd", directory="../data")
        metadata = json.loads(mf.read_metadata())
        # restore metadata to original values
        self._write_dd_metadata()
        self.assertEqual(metadata['creationDateTime'], "2024-05-25T08:30:15.019423")
        self.assertEqual(metadata['records'], 10)

    def _write_dd_metadata(self):
        with open("./data/DD.json", mode='r') as file:
            dataset = json.load(file)
        jf = JF.JsonDataFile(ds_name="dd", directory="../data")
        del dataset['rows']
        jf.write_metadata(dataset)


if __name__ == '__main__':
    unittest.main()
