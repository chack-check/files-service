class IncorrectFileName(Exception):

    def __init__(self, message: str = "Incorrect file name"):
        super().__init__(message)
