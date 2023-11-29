import sys
import logging


class LoggerHandler(logging.Handler):
    """
    Custom logging handler that stores log entries in a string.

    This handler extends the logging.Handler class and overrides the emit() method to store log entries in a string attribute.

    Attributes:
        log (str): The accumulated log entries as a string.

    Methods:
        emit(record): Overrides the emit() method of the logging.Handler class to store log entries in the log attribute.

    Example:
        handler = LoggerHandler()
        logger = logging.getLogger()
        logger.addHandler(handler)

        logger.warning("This is a warning message")
        logger.error("This is an error message")

        print(handler.log)  # Output: "WARNING: This is a warning message\n\nERROR: This is an error message\n\n"
    """
    def __init__(self):
        super().__init__()
        self.log = ""

    def emit(self, record):
        if record.name == "httpx":
            return
        log_entry = self.format(record)
        self.log += log_entry
        self.log += "\n\n"


def get_logger(name: str) -> logging.Logger:
    """

    :param name: The name of the logger to create or retrieve.
    :return: The logger object.

    """
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S"
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
