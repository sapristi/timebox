import logging

from timebox.config import Config


def test_empty_config():
    logger = logging.getLogger("timebox.test.config")
    c = Config()
    logger.setLevel(c.log_level)
