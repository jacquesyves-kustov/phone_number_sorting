import os
from typing import Type

from tools.files.manager import FileManager, FileManagerFileAlreadyExistsError
from tools.files.paginated_reader import FilePaginatedReader


class FileMerger:
    def __init__(
        self,
        input_file_directory: str,
        input_file_names: list[str],
        output_file_directory: str,
        output_file_name: str,
        limit_rows_to_write: int,
        file_manager_cls: Type[FileManager],
    ):
        # Init dependencies
        self._file_manager_cls = file_manager_cls

        # Set instance parameters
        self.result_file_directory = output_file_directory
        self.result_file_name = output_file_name
        self._limit_rows_to_write = limit_rows_to_write

        # Init file readers
        self._readers = [
            FilePaginatedReader(
                directory_path=input_file_directory,
                file_name=file_name,
                rows_per_fetch=1,
            ) for file_name in input_file_names
        ]

        # Get first values
        self._values_pool = [reader.read_next_lines()[0] for reader in self._readers]

    def merge_files(self):
        self._create_result_file()

        lines_to_write = []
        while self._values_pool:
            min_element_index = self._find_min_value_index()
            lines_to_write.append(self._values_pool[min_element_index])
            self._refresh_value_pool(min_element_index)

            if len(lines_to_write) > self._limit_rows_to_write:
                self._write_into_result_file(lines_to_write)
                lines_to_write.clear()

        if lines_to_write:
            self._write_into_result_file(lines_to_write)

    def _create_result_file(self):
        # It will clear result file if it is already created
        try:
            self._file_manager_cls.create_file(self.result_file_directory, self.result_file_name)
        except FileManagerFileAlreadyExistsError:
            open(os.path.join(self.result_file_directory, self.result_file_name), 'w').close()

    def _find_min_value_index(self) -> int:
        return self._values_pool.index(min(self._values_pool))

    def _write_into_result_file(self, lines: list[str]):
        line = ''.join(lines)
        with open(os.path.join(self.result_file_directory, self.result_file_name), 'a') as f:
            f.write(line)

    def _refresh_value_pool(self, reader_index: int):
        # Fetch next value from related file reader
        if new_value_from_reader := self._readers[reader_index].read_next_lines():
            self._values_pool[reader_index] = new_value_from_reader[0]
        else:
            self._values_pool.pop(reader_index)
            self._readers.pop(reader_index)
