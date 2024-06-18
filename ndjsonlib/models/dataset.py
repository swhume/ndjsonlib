import datetime
from pydantic import BaseModel, AnyUrl
from typing import Optional, List, Literal


class Column(BaseModel):
    """ Dataset column, or variable, metadata attributes"""
    itemOID: Optional[str] = None
    name: str
    label: str
    dataType: Literal["string", "integer", "decimal", "float", "double", "decimal", "datetime", "boolean"]
    targetDataType: Optional[Literal["decimal", "integer"]] = None
    length: Optional[int] = None
    displayFormat: Optional[str] = None
    keySequence: Optional[int] = None


class ColumnMetadata(BaseModel):
    columns: List[Column]


class RowData(BaseModel):
    """ Dataset-JSON records to append to an existing dataset """
    rows: List = []


class DatasetMetadata(BaseModel):
    """ Dataset-JSON ndjson metadata model """
    creationDateTime: Optional[datetime.datetime] = datetime.datetime.utcnow()
    datasetJSONVersion: Literal["1.0.0", "1.1.0"]
    fileOID: Optional[str] = None
    asOfDateTime: Optional[datetime.datetime] = None
    originator: Optional[str] = None
    sourceSystem: Optional[str] = None
    sourceSystemVersion: Optional[str] = None
    datasetType: Optional[Literal["clinicalData", "referenceData"]] = None
    itemGroupOID: str
    studyOID: str
    metaDataVersionOID: Optional[str] = None
    metaDataRef: Optional[str] = None
    records: Optional[int] = 0
    name: str
    label: str



