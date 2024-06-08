from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='ndjsonlib',
    version='0.0.1',
    packages=['ndjsonlib', 'ndjsonlib.data_file', 'ndjsonlib.metadata_file', 'ndjsonlib.json_data_file'],
    url='https://github.com/swhume/ndjsonlib',
    license='MIT',
    author='Sam Hume',
    author_email='swhume@gmail.com',
    description='Read and write Dataset-JSON as NDJSON'
)
