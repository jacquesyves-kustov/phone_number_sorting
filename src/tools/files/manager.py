import os


class FileManagerError(RuntimeError):
    pass


class FileManagerFileAlreadyExistsError(FileManagerError):
    pass


class FileManagerFileDoesNotExistError(FileManagerError):
    pass


class FileManager:
    @staticmethod
    def create_file(directory_path: str, file_name: str):
        try:
            open(os.path.join(directory_path, file_name), 'x')
        except FileExistsError:
            raise FileManagerFileAlreadyExistsError

    @staticmethod
    def delete_file(directory_path: str, file_name: str):
        file_path = os.path.join(directory_path, file_name)

        try:
            os.remove(file_path)
        except FileExistsError:
            raise FileManagerFileDoesNotExistError
