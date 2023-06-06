import os


class FileManagerError(RuntimeError):
    pass


class FileManagerFileAlreadyExistsError(FileManagerError):
    pass


class FileManager:
    @staticmethod
    def create_file(directory_path: str, file_name: str):
        try:
            open(os.path.join(directory_path, file_name), 'x')
        except FileExistsError:
            raise FileManagerFileAlreadyExistsError
