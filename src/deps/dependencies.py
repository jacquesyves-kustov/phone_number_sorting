from config import AppConfig
from services.file_merger import FileMerger
from services.file_splitter import FileSplitter
from tools.files.manager import FileManager
from tools.files.paginated_reader import FilePaginatedReader


file_manager = FileManager()


file_reader = FilePaginatedReader(
    directory_path=AppConfig.RESOURCES_PATH,
    file_name=AppConfig.PHONE_NUMBERS_SOURCE_FILE,
    rows_per_fetch=AppConfig.READER_LINES_PER_FETCH,
)


def sort_list(lst: list[str]) -> list[str]:
    return sorted(lst)


file_splitter = FileSplitter(
    output_directory=AppConfig.RESOURCES_PATH,
    source_file_reader=file_reader,
    file_manager=file_manager,
    max_lines_in_files=AppConfig.SPLITTER_MAX_ROW_IN_FILE,
    preprocess_handler=sort_list,
    new_files_name_base=AppConfig.SPLITTER_NEW_FILE_NAME_BASE,
)


def file_merger_factory(input_file_names: list[str]):
    return FileMerger(
        file_manager=file_manager,
        input_file_names=input_file_names,
        input_file_directory=AppConfig.RESOURCES_PATH,
        output_file_directory=AppConfig.RESOURCES_PATH,
        output_file_name=AppConfig.MERGER_RESULT_FILE_NAME,
    )
