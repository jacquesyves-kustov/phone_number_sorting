from config import AppConfig
from deps.dependencies import file_merger_factory, file_reader_factory, file_splitter_factory, sort_list
from services.file_splitter import FileSplitter
from tools.files.paginated_reader import FilePaginatedReader


def _init_resources() -> (FilePaginatedReader, FileSplitter):
    file_reader = file_reader_factory(
        directory_path=AppConfig.RESOURCES_PATH,
        file_name=AppConfig.PHONE_NUMBERS_SOURCE_FILE,
    )

    file_splitter = file_splitter_factory(
        output_directory=AppConfig.RESOURCES_PATH,
        source_file_reader=file_reader,
        preprocess_handler=sort_list,
    )

    return file_reader, file_splitter


def main():
    # Step 0) Init resources
    file_reader, file_splitter = _init_resources()

    # Step 1) Split the raw file into several small files
    file_splitter.split_file()

    # Step 2) Merge resulted files into one
    file_merger = file_merger_factory(file_splitter.get_created_files_names())
    file_merger.merge_files()


main()
