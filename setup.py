from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='ndjsonlib',
    version='0.0.1',
    packages=['ndjsonlib', 'ndjsonlib.metadata_file', 'ndjsonlib.json_data_file',
              'ndjsonlib.dataset_name'],
    url='https://github.com/swhume/ndjsonlib',
    license='MIT',
    author='Sam Hume',
    author_email='swhume@gmail.com',
    description='Read and write Dataset-JSON as NDJSON',
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        "pydantic~=2.7.1",
        "ijson~=3.3.0",
    ]
)
