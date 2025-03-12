"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

class ADBConnectionException(Exception):
    """Custom exception for a specific error condition."""
    def __init__(self, message, code=None):
        # Initialize the exception with a message and optional code
        super().__init__(message)
        self.code = code

    def __str__(self):
        # Customize the string representation of the exception
        return f"Error: no device connected. {self.code}"
    
class OptionNotAvailable(Exception):
    """Custom exception for a specific error condition."""
    def __init__(self, message, code=None):
        # Initialize the exception with a message and optional code
        super().__init__(message)
        self.code = code

    def __str__(self):
        # Customize the string representation of the exception
        return f"Error: no device connected. {self.code}"