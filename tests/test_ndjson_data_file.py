import unittest
import json
import ndjsonlib.ndjson_data_file as NF
from pathlib import Path


class TestNdjsonDataFile(unittest.TestCase):
    def test_read_dataset(self):
        nf = NF.NdjsonDataFile(ds_name="dd", directory="./data", chunk_size=1000)
        nf.read_dataset()
        self.assertEqual(nf.get_row_count(), 3)
        metadata = nf.get_metadata()
        self.assertEqual(metadata["itemGroupOID"], "IG.DD")
        self.assertEqual(metadata["dbLastModifiedDateTime"], "2024-01-04T00:00:00")

    def test_write_json_dataset(self):
        self._delete_test_dd_dataset()
        nf = NF.NdjsonDataFile(ds_name="dd", directory="./data", chunk_size=1000)
        nf.read_dataset()
        json_filename = "./data/dd_test.json"
        nf.write_dataset_json(json_filename)
        is_dataset_file_exists = Path("./data/dd_test.json").exists()
        self.assertTrue(is_dataset_file_exists)

    def _delete_test_dd_dataset(self):
        dataset_file = Path("../data/dd_test.json")
        if dataset_file.exists():
            dataset_file.unlink()


if __name__ == '__main__':
    unittest.main()
