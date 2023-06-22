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
        file_manager_cls: Type[FileManager],
    ):
        # Init dependencies
        self._file_manager_cls = file_manager_cls

        # Set instance parameters
        self.result_file_directory = output_file_directory
        self.result_file_name = output_file_name

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

        while self._is_value_pool_empty():
            min_element_index = self._find_min_value_index()
            self._write_into_result_file(self._values_pool[min_element_index])
            self._refresh_value_pool(min_element_index)

    def _create_result_file(self):
        # It will clear result file if it is already created
        try:
            self._file_manager_cls.create_file(self.result_file_directory, self.result_file_name)
        except FileManagerFileAlreadyExistsError:
            open(os.path.join(self.result_file_directory, self.result_file_name), 'w').close()

    def _is_value_pool_empty(self) -> bool:
        return bool(self._values_pool)

    def _find_min_value_index(self) -> int:
        return self._values_pool.index(min(self._values_pool))

    def _write_into_result_file(self, line):
        with open(os.path.join(self.result_file_directory, self.result_file_name), 'a') as f:
            f.write(line)

    def _refresh_value_pool(self, reader_index: int):
        # Fetch next value from related file reader
        if new_value_from_reader := self._readers[reader_index].read_next_lines():
            self._values_pool[reader_index] = new_value_from_reader[0]
        else:
            self._values_pool.pop(reader_index)
            self._readers.pop(reader_index)
