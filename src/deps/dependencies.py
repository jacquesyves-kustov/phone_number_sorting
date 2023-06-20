from typing import Optional, Callable

from config import AppConfig
from services.file_merger import FileMerger
from services.file_splitter import FileSplitter
from tools.files.manager import FileManager
from tools.files.paginated_reader import FilePaginatedReader


def file_reader_factory(directory_path: str, file_name: str) -> FilePaginatedReader:
    return FilePaginatedReader(
        directory_path=directory_path,
        file_name=file_name,
        rows_per_fetch=AppConfig.READER_LINES_PER_FETCH,
    )


def sort_list(lst: list[str]) -> list[str]:
    return sorted(lst)


def file_splitter_factory(
    source_file_reader: FilePaginatedReader,
    output_directory: str,
    preprocess_handler: Optional[Callable[[list[str]], list[str]]],
) -> FileSplitter:
    return FileSplitter(
        output_directory=output_directory,
        source_file_reader=source_file_reader,
        preprocess_handler=preprocess_handler,
        file_manager_cls=FileManager,
        max_lines_in_files=AppConfig.SPLITTER_MAX_ROW_IN_FILE,
        new_files_name_base=AppConfig.SPLITTER_NEW_FILE_NAME_BASE,
    )


def file_merger_factory(input_file_names: list[str]):
    return FileMerger(
        file_manager_cls=FileManager,
        input_file_names=input_file_names,
        input_file_directory=AppConfig.RESOURCES_PATH,
        output_file_directory=AppConfig.RESOURCES_PATH,
        output_file_name=AppConfig.MERGER_RESULT_FILE_NAME,
    )
