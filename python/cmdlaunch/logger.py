import logging

_LOGGER_NAME = "cmdlaunch"
_LOG_FORMAT = "[%(name)s] [%(levelname)s] [%(asctime)s] %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_tool_logger() -> logging.Logger:
    """ツール用loggerの取得"""
    logger = logging.getLogger(_LOGGER_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger
