import os
import sys
from shutil import disk_usage
from typing import Final, Type

from tools.files.manager import FileManager, FileManagerFileAlreadyExistsError
from tools.phone_number_generator import PhoneNumberGenerator


class SourceFileGeneratorError(RuntimeError):
    pass


class SourceFileGeneratorNotEnoughSpaceOnDiskError(SourceFileGeneratorError):
    pass


class SourceFileGenerator:
    def __init__(
        self,
        output_directory: str,
        output_file_name: str,
        rows_number_in_output_file: int,
        limit_rows_to_write_per_time: int,
        phone_number_generator_cls: Type[PhoneNumberGenerator],
        file_manager_cls: Type[FileManager],
    ):
        self._output_directory: Final[str] = output_directory
        self._output_file_name: Final[str] = output_file_name
        self._rows_number_in_output_file: Final[int] = rows_number_in_output_file
        self._limit_rows_to_write_per_time: Final[int] = limit_rows_to_write_per_time
        self._phone_number_generator_cls: Type[PhoneNumberGenerator] = phone_number_generator_cls
        self._file_manager_cls: Type[FileManager] = file_manager_cls

    def generate_source_file(self):
        output_file_path: str = os.path.join(self._output_directory, self._output_file_name)

        if not self._is_free_space_enough_to_save_file():
            raise SourceFileGeneratorNotEnoughSpaceOnDiskError

        self._prepare_file(output_file_path)
        self._fill_file_with_generated_rows(output_file_path)

    def _is_free_space_enough_to_save_file(self) -> bool:
        estimated_new_file_size = self._get_estimated_source_file_size_in_bytes() * self._rows_number_in_output_file
        total, used, free = disk_usage('/')

        return free < estimated_new_file_size

    @staticmethod
    def _get_estimated_source_file_size_in_bytes():
        return sys.getsizeof('+79123456789')

    def _prepare_file(self, output_file_path: str):
        # It will make the output file empty if it is already created
        try:
            self._file_manager_cls.create_file(self._output_directory, self._output_file_name)
        except FileManagerFileAlreadyExistsError:
            open(output_file_path, 'w').close()

    def _fill_file_with_generated_rows(self, output_file_path: str):
        written_rows_counter = 0

        while written_rows_counter < self._rows_number_in_output_file:
            phone_number_numbers_to_generate = self._limit_rows_to_write_per_time
            if self._rows_number_in_output_file - written_rows_counter < phone_number_numbers_to_generate:
                phone_number_numbers_to_generate = self._rows_number_in_output_file - written_rows_counter

            new_numbers = self._phone_number_generator_cls.generate_random_numbers(
                limit=phone_number_numbers_to_generate,
            )

            with open(output_file_path, 'a') as f:
                for number in new_numbers:
                    f.write(number)
                    f.write('\n')

            written_rows_counter += len(new_numbers)
