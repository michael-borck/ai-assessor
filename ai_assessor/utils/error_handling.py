import logging
import os
import tempfile
import traceback


class ErrorHandler:
    """
    Handles errors in the application.
    """

    # Set up logging
    @staticmethod
    def setup_logging(log_file=None, level=logging.INFO):
        """
        Set up logging for the application.

        Args:
            log_file (str): Path to the log file (defaults to user home directory)
            level (int): Logging level
        """
        if log_file is None:
            # Default to user's home directory or temp if running from AppImage
            if os.getenv("APPIMAGE"):
                # Running as AppImage - use temp directory
                log_file = os.path.join(os.path.expanduser("~"), "aiassessor.log")
            else:
                # Running normally - use current directory
                log_file = "aiassessor.log"

        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except OSError:
                # If we can't create the log directory, fall back to temp
                log_file = os.path.join(tempfile.gettempdir(), "aiassessor.log")

        logging.basicConfig(
            filename=log_file,
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    @staticmethod
    def handle_api_error(error, context=None):
        """
        Handle API errors.

        Args:
            error (Exception): The error that occurred
            context (str, optional): Context information

        Returns:
            str: Error message
        """
        error_msg = f"API Error: {str(error)}"
        if context:
            error_msg = f"{context}: {error_msg}"

        full_error_msg = f"{error_msg}\n\nTraceback:\n{traceback.format_exc()}"
        logging.error(full_error_msg)
        return full_error_msg

    @staticmethod
    def handle_file_error(error, file_path=None):
        """
        Handle file-related errors.

        Args:
            error (Exception): The error that occurred
            file_path (str, optional): Path to the file

        Returns:
            str: Error message
        """
        if isinstance(error, FileNotFoundError):
            error_type = "File not found"
        elif isinstance(error, PermissionError):
            error_type = "Permission denied"
        else:
            error_type = "File error"

        error_msg = f"{error_type}: {str(error)}"
        if file_path:
            error_msg = f"{error_msg} ({file_path})"

        logging.error(error_msg)
        logging.debug(traceback.format_exc())

        return error_msg

    @staticmethod
    def handle_validation_error(error, field=None):
        """
        Handle validation errors.

        Args:
            error (Exception): The error that occurred
            field (str, optional): Field that failed validation

        Returns:
            str: Error message
        """
        error_msg = f"Validation error: {str(error)}"
        if field:
            error_msg = f"{field}: {error_msg}"

        logging.error(error_msg)

        return error_msg
