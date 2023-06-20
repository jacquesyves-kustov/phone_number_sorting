import os


# TODO: Change to pydantic config class?
class AppConfig:
    RESOURCES_PATH = os.path.relpath('..\\resources', os.path.dirname(__file__))
    PHONE_NUMBERS_SOURCE_FILE = 'phones_raw.txt'
    READER_LINES_PER_FETCH = 4
    SPLITTER_MAX_ROW_IN_FILE = 3
    SPLITTER_NEW_FILE_NAME_BASE = 'split_result'
    MERGER_RESULT_FILE_NAME = 'result'
    ROWS_NUMBER_IN_OUTPUT_FILE = 100
    LIMIT_ROWS_TO_WRITE_PER_TIME = 30
