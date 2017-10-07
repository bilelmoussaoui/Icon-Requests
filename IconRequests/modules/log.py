import logging
import sys


class Logger:
    """Logger class"""
    FORMAT = "[%(levelname)-s] %(asctime)s %(message)s"
    DATE = "%Y-%m-%d %H:%M:%S"
    # Logger instance
    instance = None

    @staticmethod
    def get_default():
        """Return default instance of Logger."""
        if Logger.instance is None:
            logger = logging.getLogger("com.github.bilelmoussaoui.IconRequests")

            handler = logging.StreamHandler(sys.stdout)
            formater = logging.Formatter(Logger.FORMAT, Logger.DATE)
            handler.setFormatter(formater)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

            Logger.instance = logging.getLogger("com.github.bilelmoussaoui.IconRequests")
        return Logger.instance

    @staticmethod
    def warning(msg):
        """Log warning message."""
        Logger.get_default().warning(msg)

    @staticmethod
    def debug(msg):
        """Log debug message."""
        Logger.get_default().debug(msg)

    @staticmethod
    def info(msg):
        """Log info message."""
        Logger.get_default().info(msg)

    @staticmethod
    def error(msg):
        """Log error message."""
        Logger.get_default().error(msg)
