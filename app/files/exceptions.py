class IncorrectFileName(Exception):

    def __init__(self, message: str = "Incorrect file name"):
        super().__init__(message)


class FileWithoutFilenameError(Exception):

    def __init__(self, message: str = "You need to upload file with filename"):
        super().__init__(message)


class CantConvertFile(Exception):

    def __init__(self, convert_to: str):
        super().__init__(f"Can't convert file to {convert_to} extension: there are no such converters")


class IncorrectMIMEType(Exception):

    def __init__(self, filename: str):
        super().__init__(f"There is no MIME type for filename {filename}")


class FileValidationError(Exception):
    ...
