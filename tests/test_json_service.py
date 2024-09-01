import unittest
import json
import ndjsonlib.json_data_file as JF
import ndjsonlib.dataset_name as DN
from pathlib import Path


class TestJsonService(unittest.TestCase):
    def test_01_append_json_row(self):
        with open("../data/ae_append_data.json", mode='r') as file:
            data = json.load(file)
        jf = JF.JsonDataFile(ds_name="ae", directory="../data")
        rows_added = jf.append_dataset(data)
        self.assertEqual(first=1, second=rows_added)  # add assertion here

    def test_02_read_dataset(self):
        dsn = DN.DatasetName(directory="../data", dataset_name="ae")
        df = JF.JsonDataFile(ds_name="ae", directory="../data")
        dataset = df.read_dataset()
        self.assertEqual(len(dataset['rows']), 75)

    def test_03_read_metadata(self):
        self._delete_test_dd_datasets()
        with open("./data/DD.json", mode='r') as file:
            data = json.load(file)
        jf = JF.JsonDataFile(ds_name="dd", directory="../data")
        jf.write_dataset(data)
        is_datafile_exists = Path("../data/dd_data.ndjson").exists()
        is_metadatafile_exists = Path("../data/dd_metadata.ndjson").exists()
        self.assertTrue(is_datafile_exists and is_metadatafile_exists)
        dsn = DN.DatasetName(directory="../data", dataset_name="ae")
        df = JF.JsonDataFile(ds_name="ae", directory="../data")
        metadata = df.read_metadata()
        self.assertEqual(metadata['fileOID'], "www.cdisc.org/StudyMSGv2/1/Define-XML_2.1.0/2023-06-28/ae")

    def test_04_write_dataset(self):
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

    def test_05_write_metadata(self):
        metadata_file = Path("../data/dd_metadata.ndjson")
        if metadata_file.exists():
            metadata_file.unlink()
        self._write_dd_metadata()
        self.assertTrue(metadata_file.exists())

    def test_06_update_metadata(self):
        metadata_file = Path("../data/dd_metadata.ndjson")
        if not metadata_file.exists():
            self._write_dd_metadata()
        with open("./data/DD.json", mode='r') as file:
            dataset = json.load(file)
        jf = JF.JsonDataFile(ds_name="dd", directory="../data")
        jf.update_metadata_on_append(rows_added=7)
        mf = JF.JsonDataFile(ds_name="dd", directory="../data")
        metadata = mf.read_metadata()
        # restore metadata to original values
        self._write_dd_metadata()
        self.assertEqual(metadata["dbLastModifiedDateTime"], "2024-01-04T00:00:00")
        self.assertEqual(metadata['records'], 10)

    def test_07_reset_ae_dataset(self):
        dsn = DN.DatasetName(directory="../data", dataset_name="ae")
        df = JF.JsonDataFile(ds_name="ae", directory="../data")
        dataset = df.read_dataset()
        metadata = df.read_metadata()
        self.assertEqual(len(dataset['rows']), 75)
        self.assertEqual((metadata['records']), 75)
        # delete data and metadata files
        data_file = Path("../data/ae_data.ndjson")
        if data_file.exists():
            data_file.unlink()
        metadata_file = Path("../data/ae_metadata.ndjson")
        if metadata_file.exists():
            metadata_file.unlink()
        # reset the ae number of records
        dataset['rows'].pop()
        metadata['records'] = 74
        # write new data and metadata files
        df.write_dataset(dataset)
        df.write_metadata(metadata)
        # test that the new versions of the ae dataset files exist
        is_datafile_exists = Path("../data/ae_data.ndjson").exists()
        is_metadatafile_exists = Path("../data/ae_metadata.ndjson").exists()
        self.assertTrue(is_datafile_exists and is_metadatafile_exists)

    def _write_dd_metadata(self):
        with open("./data/DD.json", mode='r') as file:
            dataset = json.load(file)
        jf = JF.JsonDataFile(ds_name="dd", directory="../data")
        del dataset['rows']
        jf.write_metadata(dataset)


if __name__ == '__main__':
    unittest.main()
