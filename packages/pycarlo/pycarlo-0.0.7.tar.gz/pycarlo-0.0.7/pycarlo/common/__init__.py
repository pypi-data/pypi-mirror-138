import logging

from pycarlo.common.settings import MCD_VERBOSE_ERRORS


def get_logger(name: str) -> logging:
    """
    Returns a logger with the specified name.

    :param name: Name of the logger.
    """

    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if MCD_VERBOSE_ERRORS else logging.CRITICAL)
    return logger
