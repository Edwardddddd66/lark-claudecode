"""按天切分日志：把 stdout/stderr 重定向到 TimedRotatingFileHandler。

在 main.py 最早调用（早于其它库 import），确保所有输出都进轮转文件。
每天午夜切一个新文件（旧文件加 .YYYY-MM-DD 后缀），默认保留最近 14 天。
"""

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler


class _StreamToLogger:
    """让 print()（写 sys.stdout/stderr）的输出进入 logging。"""

    def __init__(self, logger: logging.Logger, level: int):
        self._logger = logger
        self._level = level
        self._buf = ""

    def write(self, msg: str):
        self._buf += msg
        while "\n" in self._buf:
            line, self._buf = self._buf.split("\n", 1)
            if line:
                self._logger.log(self._level, line)

    def flush(self):
        if self._buf.strip():
            self._logger.log(self._level, self._buf.rstrip("\n"))
        self._buf = ""

    def isatty(self) -> bool:
        return False


def setup_logging(bot_name: str, log_dir: str, backup_days: int = 14) -> None:
    os.makedirs(log_dir, exist_ok=True)
    handler = TimedRotatingFileHandler(
        os.path.join(log_dir, f"{bot_name}.log"),
        when="midnight",
        backupCount=backup_days,
        encoding="utf-8",
    )
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%H:%M:%S"))

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)

    sys.stdout = _StreamToLogger(root, logging.INFO)
    sys.stderr = _StreamToLogger(root, logging.ERROR)
