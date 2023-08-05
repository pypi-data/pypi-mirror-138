from enum import Enum
from os import environ


class LogLevel(Enum):
    debug = 0
    info = 1
    warn = 2


def get_log_level():
    raw_level = environ.get("LOG_LEVEL", "WARN").lower()
    return LogLevel[raw_level]


def log(level, msg):
    if level.value < get_log_level().value:
        return
    print(f"[{level.name}] {msg}", flush=True)


def debug(msg):
    log(LogLevel.debug, msg)


def info(msg):
    log(LogLevel.info, msg)


def warn(msg):
    log(LogLevel.warn, msg)
