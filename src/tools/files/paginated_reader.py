import os
from typing import Final


class FilePaginatedReader:
    def __init__(
        self,
        directory_path: str,
        file_name: str,
        rows_per_fetch: int,
    ):
        self._file_path: str = os.path.join(directory_path, file_name)
        self._rows_per_fetch: Final[int] = rows_per_fetch
        self._prev_byte_offset: int = 0
        self._is_file_read: bool = False

    def read_next_lines(self) -> list[str]:
        fetched_lines = []

        with open(self._file_path, mode='r') as f:
            f.seek(self._prev_byte_offset)

            # Fetch next '_rows_per_fetch' rows
            for _ in range(self._rows_per_fetch):
                if not (line := f.readline()):
                    self._is_file_read = True
                    break

                fetched_lines.append(line)

            self._prev_byte_offset = f.tell()

        return fetched_lines

    def is_file_fully_read(self):  # TODO: Change me into a property?
        return self._is_file_read
