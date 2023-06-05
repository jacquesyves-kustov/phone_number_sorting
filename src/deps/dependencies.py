from config import AppConfig
from services.file_splitter import FileSplitter
from tools.files.manager import FileManager
from tools.files.paginated_reader import FilePaginatedReader


def sort_list(lst: list[str]) -> list[str]:
    return sorted(lst)


file_manager = FileManager()


file_reader = FilePaginatedReader(
    directory_path=AppConfig.RESOURCES_PATH,
    file_name=AppConfig.PHONE_NUMBERS_SOURCE_FILE,
    rows_per_fetch=AppConfig.READER_LINES_PER_FETCH,
)


file_splitter = FileSplitter(
    output_directory=AppConfig.RESOURCES_PATH,
    source_file_reader=file_reader,
    file_manager=file_manager,
    max_lines_in_files=AppConfig.SPLITTER_MAX_ROW_IN_FILE,
    preprocess_handler=sort_list,
)
