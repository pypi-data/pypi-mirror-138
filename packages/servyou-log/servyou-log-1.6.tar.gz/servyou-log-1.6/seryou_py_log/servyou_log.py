import copy
import os
import sys
import typing
import logging
import threading
import multiprocessing
from functools import lru_cache

from pathlib import Path

from seryou_py_log import log_config
from seryou_py_log.load_log_config import servyou_print, get_host_ip
from seryou_py_log.handlers import (ColorHandler, FileHandlerWithBufferWindwos, FileHandlerWithBufferLinux,
                                    ConcurrentRotatingFileHandler, DayRotatingFileHandler,
                                    ConcurrentRotatingFileHandlerWithBufferInitiativeLinux
                                    )

OS_NAME = os.name


class ServyouLog(object):
    """
    一个日志管理类，用于创建logger、添加handler
    """
    logger_name_list = []
    logger_list = []
    preset_name_level_map = dict()
    _unique_lock = threading.Lock()
    _unique = None

    def __init__(self, logger_name: typing.Union[str, None] = None):
        """
        :param logger_name
        """
        if logger_name in (None, '', 'root') and multiprocessing.process.current_process().name == 'MainProcess':
            logger_name = log_config.LOG_NAME
        self._logger_name = logger_name
        self.preset_name_level_map[logger_name] = 1
        self.logger = logging.getLogger(logger_name)

    def __new__(cls, *args, **kwargs):
        if ServyouLog._unique is None or (args and args[0] not in cls.preset_name_level_map):
            with ServyouLog._unique_lock:
                ServyouLog._unique = object.__new__(cls)
        return ServyouLog._unique

    def preset_log_level(self, log_level_int=20):
        """
        提前设置锁定日志级别，当之后再设置该命名空间日志的级别的时候，按照提前预设的级别，无视之后设定的级别。
        主要是针对动态初始化的日志，在生成日志之后再去设置日志级别不方便。
        :param log_level_int:
        :return:
        """
        self.preset_name_level_map[self._logger_name] = log_level_int

    def get_logger_and_add_handlers(self, log_level_int: int = None, *, is_add_stream_handler=True,
                                    do_not_use_color_handler=None, log_path=None,
                                    log_file_size: int = None,
                                    log_file_handler_type: int = None,
                                    formatter_template: typing.Union[int, logging.Formatter] = None):
        """
       :param log_level_int: 日志输出级别，设置为0 10 20 30 40 50，分别对应原生logging.DEBUG(10)，logging.INFO(20)，logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别
       :param is_add_stream_handler: 是否打印日志到控制台
       :param do_not_use_color_handler :是否禁止使用color彩色日志
       :param log_path: 设置存放日志的文件夹路径,如果不设置，则取默认配置
       :param log_file_size :日志大小，单位M，默认100M
       :param log_file_handler_type :这个值可以设置为1 2 3
              1）为使用多进程安全按日志文件大小切割的文件日志
              2）为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个日志
              3）为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题)
       :param formatter_template :日志模板，如果为数字，则为nb_log_config.py字典formatter_dict的键对应的模板，
                                1为formatter_dict的详细模板，2为简要模板,5为最好模板。
                                如果为logging.Formatter对象，则直接使用用户传入的模板。
       """
        if log_level_int is None:
            log_level_int = log_config.LOG_LEVEL_FILTER
        if do_not_use_color_handler is None:
            do_not_use_color_handler = not log_config.DEFAULUT_USE_COLOR_HANDLER
        log_filename = self._logger_name
        if log_config.LOG_NAME:
            log_filename = log_config.LOG_NAME
        if log_file_size is None:
            log_file_size = log_config.LOG_FILE_SIZE
        if log_path is None:
            log_path = log_config.LOG_ENV_PATH.get(log_config.ENV, Path(sys.path[1]).as_posix())
        if formatter_template is None:
            formatter_template = log_config.FORMATTER_STYLE_CODE
        self._logger_level = log_level_int * 10 if log_level_int < 10 else log_level_int
        assert self._logger_level in [0, 10, 20, 30, 40, 50], ValueError("日志等级错误")
        self._is_add_stream_handler = is_add_stream_handler
        self._do_not_use_color_handler = do_not_use_color_handler
        self._log_path = log_path
        self._log_filename = log_filename
        self._log_file_size = log_file_size
        assert log_file_handler_type in (None, 1, 2, 3), ValueError("LOG_FILE_HANDLER_TYPE配置只可为 1 2 3")
        self._log_file_handler_type = log_file_handler_type or log_config.LOG_FILE_HANDLER_TYPE
        if isinstance(formatter_template, int):
            if formatter_template not in log_config.FORMATTER_TEMPLATE_DEMO.keys():
                raise ValueError("FORMATTER_STYLE_CODE日志模板样式配置必须在模板序列中选择")
            self._formatter = log_config.FORMATTER_TEMPLATE_DEMO[formatter_template]
        elif isinstance(formatter_template, str):
            self._formatter = formatter_template
        else:
            raise ValueError('设置的 formatter_template 不正确')
        self.logger.setLevel(self._logger_level)
        self.__add_handlers()
        return self.logger

    def look_over_all_handlers(self):
        """
        pring  current  all handlers
        :return:
        """
        servyou_print(f'当前logName:{self._logger_name},当前logHandlers是: {self.logger.handlers}')

    def remove_all_handlers(self):
        """
        clear current handlers
        :return:
        """
        for hd in self.logger.handlers:
            self.logger.removeHandler(hd)

    def remove_handler_by_handler_class(self, handler_class: type):
        """
        remove handlers by type
        :param handler_class:logging.StreamHandler,ColorHandler,MongoHandler,ConcurrentRotatingFileHandler,MongoHandler,CompatibleSMTPSSLHandler的一种
        :return:
        """
        assert handler_class in [logging.StreamHandler, ColorHandler, ConcurrentRotatingFileHandler], TypeError(
            '设置的handler类型不正确')
        for handler in self.logger.handlers:
            if isinstance(handler, handler_class):
                self.logger.removeHandler(handler)

    def __add_a_hanlder(self, handlerx: logging.Handler):
        """
        add noe log header
        :param handlerx:
        :return:
        """
        handlerx.setLevel(self._logger_level)
        c_computer_id, c_computer_name = get_host_ip()
        log_pattern = self._formatter.replace('%(computer_ip)', c_computer_id).replace('%(computer_name)',
                                                                                       c_computer_name)
        handlerx.setFormatter(logging.Formatter(log_pattern))
        self.logger.addHandler(handlerx)

    def _judge_logger_has_handler_type(self, handler_type: type):
        for hr in self.logger.handlers:
            if isinstance(hr, handler_type):
                return True

    def __add_handlers(self):
        """
        register log handlers
        :return:
        """
        #  不写日志文件， 默认控制台打印：
        if not log_config.DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE:
            self.__add_a_hanlder(logging.StreamHandler())
            return True
        # register添加控制台日志
        if not (self._judge_logger_has_handler_type(ColorHandler) or self._judge_logger_has_handler_type(
                logging.StreamHandler)) and self._is_add_stream_handler:
            handler = ColorHandler() if not self._do_not_use_color_handler else logging.StreamHandler()
            self.__add_a_hanlder(handler)

        # register 添加多进程安全切片的文件日志
        if not (self._judge_logger_has_handler_type(ConcurrentRotatingFileHandler) or
                self._judge_logger_has_handler_type(FileHandlerWithBufferWindwos) or
                self._judge_logger_has_handler_type(FileHandlerWithBufferLinux) or
                self._judge_logger_has_handler_type(ConcurrentRotatingFileHandlerWithBufferInitiativeLinux) or
                self._judge_logger_has_handler_type(DayRotatingFileHandler) or
                self._judge_logger_has_handler_type(logging.FileHandler) or
                self._judge_logger_has_handler_type(ConcurrentRotatingFileHandler)) and all(
            [self._log_path, self._log_filename]):
            if not os.path.exists(self._log_path):
                os.makedirs(self._log_path)
            log_file = f'{os.path.join(self._log_path, self._log_filename)}.log'
            servyou_print(f"logFilePath:{log_file}")
            file_handler = None
            # 日志文件大小切割
            if self._log_file_handler_type == 1:
                if OS_NAME == 'nt':
                    # 在win下使用这个ConcurrentRotatingFileHandler可以解决多进程安全切片，但性能损失惨重。
                    # 10进程各自写入10万条记录到同一个文件消耗15分钟。比不切片写入速度降低100倍。
                    file_handler = FileHandlerWithBufferWindwos(log_file,
                                                                maxBytes=self._log_file_size * 1024 * 1024,
                                                                backupCount=log_config.LOG_FILE_BACKUP_COUNT,
                                                                encoding="utf-8")
                elif OS_NAME == 'posix':
                    # linux下可以使用ConcurrentRotatingFileHandler，进程安全的日志方式。
                    # 10进程各自写入10万条记录到同一个文件消耗100秒，还是比不切片写入速度降低10倍。因为每次检查切片大小和文件锁的原因。
                    file_handler = FileHandlerWithBufferLinux(log_file,
                                                              maxBytes=self._log_file_size * 1024 * 1024,
                                                              backupCount=log_config.LOG_FILE_BACKUP_COUNT,
                                                              encoding="utf-8")

            # 多进程安全按天自动切割的文件
            elif self._log_file_handler_type == 2:
                file_handler = DayRotatingFileHandler(self._log_filename, self._log_path,
                                                      back_count=log_config.LOG_FILE_BACKUP_COUNT)
            # 为不自动切割
            elif self._log_file_handler_type == 3:
                file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            self.__add_a_hanlder(file_handler)


@lru_cache()  # LogManager 本身也支持无限实例化
def get_logger(name: typing.Union[str, None], *, log_level_int: int = None,
               is_add_stream_handler=True,
               do_not_use_color_handler=None, log_path=None,
               log_file_size: int = None,
               log_file_handler_type: int = None,
               formatter_template: typing.Union[int, logging.Formatter] = None) -> logging.Logger:
    locals_copy = copy.copy(locals())
    locals_copy.pop('name')
    return ServyouLog(name).get_logger_and_add_handlers(**locals_copy)
