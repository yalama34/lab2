class ShellError(Exception):
    def __init__(self, message, filename=None):
        super().__init__(message)
        self.message = message
        self.filename = filename
class MissingFlagError(ShellError):
    pass
class OverwriteNonDirectoryError(ShellError):
    pass
class SameFileError(ShellError):
    pass
class InvalidMoveError(ShellError):
    pass
class NotAZipError(ShellError):
    pass
class NotATarError(ShellError):
    pass