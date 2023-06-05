import os


# TODO: Change to pydantic config class?
class AppConfig:
    RESOURCES_PATH = os.path.relpath('..\\resources', os.path.dirname(__file__))
    PHONE_NUMBERS_SOURCE_FILE = 'phones_raw.txt'
    READER_LINES_PER_FETCH = 4
