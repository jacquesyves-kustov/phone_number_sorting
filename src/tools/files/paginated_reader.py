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
        self._last_fetched_line: int = 0
        self._is_file_read: bool = False

    def read_next_lines(self) -> list[str]:
        current_row = 0
        fetched_lines = []

        with open(self._file_path, mode='r') as f:
            # Move to the last fetched row
            while current_row != self._last_fetched_line:
                f.readline()
                current_row += 1

            # Fetch next '_rows_per_fetch' rows
            for _ in range(self._rows_per_fetch):
                if not (line := f.readline()):
                    self._is_file_read = True
                    break

                self._last_fetched_line += 1
                fetched_lines.append(line)

        return fetched_lines

    def is_file_fully_read(self):  # TODO: Change me into a property?
        return self._is_file_read
