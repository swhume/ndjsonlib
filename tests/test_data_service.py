import unittest
import ndjsonlib.data_file as DF
import ndjsonlib.dataset_name as DN


class TestDataService(unittest.TestCase):
    def test_read_data_file(self):
        dsn = DN.DatasetName("../data", "ae")
        fin = dsn.get_data_filename()
        df = DF.DataFile(dsn.get_data_filename())
        df_rows = df.read_file()
        self.assertEqual(len(df_rows.rows), 74)

    def test_write_data_file(self):
        dsn_read = DN.DatasetName("../data", "ae")
        dsn_write = DN.DatasetName("../data", "ae_out")
        mf = DF.DataFile(dsn_read.get_data_filename())
        df_rows = mf.read_file()
        mf_out = DF.DataFile(filename=dsn_write.get_data_filename(), row_data=df_rows)
        mf_out.write_file()
        df_rows = mf_out.read_file()
        self.assertEqual(len(df_rows.rows), 74)


if __name__ == '__main__':
    unittest.main()
