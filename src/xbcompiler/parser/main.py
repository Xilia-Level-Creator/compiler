"""XLA format parser for XBCompiler"""

from loguru import logger

logger = logger.opt(colors=True)


def parse(files: list):
    """Parse a given set of files"""
    logger.debug("Got a set of XLA files to parse")

    return str(files)
