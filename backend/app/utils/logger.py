import logging
import sys
from pathlib import Path

from fastapi import Request
from utils.config import get_config

config = get_config()

def get_logger(
    name: str = "app",
    logdir: Path = Path(config["logdir"]),
    log_level: int = logging.INFO,
) -> logging.Logger:
    """Setup a logger with file and stream handlers.

    Args:
        name (str, optional): name of logger. Defaults to "app".

        logdir (Path | str, optional): folder where log files will
        be stored. Defaults to Path(config.logdir).

        log_level (int, optional): log level. Defaults to logging.INFO.

    Returns:
        logging.Logger: logger object
    """

    logdir = Path(logdir)
    logdir.mkdir(parents=True, exist_ok=True)
    path = logdir / name

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)s %(funcName)s(%(lineno)d) %(message)s"
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(
        filename=path.with_suffix(".log"),
        mode="a",
        encoding="utf-8",
    )

    file_handler.setLevel(log_level)
    stream_handler.setLevel(log_level)

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger


def log_request(request: Request, logger: logging.Logger) -> None:
    s = "Request validation error:\n"
    s += "ULR: %s\n"
    s += "Path params: %s\n"
    s += "Query params: %s\n"
    s += "Headers: %s\n"
    logger.error(
        s
        % (
            request.url,
            request.path_params,
            request.query_params,
            request.headers,
        ),
    )
