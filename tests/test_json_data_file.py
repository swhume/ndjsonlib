import unittest
import json
import ndjsonlib.json_data_file as JF
import ndjsonlib.ndjson_data_file as NF
from pathlib import Path


class TestJsonDataFile(unittest.TestCase):

    def test_read_dataset(self):
        jf = JF.JsonDataFile(ds_name="DD", directory="./data", chunk_size=1000)
        dataset = jf.read_full_json_dataset()
        self.assertEqual(dataset["itemGroupOID"], "IG.DD")
        self.assertEqual(dataset["studyOID"], "CDISCPILOT02")
        self.assertEqual(dataset["dbLastModifiedDateTime"], "2024-01-04T00:00:00")

    def test_write_full_dataset(self):
        """ tests writing ndjson as one file """
        self._delete_test_dd_dataset()
        with open("./data/DD.json", mode='r') as file:
            data = json.load(file)
        jf = JF.JsonDataFile(ds_name="dd", directory="../data", chunk_size=1000)
        jf.write_full_dataset(data)
        is_dataset_file_exists = Path("../data/dd.ndjson").exists()
        self.assertTrue(is_dataset_file_exists)
        nf = NF.NdjsonDataFile(ds_name="dd", directory="../data", chunk_size=1000)
        nf.read_dataset()
        self.assertEqual(nf.get_row_count(), 3)

    def _delete_test_dd_dataset(self):
        dataset_file = Path("../data/dd.ndjson")
        if dataset_file.exists():
            dataset_file.unlink()
        data_file = Path("../data/dd_data.ndjson")
        if data_file.exists():
            data_file.unlink()
        metadata_file = Path("../data/dd_metadata.ndjson")
        if metadata_file.exists():
            metadata_file.unlink()


if __name__ == '__main__':
    unittest.main()
