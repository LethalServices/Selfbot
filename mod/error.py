from colorama import Fore, init

import logging, os

init(autoreset=True)

class CustomLogger:
    """
    A custom logger with both console and file handlers.
    Console logs are colorized while file logs are stored in a specified file.
    """

    def __init__(self, logger_name, log_level=logging.INFO, log_file_path="./Modules/Logs/error.log"):
        """
        Initialize the custom logger.
        :param logger_name: Name of the logger
        :param log_level: Logging level for the console handler
        :param log_file_path: Path to the log file for the file handler
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            self._add_console_handler(log_level)
            self._add_file_handler(log_file_path)

    def _add_console_handler(self, log_level):
        """Add a console handler with colorized logs."""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        formatter = logging.Formatter(f'【{Fore.LIGHTMAGENTA_EX}%(asctime)s{Fore.RESET}】'
                                      f'【{Fore.LIGHTYELLOW_EX}%(levelname)s{Fore.RESET}】'
                                      f'【{Fore.LIGHTBLUE_EX}%(name)s{Fore.RESET}】%(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _add_file_handler(self, log_file_path):
        """Add a file handler."""
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.ERROR)
        plain_formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s]%(message)s')
        file_handler.setFormatter(plain_formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        """Return the custom logger instance."""
        return self.logger
