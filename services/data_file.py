import aiofiles
import json
import models.dataset as DS


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

    async def read_chunk(self, start_row: int = None) -> list:
        rows = []
        if start_row is None:
            start_row = self.current_row + 1
        async with aiofiles.open(self.filename) as f:
            line_count = 0
            async for line in f:
                if line_count >= start_row:
                    rows.append(json.loads(line))
                line_count += 1
                if line_count >= self.chunk_size:
                    break
        self.current_row = start_row + len(rows)
        return DS.RowData(rows=rows)

    async def write_file(self, filename: str = None) -> None:
        if filename is None:
            filename = self.filename
        async with aiofiles.open(filename, mode='w') as f:
            async for row in self.row_data:
                await f.write(f"{json.dumps(row)}\n")
            await f.flush()

    def show_file(self) -> None:
        with open(self.filename) as f:
            for line in f:
                print(json.loads(line))
