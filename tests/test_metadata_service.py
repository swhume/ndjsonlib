import unittest
import ndjsonlib.metadata_file as MF
import ndjsonlib.dataset_name as DN


class TestMetadataService(unittest.TestCase):
    def test_read_metadata_file(self):
        dsn = DN.DatasetName("../data", "ae")
        mf = MF.MetadataFile(dsn.get_metadata_filename())
        mf.read_file()
        metadata = mf.get_dataset_metadata()
        self.assertEqual(metadata.fileOID, "www.cdisc.org/StudyMSGv2/1/Define-XML_2.1.0/2023-06-28/ae")

    def test_write_metadata_file(self):
        dsn_read = DN.DatasetName("../data", "ae")
        dsn_write = DN.DatasetName("../data", "ae_out")
        mf = MF.MetadataFile(dsn_read.get_metadata_filename())
        mf.read_file()
        mf_out = MF.MetadataFile(dsn_write.get_metadata_filename(), mf.dataset_metadata, mf.column_metadata)
        mf_out.write_file()
        mf_out.read_file()
        metadata = mf_out.get_dataset_metadata()
        self.assertEqual(metadata.fileOID, "www.cdisc.org/StudyMSGv2/1/Define-XML_2.1.0/2023-06-28/ae")


if __name__ == '__main__':
    unittest.main()