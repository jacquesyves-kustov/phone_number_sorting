import os
from typing import Final, Callable, Optional, Type

from tools.files.manager import FileManager
from tools.files.paginated_reader import FilePaginatedReader


class FileSplitter:
    def __init__(
        self,
        file_manager_cls: Type[FileManager],
        source_file_reader: FilePaginatedReader,
        output_directory: str,
        new_files_name_base: str,
        max_lines_in_files: int,
        preprocess_handler: Optional[Callable[[list[str]], list[str]]],
    ):
        # Init dependencies
        self.file_manager_cls = file_manager_cls
        self._source_file_reader: FilePaginatedReader = source_file_reader

        # Set instance parameters
        self.output_directory: str = output_directory
        self._new_files_name_base: Final[str] = new_files_name_base
        self._max_lines_in_files: Final[int] = max_lines_in_files
        self._preprocess_handler: Optional[Callable[[list[str]], list[str]]] = preprocess_handler
        self._created_files_names: list[str] = []

    @property
    def created_files_names(self) -> list[str]:
        return self._created_files_names

    def split_file(self):
        lines_to_be_written: list[str] = []

        while not self._source_file_reader.is_file_read:
            fetched_lines = self._source_file_reader.read_next_lines()
            lines_to_be_written += fetched_lines

            if len(lines_to_be_written) >= self._max_lines_in_files:
                self._create_new_result_file(lines_to_be_written[:self._max_lines_in_files])
                lines_to_be_written = lines_to_be_written[self._max_lines_in_files:]

        if lines_to_be_written:
            self._create_new_result_file(lines_to_be_written[:self._max_lines_in_files])

    def _create_new_result_file(self, lines_to_write: list[str]):
        new_file_name = self._generate_new_file_name()
        self.file_manager_cls.create_file(
            directory_path=self.output_directory,
            file_name=new_file_name,
        )
        self._write_to_file(file_name=new_file_name, lines=lines_to_write)

    def _generate_new_file_name(self) -> str:
        name = self._new_files_name_base + str(len(self._created_files_names))
        self._created_files_names.append(name)
        return name

    def _write_to_file(
        self,
        file_name: str,
        lines: list[str],
    ):
        if self._preprocess_handler:
            lines = self._preprocess_handler(lines)

        with open(os.path.join(self.output_directory, file_name), mode='w') as f:
            for line in lines:
                f.write(line)
