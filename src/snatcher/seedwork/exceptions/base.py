import traceback
import inspect
import os
from types import FrameType
from urllib.request import Request

from loguru import logger


class CustomException(Exception):
    """
    Base Exception customized

    Attributes:
        message (str): The error message describing the reason for the exception.

    Methods:
        __init__(self, message): Initializes the BaseException exception with the given message.
        __str__(self): Returns the error message as a string representation of the exception.
    """

    def __init__(self, message):
        self.message = message.replace("  ", "").replace("\n", "")
        super().__init__()

    def __str__(self):
        return self.message


class StandardErrorMessage:

    @staticmethod
    def format_exception_request_message(
        exc: Exception, message: str = "", request: Request = None
    ) -> NotImplementedError:
        raise NotImplementedError("Future development")

    @staticmethod
    def format_exception_error_message(exc: Exception, message: str = "") -> str:
        stack = traceback.extract_tb(exc.__traceback__)
        frame = stack[-1]

        relative_path = os.path.relpath(frame.filename)
        line_number = frame.lineno

        frame_info = inspect.getframeinfo(inspect.currentframe())
        method = frame_info.function

        error_message = (
            f"detail: {message: {message}},"
            f" error: {{code_line: {line_number}, relative_path: {relative_path}, method: ({method}), exception_message: {str(exc)}}}"
        )
        logger.error(error_message)

        return error_message

    @staticmethod
    def format_string_error_message(message: str) -> str:
        current_frame = inspect.currentframe()
        previous_frame = current_frame.f_back

        relative_path = os.path.relpath(previous_frame.f_code.co_filename)
        line_number = previous_frame.f_lineno

        method = previous_frame.f_code.co_name

        error_message = f"erro: {{code_line: {line_number}, relative_path: {relative_path}, method: ({method}), message: {message}}}"
        logger.error(error_message)

        return error_message
