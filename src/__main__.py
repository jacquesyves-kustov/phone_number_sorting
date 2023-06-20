from config import AppConfig
from deps.dependencies import (
    file_merger_factory,
    file_reader_factory,
    file_splitter_factory,
    sort_list,
    source_file_generator_factory,
)
from services.file_splitter import FileSplitter
from services.source_generator import SourceFileGenerator
from tools.execution_timer import measure_time
from tools.files.paginated_reader import FilePaginatedReader


def _init_resources() -> (SourceFileGenerator, FilePaginatedReader, FileSplitter):
    source_file_generator = source_file_generator_factory(
        output_directory_path=AppConfig.RESOURCES_PATH,
        output_file_name=AppConfig.PHONE_NUMBERS_SOURCE_FILE,
        rows_number_in_output_file=AppConfig.ROWS_NUMBER_IN_OUTPUT_FILE,
        limit_rows_to_write_per_time=AppConfig.LIMIT_ROWS_TO_WRITE_PER_TIME,
    )

    file_reader = file_reader_factory(
        directory_path=AppConfig.RESOURCES_PATH,
        file_name=AppConfig.PHONE_NUMBERS_SOURCE_FILE,
    )

    file_splitter = file_splitter_factory(
        output_directory=AppConfig.RESOURCES_PATH,
        source_file_reader=file_reader,
        preprocess_handler=sort_list,
    )

    return source_file_generator, file_reader, file_splitter


@measure_time
def main():
    # Step 0) Init resources
    source_file_generator, file_reader, file_splitter = _init_resources()

    # Step 1) Generate raw source file
    source_file_generator.generate_source_file()

    # Step 2) Split the raw file into several small files
    file_splitter.split_file()

    # Step 3) Merge resulted files into one
    file_merger = file_merger_factory(file_splitter.get_created_files_names())
    file_merger.merge_files()


main()
