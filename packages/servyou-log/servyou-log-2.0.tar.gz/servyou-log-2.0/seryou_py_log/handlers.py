import atexit
import queue
import re
import sys
import os
import time
import copy
import traceback

import logging

from pathlib import Path
from queue import Queue, Empty
from threading import Lock, Thread
from concurrent_log_handler import ConcurrentRotatingFileHandler

from seryou_py_log import servyou_print, FileLock

os_name = os.name


class ColorHandler(logging.Handler):
    """
    根据日志严重级别，显示成五彩控制台日志。
    强烈建议使用pycharm的 monokai主题颜色，这样日志的颜色符合常规的交通信号灯颜色指示，色彩也非常饱和鲜艳。
    设置方式为 打开pycharm的settings -> Editor -> Color Scheme -> Console Font 选择monokai
    """

    terminator = '\r\n' if os_name == 'nt' else '\n'
    bule = 96 if os_name == 'nt' else 36
    yellow = 93 if os_name == 'nt' else 33

    def __init__(self, stream=None):
        """
        Initialize the handler.

        If stream is not specified, sys.stderr is used.
        """
        logging.Handler.__init__(self)
        if stream is None:
            stream = sys.stdout
        self.stream = stream
        self._display_method = 7 if os_name == 'posix' else 0

    def flush(self):
        """
        Flushes the stream.
        """
        self.acquire()
        try:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()
        finally:
            self.release()

    def __build_color_msg_with_no_backgroud_color(self, record_level, record_copy: logging.LogRecord, ):
        complete_msg = self.format(record_copy)
        if record_level == 10:
            # msg_color = ('\033[0;32m%s\033[0m' % msg)  # 绿色
            # print(msg1)
            msg_color = f'\033[0;32m{complete_msg}\033[0m'  # 绿色
        elif record_level == 20:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.bule, msg))  # 青蓝色 36    96
            msg_color = f'\033[0;36m{complete_msg}\033[0m'
        elif record_level == 30:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.yellow, msg))
            msg_color = f'\033[0;33m{complete_msg}\033[0m'
        elif record_level == 40:
            # msg_color = ('\033[%s;35m%s\033[0m' % (self._display_method, msg))  # 紫红色
            msg_color = f'\033[0;31m{complete_msg}\033[0m'
        elif record_level == 50:
            # msg_color = ('\033[%s;31m%s\033[0m' % (self._display_method, msg))  # 血红色
            msg_color = f'\033[0;31m{complete_msg}\033[0m'
        else:
            msg_color = f'{complete_msg}'
        return msg_color

    @staticmethod
    def __spilt_msg(log_level, msg: str):
        split_text = '- 级别 -'
        if log_level == 10:
            split_text = '- DEBUG -'
        elif log_level == 20:
            split_text = '- INFO -'
        elif log_level == 30:
            split_text = '- WARNING -'
        elif log_level == 40:
            split_text = '- ERROR -'
        elif log_level == 50:
            split_text = '- CRITICAL -'
        msg_split = msg.split(split_text, maxsplit=1)
        return msg_split[0] + split_text, msg_split[-1]

    def __repr__(self):
        level = logging.getLevelName(self.level)
        name = getattr(self.stream, 'name', '')
        if name:
            name += ' '
        return '<%s %s(%s)>' % (self.__class__.__name__, name, level)

    def emit(self, record: logging.LogRecord):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        # noinspection PyBroadException
        try:
            # very_nb_print(record)
            # record.message = record.getMessage()
            # effective_information_msg = record.getMessage()  # 不能用msg字段，例如有的包的日志格式化还有其他字段
            # record_copy = copy.copy(record)  # copy是因为，不要因为要屏幕彩色日志而影响例如文件日志 叮叮日志等其他handler的格式。
            # record_copy.for_segmentation_color = '彩色分段标志属性而已'
            # del record_copy.msg
            # assist_msg = self.format(record_copy)
            # print(f'**  {assist_msg}  ** ')
            stream = self.stream

            msg_color = self.__build_color_msg_with_no_backgroud_color(record.levelno, copy.copy(record))
            # stream.write(msg_color)
            # stream.write(self.terminator)
            # self.flush()
            stream.write(msg_color + self.terminator)
            # self.flush()
        except Exception as e:
            servyou_print(e)
            servyou_print(traceback.format_exc())
            # self.handleError(record)


class FileHandlerWithBufferWindwos(ConcurrentRotatingFileHandler):
    """
     解决了多进程下文件切片问题，但频繁操作文件锁，带来程序性能巨大下降。
    """
    file_handler_list = []
    # 只能在windwos运行正常，windwos是多进程每个进程的变量has_start_emit_all_file_handler是独立的。linux是共享的。
    has_start_emit_all_file_handler = False

    @classmethod
    def _emit_all_file_handler(cls):
        while True:
            for hr in cls.file_handler_list:
                hr.rollover_and_do_write()
            time.sleep(1)

    @classmethod
    def start_emit_all_file_handler(cls):
        Thread(target=cls._emit_all_file_handler, daemon=True).start()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer_msgs_queue = Queue()
        # 如果程序属于立马就能结束的，需要在程序结束前执行这个钩子，防止不到最后一秒的日志没记录到。
        atexit.register(self._when_exit)
        self.file_handler_list.append(self)
        if not self.has_start_emit_all_file_handler:
            self.start_emit_all_file_handler()
            self.__class__.has_start_emit_all_file_handler = True

    def _when_exit(self):
        self.rollover_and_do_write()

    def emit(self, record):
        """
        emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
        :param record:
        :return:
        """
        try:
            msg = self.format(record)
            self.buffer_msgs_queue.put(msg)
        except Exception:
            self.handleError(record)

    def rollover_and_do_write(self, ):
        self._rollover_and_do_write()

    def _rollover_and_do_write(self):
        buffer_msgs = ''
        while True:
            try:
                msg = self.buffer_msgs_queue.get(block=False)
                buffer_msgs += msg + '\n'
            except Empty:
                break
        if buffer_msgs:
            try:
                self._do_lock()
                try:
                    if self.shouldRollover(None):
                        self.doRollover()
                except Exception as e:
                    self._console_log("Unable to do rollover: %s" % (e,), stack=True)
                self.do_write(buffer_msgs)
            finally:
                self._do_unlock()


FileHandlerWithBufferLinux = ConcurrentRotatingFileHandler


class DayRotatingFileHandler(logging.Handler):
    """
    这个多进程按时间切片安全的。
    官方的 TimedRotatingFileHandler 在多进程下疯狂报错，
    """
    file_handler_list = []
    has_start_emit_all_file_handler_process_id_set = set()
    __lock_for_rotate = Lock()

    @classmethod
    def _emit_all_file_handler(cls):
        while True:
            for hr in cls.file_handler_list:
                hr._write_to_file()
            #  每隔一秒钟批量写入一次
            time.sleep(1)

    @classmethod
    def _start_emit_all_file_handler(cls):
        Thread(target=cls._emit_all_file_handler, daemon=True).start()

    def __init__(self, file_name: str, file_path: str, back_count=10):
        super().__init__()
        self.file_name = file_name
        self.file_path = file_path
        self.backupCount = back_count
        self.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self.extMatch2 = re.compile(r"^\d{2}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self._last_delete_time = time.time()

        self.buffer_msgs_queue = queue.Queue()
        atexit.register(self._write_to_file)
        self.file_handler_list.append(self)
        if os.getpid() not in self.has_start_emit_all_file_handler_process_id_set:
            self._start_emit_all_file_handler()
            self.__class__.has_start_emit_all_file_handler_process_id_set.add(os.getpid())

    def emit(self, record: logging.LogRecord):
        """
        emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            self.buffer_msgs_queue.put(msg)
        except Exception:
            self.handleError(record)
        try:
            servyou_print(str(self.format(record)))
        except:
            pass

    def _write_to_file(self):
        buffer_msgs = ''
        while True:
            try:
                msg = self.buffer_msgs_queue.get(block=False)
                buffer_msgs += msg + '\n'
            except queue.Empty:
                break
        if buffer_msgs:
            with FileLock(self.file_path / Path(f'_delete_{self.file_name}.lock')):
                time_str = time.strftime('%Y-%m-%d')
                new_file_name = self.file_name + '.' + time_str
                path_obj = Path(self.file_path) / Path(new_file_name)
                path_obj.touch(exist_ok=True)
                with path_obj.open(mode='a') as f:
                    f.write(buffer_msgs)
                if time.time() - self._last_delete_time > 60:
                    self._find_and_delete_files()
                    self._last_delete_time = time.time()

    def _find_and_delete_files(self):
        """
        这一段命名不规范是复制原来的官方旧代码。
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName = self.file_path
        baseName = self.file_name
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                # print(fileName, prefix,suffix)
                if self.extMatch.match(suffix) or self.extMatch2.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        for r in result:
            Path(r).unlink()
