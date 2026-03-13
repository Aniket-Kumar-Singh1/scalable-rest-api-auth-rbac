"""
Centralised logging utility.

Usage:
    from app.utils.logger import get_logger
    logger = get_logger("module_name")
    logger.info("Hello %s", name)
"""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger with the given name.

    Logs to stdout with a clean format including timestamp, level, and name.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger
