import os


# TODO: Change to pydantic config class?
class AppConfig:
    RESOURCES_PATH = os.path.relpath('..\\resources', os.path.dirname(__file__))
    PHONE_NUMBERS_SOURCE_FILE = 'phones_raw.txt'
    READER_LINES_PER_FETCH = 500
    SPLITTER_MAX_ROW_IN_FILE = 1_000
    SPLITTER_NEW_FILE_NAME_BASE = 'split_result'
    MERGER_RESULT_FILE_NAME = 'result'
    NUMBER_OF_ROWS_IN_GENERATED_FILE = 10_000
    LIMIT_ROWS_TO_WRITE_PER_TIME = 500
