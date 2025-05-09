# exception.py
# -----------------------------------------
# This file defines a custom exception class to handle errors more clearly in Python projects.
# It captures detailed information about where an error occurred — including the file name, 
# line number, and error message — which is helpful for debugging.
# It uses the sys module to extract traceback details during exceptions.

import sys  # Imports the sys module to access exception information (like traceback)
from src.logger import logging

# This function creates a detailed error message including filename, line number, and the actual error
def error_message_detail(error, error_detail: sys):
    # Gets exception information using sys.exc_info()
    _, _, exc_tb = error_detail.exc_info()

    # Extracts the filename from where the exception was raised
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Formats a detailed error message
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message  # Returns the formatted error message

# Custom exception class to include the detailed error message
class CustomException(Exception):
    # Constructor that initializes the custom error message
    def __init__(self, error_message, error_detail: sys):  # NOTE: You had a typo '__inti__'; corrected to '__init__'
        super().__init__(error_message)  # Calls the base Exception constructor
        # Calls the helper function to generate a detailed message
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    # String representation of the exception, returns the detailed error message
    def __str__(self):
        return self.error_message

