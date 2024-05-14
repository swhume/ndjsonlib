import services.metadata_file as MF
import services.data_file as DF
import services.json_data_file as JF
import argparse
import os


def create_metadata_filename(directory: str, ds_name: str) -> str:
    filename = os.path.join(directory, ds_name + "_metadata.ndjson")
    return filename


def create_data_filename(directory: str, ds_name: str) -> str:
    filename = os.path.join(directory, ds_name + "_data.ndjson")
    return filename


def set_cmd_line_args():
    """
    get the command-line arguments needed to determine the details of the dsj conversion
    :return: return the argparse object with the command-line parameters
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--directory", help="the dataset path or directory", required=False,
                        dest="directory", default="./data")
    parser.add_argument("-n", "--name", help="dataset or domain name, e.g. AE", required=True,
                        dest="dataset_name")
    parser.add_argument("-m", "--is_metadata", help="process the metadata only", default=False, const=True,
                        nargs='?', dest="is_metadata")
    args = parser.parse_args()
    return args


def main():
    args = set_cmd_line_args()
    # test reading and showing a metadata dataset
    metadata_file = create_metadata_filename(args.directory, args.dataset_name)
    mf = MF.MetadataFile(metadata_file)
    mf.read_file()
    # mf.show_file()

    # test writing a metadata dataset file
    metadata_out_file = create_metadata_filename("./data", "ae_out")
    mf_out = MF.MetadataFile(metadata_out_file, mf.dataset_metadata, mf.column_metadata)
    mf_out.write_file()

    # test reading and showing the data dataset
    data_file = create_data_filename(args.directory, args.dataset_name)
    df = DF.DataFile(data_file)
    df.read_file()
    # df.show_file()

    # test reading ndjson but returning a json version
    jf = JF.JsonDataFile(args.dataset_name, args.directory)
    json_ds = jf.read_dataset()
    print(json_ds)


if __name__ == "__main__":
    main()
