import math
import os
import sys
from pathlib import Path


class AppConfigError(RuntimeError):
    pass


class AppConfigAutoSetupError(AppConfigError):
    pass


class AppConfig:
    # Fell free to change
    NUMBER_OF_ROWS_IN_GENERATED_FILE = 100_000_000
    RAM_PERCENT_TO_USE = 10

    # These fields will be changed automatically if you are Linux user
    READER_LINES_PER_FETCH = 500
    SPLITTER_MAX_ROW_IN_FILE = 1_000
    LIMIT_ROWS_TO_WRITE_PER_TIME = 500

    # It is not recommended to change these fields
    RESOURCES_PATH = Path(__file__).parent / '../resources'
    PHONE_NUMBERS_SOURCE_FILE = 'phones_raw.txt'
    SPLITTER_NEW_FILE_NAME_BASE = 'split_result'
    MERGER_RESULT_FILE_NAME = 'result'

    @classmethod
    def auto_setup(cls):
        try:
            memory_to_use_in_bytes = cls._get_memory_to_use_in_bytes()
            max_rows_in_memory = memory_to_use_in_bytes // cls._get_estimated_row_size_in_bytes()

            cls.READER_LINES_PER_FETCH = cls.LIMIT_ROWS_TO_WRITE_PER_TIME = max_rows_in_memory
            cls.SPLITTER_MAX_ROW_IN_FILE = max_rows_in_memory * 2

            print(f'Auto setup is completed successfully.')
            print(f'{memory_to_use_in_bytes / 1_000_000} mb of RAM will be used by app.')
            print(f'{round((cls.NUMBER_OF_ROWS_IN_GENERATED_FILE * cls._get_estimated_row_size_in_bytes()) / (1024 ** 3), 2)} gb is the source file size.')
            print(f'{math.ceil((cls.NUMBER_OF_ROWS_IN_GENERATED_FILE / cls.SPLITTER_MAX_ROW_IN_FILE))} temporary files will be created.')
            print(f'{cls.SPLITTER_MAX_ROW_IN_FILE} rows is the limit for temporary files.')
            print(f'{cls.READER_LINES_PER_FETCH} rows will be fetched from source file per time.')
            print(f'{cls.LIMIT_ROWS_TO_WRITE_PER_TIME} rows is the rows limit for writing to the result file.')

        except Exception:
            raise AppConfigAutoSetupError

    @classmethod
    def _get_memory_to_use_in_bytes(cls):
        total_memory, used_memory, free_memory = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
        return ((free_memory // 100) * cls.RAM_PERCENT_TO_USE) * 1_000_000

    @staticmethod
    def _get_estimated_row_size_in_bytes():
        return sys.getsizeof('+79123456789')
