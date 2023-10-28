class IncorrectToken(Exception):

    def __init__(self, message: str = "Incorrect token") -> None:
        super().__init__(message)

