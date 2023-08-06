#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: LiangChao
@email：liangchao@noboauto.com
@desc: 
"""
import atexit
import io
import multiprocessing
import os
import socket
import sys
import threading
import traceback
from abc import ABC
from datetime import datetime
from typing import List, Optional

from logzero.colors import Fore
from makit.lib import fn
from makit.lib._serialize import serialize
from makit.lib.const import DEFAULT_TIME_FORMAT
from makit.lib.errors import NotSupportError
from makit.lib.fn import CallInfo

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


class Level:
    """
    日志级别
    """

    def __init__(self, name: str, code: int, color=None):
        self.name = name
        self.code = code
        self.color = color
        self.instance: Optional[Logger] = None

    def __set__(self, instance, value):
        raise LoggingError('Can not change level!')

    def __get__(self, instance, owner):
        self.instance = instance
        return self

    def __call__(self, message, *args, **kwargs):
        if self.code <= 0:
            raise LoggingError(f'Level {self.name} is not callable!')  # TODO return?
        self.instance.log(self, message, *args, **kwargs)

    def __repr__(self):
        return f'<LogLevel {self.name} {self.code}>'


class Record:
    def __init__(self, message, level: Level, caller: CallInfo, stack_info=None, *args, **kwargs):
        self.message = str(message)
        self.level_name = level.name
        self.level_code = level.code
        self._caller = caller
        self.func_name = caller.func_name
        self.lineno = caller.lineno
        self.filepath = caller.filename
        self.filename = os.path.basename(caller.filename)
        self.time = datetime.now()
        self.color = level.color
        self.thread = threading.get_ident()
        self.thread_name = threading.current_thread().name
        self.process = os.getpid()
        self.process_name = multiprocessing.current_process().name
        self.stack_info = stack_info
        if args:
            self.message = self.message.format(*args)
        if kwargs:
            self.message = self.message.format(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)


class LogProcessor:
    """
    日志加工器，用于统一对日志进行加工处理，便于后续消费。在有些情况下，不同的程序阶段对日志有不同的要求，需要在日志信息中插入当前阶段相关的数据
    """

    def handle(self, record):
        raise NotImplementedError


class LogConsumer:
    """
    日志消费者，消费者不对日志记录做任何修改处理
    """

    def format(self, record):
        raise NotImplementedError


class Filter:
    def filter(self, record):
        raise NotImplementedError


_loggers = []


class Logger:
    """

    """
    debug = Level(name='DEBUG', code=DEBUG, color=Fore.CYAN)
    info = Level(name='INFO', code=INFO, color=Fore.GREEN)
    warning = Level(name='WARNING', code=WARNING, color=Fore.YELLOW)
    warn = warning
    error = Level(name='ERROR', code=ERROR, color=Fore.RED)
    critical = Level(name='CRITICAL', code=CRITICAL, color=Fore.RED)
    fatal = critical

    def __init__(self, level=0, propagate=True):
        self.level = level
        self.handlers: List[Handler] = []
        self._lock = threading.Lock()
        self._parent = None
        self.propagate = propagate  # 是否向上传递
        self.disabled = False
        _loggers.append(self)
        self._processors = []  # 日志加工器

    @property
    def parent(self):
        if not self._parent:
            return logger
        return self._parent

    def add_handler(self, handler):
        with self._lock:
            if handler not in self.handlers:
                self.handlers.append(handler)

    def remove_handler(self, handler):
        with self._lock:
            self.handlers.remove(handler)

    def handle(self, record):
        if self.is_enabled_for(record.level_code):
            for handler in self.handlers:
                if record.level_code >= handler.level:
                    handler.handle(record)
        if self.propagate and self.parent != self:  # 避免logger回调自身
            self.parent.handle(record)

    def sub(self, level, propagate=True):
        sub = self.__class__(level, propagate=propagate)
        sub._parent = self
        return sub

    def is_enabled_for(self, level):
        return not self.disabled and self.level <= level

    def exception(self, message, *args, **kwargs):
        self.log(self.error, message, *args, log_stack=True, **kwargs)

    def log(self, level: Level, message, *args, log_stack=False, invoked_file=None, **kwargs):
        if self.disabled:
            return
        c = fn.parse_caller(invoked_file=invoked_file or __file__)
        if log_stack:
            e_type, e, tb = sys.exc_info()
            if e:
                stack_info = traceback.format_tb(tb)
                stack_info.insert(0, 'Traceback (most recent call last):\n')
                stack_info.append(f'{e_type.__name__}: {e}')
            else:
                stack_info = c.get_stack()
        else:
            stack_info = None
        record = Record(message, level, c, stack_info=stack_info, *args, **kwargs)
        self.handle(record)

    def write_file(self, filename, level=NOTSET):
        handler = FileHandler(filename, level)
        self.add_handler(handler)
        return handler

    def rotate(self, filename, level=NOTSET, mode='a', encoding=None, errors=None, backup_count=0):
        handler = RotatingFileHandler(filename, level=level, mode=mode, encoding=encoding, errors=errors,
                                      backup_count=backup_count)
        self.add_handler(handler)
        return handler

    def handler(self, level, format):

        def deco(func):
            class DynamicHandler(Handler):
                def emit(self, record):
                    func(record)

            handler = DynamicHandler(level, format=format)
            self.add_handler(handler)

            return func

        return deco

    def exit(self):
        for handler in self.handlers:
            handler.close()


def _exit():
    for logger in _loggers:
        logger.exit()


atexit.register(_exit)


class Handler:

    def __init__(self, level, format=None, time_fmt=None):
        self.level = level
        self._format = format
        self.time_fmt = time_fmt or DEFAULT_TIME_FORMAT

    def format(self, record):
        if not self._format:
            return record
        if callable(self._format):
            return self._format(record)
        elif isinstance(self._format, str):
            record_dict = dict(record.__dict__)
            record_dict['time'] = record.time.strftime(self.time_fmt)
            return self._format.format(**record_dict)
        else:
            raise NotSupportError(self._format)

    def handle(self, record):
        try:
            lines = [self.format(record) + '\n']
            stack_info = record.stack_info
            if stack_info:
                if isinstance(stack_info, str):
                    stack_info = stack_info.splitlines()
                for line in stack_info:
                    lines.extend('  ' + line)
            self.emit(''.join(lines))
        except Exception:
            sys.stderr.write('--- Logging error ---\n')
            stack_info = traceback.format_exc()
            sys.stderr.write(stack_info)
            self.handle_error(record)

    def emit(self, formatted_record):
        raise NotImplementedError

    def handle_error(self, record):
        pass

    def close(self):
        pass


class LockableHandler(Handler, ABC):
    """"""

    def __init__(self, level, format=None, time_fmt=None):
        super().__init__(level, format=format, time_fmt=time_fmt)
        self._lock = threading.RLock()

    def handle(self, record):
        with self._lock:
            super().handle(record)


# COLORED_FORMAT = '{color}[{level:1.1s} {time} {filename}:{line}]{end_color} {message}'
COLORED_FORMAT = '{color}[{level_name:1.1s} {time} {filename}:{lineno}]{end_color} {message}'


class StreamHandler(LockableHandler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a stream. Note that this class does not close the stream, as
    sys.stdout or sys.stderr may be used.
    """

    terminator = '\n'

    def __init__(self, level, stream=None, format=None, time_fmt=None):
        super().__init__(level, format=format, time_fmt=time_fmt)
        self._stream = stream

    @property
    def stream(self):
        if not self._stream:
            self._stream = self._open_stream()
        return self._stream

    @stream.setter
    def stream(self, stream):
        if stream is not self._stream:
            with self._lock:
                self.flush()
                prev_stream, self._stream = self._stream, stream
                if hasattr(prev_stream, "close"):
                    prev_stream.close()

    def emit(self, formatted_record):
        if not self.stream:
            return
        self.stream.write(formatted_record + self.terminator)
        self.flush()

    def _open_stream(self):
        raise NotImplementedError

    def flush(self):
        """
        Flushes the stream.
        """
        with self._lock:
            if self._stream and hasattr(self._stream, "flush"):
                self._stream.flush()

    def close(self):
        """
        Closes the stream.
        """
        with self._lock:
            if not self.stream:
                return
            try:
                self.flush()
            finally:
                stream = self.stream
                self.stream = None
                if hasattr(stream, "close"):
                    stream.close()

    def __del__(self):
        self.close()


class FileHandler(StreamHandler):
    FORMAT = '[{level_name:1.1s} {time} {filename}:{lineno}] {message}'

    def __init__(self, filename, level, mode='a', encoding=None, errors=None, format=FORMAT):
        super().__init__(level, format=format)
        filename = os.fspath(filename)
        self.filename = os.path.abspath(filename)
        self.mode = mode
        self.encoding = encoding
        self.errors = errors

    def _open_stream(self):
        return open(self.filename, self.mode, encoding=self.encoding, errors=self.errors)


class RotatingFileHandler(FileHandler):
    def __init__(self, filename, level=NOTSET, mode='a', encoding=None, errors=None, backup_count=0):
        super().__init__(filename, level, mode, encoding, errors)
        self.mode = mode
        self.encoding = encoding
        self.errors = errors
        self.backup_count = backup_count
        self._log_create_time = None
        self.__cache_files = []
        self._should_rotate = None

    def _open_stream(self):
        self._log_create_time = datetime.now()
        return super()._open_stream()

    def emit(self, record):
        if self._should_rotate and self._should_rotate(record):
            self.rotate()
        super().emit(record)

    def rotate(self):
        """
        Do a rollover, as described in __init__().
        """
        self.stream = None
        if self.backup_count > 0:
            for i in range(self.backup_count - 1, 0, -1):
                sfn = "%s.%d" % (self.filename, i)
                dfn = "%s.%d" % (self.filename, i + 1)
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.filename + ".1"
            if os.path.exists(dfn):
                os.remove(dfn)
            os.rename(self.filename, dfn)

    def rotate_max_bytes(self, max_bytes):
        def should_rotate(record):
            if max_bytes > 0:  # are we rolling over?
                msg = "%s\n" % self.format(record)
                self.stream.seek(0, 2)  # due to non-posix-compliant Windows feature
                if self.stream.tell() + len(msg) >= max_bytes:
                    return 1
            return 0

        self._should_rotate = should_rotate
        return self

    def every_day(self):
        self._should_rotate = lambda r: self._log_create_time and datetime.now().day > self._log_create_time.day
        return self

    def every_week(self):

        def is_next_week():
            now_week = int(datetime.now().strftime("%W"))
            prev_week = int(self._log_create_time.strftime("%W")) if self._log_create_time else -1
            return now_week > prev_week

        self._should_rotate = lambda r: is_next_week()
        return self

    def interval(self, interval):

        class RotateInterval:
            def __init__(self):
                self.seconds = 0

            def days(self, n: int):
                self.seconds = n * 24 * 3600
                return self

            def hours(self, n: int):
                self.seconds = n * 3600
                return self

            def minutes(self, n: int):
                self.seconds = n * 60
                return self

            def __call__(self, record):
                pass

        interval = RotateInterval()
        self._should_rotate = interval
        return interval


class SocketHandler(LockableHandler):
    def __init__(self, level, host, port):
        super().__init__(level)
        self.host = host
        self.port = port
        if port is None:
            self.address = host
        else:
            self.address = (host, port)
        self.sock = None

    def make_socket(self, timeout=1):
        """
        A factory method which allows subclasses to define the precise
        type of socket they want.
        """
        if self.port is not None:
            s = socket.create_connection(self.address, timeout=timeout)
        else:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.settimeout(timeout)
            try:
                s.connect(self.address)
            except OSError:
                s.close()
                raise
        return s

    def send(self, s):
        if self.sock is None:
            self.make_socket()
        if self.sock:
            try:
                self.sock.sendall(s)
            except OSError:
                self.sock.close()
                self.sock = None

    def handle_error(self, record):
        if self.sock:
            self.sock.close()
            self.sock = None  # try to reconnect next time
        else:
            super().handle_error(record)

    def format(self, record):  # TODO
        pass

    def emit(self, formatted_record):
        self.send(formatted_record)

    def close(self):
        with self._lock:
            sock = self.sock
            if sock:
                self.sock = None
                sock.close()
            super().close()


class QueueHandler(Handler):
    def __init__(self, level, queue, format=None):
        super().__init__(level, format=format)
        self.queue = queue

    def enqueue(self, record):
        self.queue.put_nowait(record)

    def emit(self, record):
        self.enqueue(self.format(record))


class TerminalHandler(StreamHandler):

    def format(self, record):
        record_dict = serialize(record)
        record_dict['time'] = record.time.strftime(self.time_fmt)
        record_dict['end_color'] = Fore.RESET
        return self._format.format(**record_dict)

    def _open_stream(self):
        return sys.stderr


# 基础日志对象，只在控制台打印输出，所有日志记录器都会将日志传递给它
logger = Logger()
logger.add_handler(TerminalHandler(0, format=COLORED_FORMAT))


class LoggingError(Exception):
    """"""
