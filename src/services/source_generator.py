import os
from typing import Final, Type

from tools.files.manager import FileManager, FileManagerFileAlreadyExistsError
from tools.phone_number_generator import PhoneNumberGenerator


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
        self._prepare_file(output_file_path)
        self._fill_file_with_generated_rows(output_file_path)

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

            # TODO: Rewrite me pls ._.
            with open(output_file_path, 'a') as f:
                for number in new_numbers:
                    f.write(number)
                    written_rows_counter += 1

                    if written_rows_counter < self._rows_number_in_output_file:
                        f.write('\n')
