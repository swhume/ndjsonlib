import datetime
from pydantic import BaseModel, AnyUrl
from typing import Optional, List, Literal


class Column(BaseModel):
    """ Dataset column, or variable, metadata attributes"""
    OID: Optional[str] = None
    name: str
    label: str
    type: Literal["string", "integer", "decimal", "float", "double", "boolean"]
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
    datasetType: Literal["clinicalData", "referenceData"]
    OID: str
    studyOID: str
    metaDataVersionOID: Optional[str] = None
    metaDataRef: Optional[AnyUrl] = None
    records: Optional[int] = 0
    name: str
    label: str



