import os
import sys
import time
import threading
from enum import IntEnum


class Severity(IntEnum):
    """消息严重性(枚举)
    """

    def __new__(cls, value, phrase, description=""):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.phrase = phrase
        obj.description = description

        return obj

    Debug = 1, "Debug", "Debug"
    Info = 1 << 1, "Info", "Info."
    Warning = 1 << 2, "Warning", "Warning"
    Error = 1 << 3, "Error", "Error"
    Critical = 1 << 3, "Critical", "Critical"


class Logging(object):
    """日志输出简单实现
    """

    def __init__(self):
        self._level = Severity.Info
        self._writer = StreamWriter()

    def debug(self, msg, *args):
        self._write(Severity.Debug, msg, *args)

    def info(self, msg, *args):
        self._write(Severity.Info, msg, *args)

    def warning(self, msg, *args):
        self._write(Severity.Warning, msg, *args)

    def error(self, msg, *args):
        self._write(Severity.Error, msg, *args)

    def critical(self, msg, *args):
        self._write(Severity.Critical, msg, *args)

    def set_level(self, level):
        self._level = level

    def set_writer(self, writer):
        self._writer = writer

    def set_format(self, format):
        self._writer.set_format(format)

    def close(self):
        self._writer.close()

    def _write(self, level, msg, *args):
        if self._check_severity(level) is True:
            self._writer.write(level, msg % args)

    def _check_severity(self, level):
        return self._level <= level


class Writer(object):
    """Writer基类
    """

    def __init__(self):
        self._format = None
        self._date_format = "%Y%m%d"
        self._lock = threading.RLock()

    def set_format(self, format):
        self._format = format

    def acquire(self):
        self._lock.acquire()

    def release(self):
        self._lock.release()

    def format(self, level, msg):
        return (
            self._format
            % {
                "level": level.phrase,
                "time": time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(time.time())
                ),
                "message": msg,
            }
            if self._format
            else msg
        )

    def write(self, level, msg):
        try:
            self.acquire()
            self._write(level, msg)
        finally:
            self.release()

    def close(self):
        pass

    def _write(self, level, msg):
        raise NotImplemented()


class StreamWriter(Writer):
    """将消息输出到sys.stderr的writer
    """

    def __init__(self):
        super(StreamWriter, self).__init__()
        self._output = None

    def _get_output(self):
        if self._output is None:
            self._output = sys.stderr

        return self._output

    def _write(self, level, msg):
        output = self._get_output()
        output.write(self.format(level, msg))
        output.write(os.linesep)
        self.flush()

    def flush(self):
        if self._output and hasattr(self._output, "flush"):
            self._output.flush()


class FileWriter(StreamWriter):
    """将消息输出到文件的writer
    """

    def __init__(self, file_name):
        super(FileWriter, self).__init__()
        self._file_name = file_name

    def _get_file_name(self):
        dir_name = os.path.dirname(self._file_name)
        base_name = os.path.basename(self._file_name)
        name_parts = list(os.path.splitext(base_name))
        name_parts.insert(1, ".")
        name_parts.insert(
            2, time.strftime(self._date_format, time.localtime(time.time())),
        )

        return os.path.join(dir_name, "".join(name_parts))

    def _get_output(self):
        if self._output is None:
            self._output = open(self._get_file_name(), "a",)

        return self._output

    def close(self):
        if self._output and hasattr(self._output, "close"):
            self._output.close()


class LogFeature(Logging):
    """PVM的日志功能插件
    """

    def __init__(self):
        super(LogFeature, self).__init__()
        self._enabled = False

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def _write(self, level, msg, *args):
        if self._enabled:
            super(LogFeature, self)._write(level, msg, *args)
