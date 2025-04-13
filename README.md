# ndjsonlib

## Introduction
![under development](https://img.shields.io/badge/under-development-blue)

The ndjsonlib module provides an interface to read and write Dataset-JSON as NDJSON. It can convert to and from the JSON
format of Dataset-JSON. It also supports storing NDJSON metadata and data as separate files and combining them for 
data exchange. Maintaining the metadata in a separate file makes it simple to update the datasetJsonCreationDatetime 
and the records attributes without requiring an application to re-write the entire file.

The ndjsonlib module was initiated to support a POC implementation of a draft Dataset-JSON API standard. The ndjsonlib
module remains under development and its API will evolve.

## Basic Structure and Interfaces
* **dataset_name.py**: Given the dataset name and the directory, the DatasetName class provides the file names needed for 
the metadata and data parts of the NDJSON dataset.
* **data_file.py**: The DataFile class provides methods for reading and writing the NDJSON data file
* **metadata_file.py**: The MetadataFile class provides methods for reading and writing the NDJSON metadata file
* **json_data_file.py**: The JsonDataFile class returns JSON by reading the NDJSON files and writes NDJSON given a JSON 
dataset. Basically, this class uses NDJSON as a data store for JSON inputs and outputs.
* **ndjson_data_file.py**: The NdjsonDataFile reads and writes NDJSON datasets as one file.

## Status
The ndjsonlib module has been updated to support Dataset-JSON v1.1 and is still under development. The ndjsonlib 
module was originally developed to support the Dataset-JSON API Proof-of-Concept.

## TODO
1. refine API / class interfaces
2. complete documentation
3. update tests

