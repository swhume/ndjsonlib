import aiofiles
import json
import ndjsonlib.models.dataset as DS


class DataFile:
    def __init__(self, filename: str, chunk_size: int = 1000, row_data: DS.RowData = None):
        self.filename = filename
        self.chunk_size = chunk_size
        self.current_row = 0
        self.row_data = row_data

    def read_file(self) -> DS.RowData:
        rows = []
        with open(self.filename) as f:
            for line in f:
                rows.append(json.loads(line))
        return DS.RowData(rows=rows)

    def read_file_to_list(self) -> list:
        rows = []
        with open(self.filename) as f:
            for line in f:
                rows.append(json.loads(line))
        return DS.RowData.model_dump(rows=rows)

    def read_chunk(self, start_row: int = None) -> list:
        rows = []
        if start_row is None:
            start_row = self.current_row + 1
        with open(self.filename, mode='r') as f:
            line_count = 0
            for line in f:
                if line_count >= start_row:
                    rows.append(json.loads(line))
                line_count += 1
                if self.chunk_size and line_count >= self.chunk_size:
                    break
        self.current_row = start_row + len(rows)
        return DS.RowData(rows=rows)

    def write_file(self, filename: str = None) -> None:
        if filename is None:
            filename = self.filename
        with open(filename, mode='w') as f:
            for row in self.row_data.rows:
                f.write(f"{json.dumps(row)}\n")
            f.flush()

    def append_file(self, filename: str = None) -> int:
        if filename is None:
            filename = self.filename
        row_counter = 0
        with open(filename, mode='a') as f:
            for row in self.row_data.rows:
                f.write(f"{json.dumps(row)}\n")
                row_counter += 1
            f.flush()
        return row_counter

    def show_file(self) -> None:
        with open(self.filename) as f:
            for line in f:
                print(json.loads(line))
