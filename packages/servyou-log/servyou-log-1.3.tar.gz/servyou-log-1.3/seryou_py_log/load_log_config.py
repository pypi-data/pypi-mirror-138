import time
import sys
import importlib
import socket
import multiprocessing
import traceback

from pathlib import Path
from shutil import copyfile

from seryou_py_log.pring_tools import stdout_write, stderr_write
from seryou_py_log import log_config


def is_main_process():
    """
    当前进程是否是主进程
    :return:
    """
    return multiprocessing.process.current_process().name == 'MainProcess'


def get_host_ip() -> tuple:
    """
    get machine name info
    :return:
    """
    ip = ''
    host_name = ''
    try:
        sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sc.connect(('8.8.8.8', 80))
        ip = sc.getsockname()[0]
        host_name = socket.gethostname()
        sc.close()
    except Exception:
        pass
    return ip, host_name


def exec_load_log_config(config_path: str = None):
    """
    加载日志模块配置
    :param config_path: log config file abs path
    :return:
    """
    try:
        default_module = importlib.import_module('log_config')
        if config_path:
            config_module = importlib.import_module(config_path)
        else:
            config_module = default_module
        importlib.reload(config_module)
        for var_name, var_value in config_module.__dict__.items():
            if var_name.isupper():
                setattr(default_module, var_name, var_value)
    except ModuleNotFoundError:
        print(traceback.format_exc())
        auto_create_config_file_to_project_root_path()
        stdout_write(f'{time.strftime("%H:%M:%S")} \n \033[0m')
    return True


def auto_create_config_file_to_project_root_path():
    """
    配置文件加载失败后，生成默认配置文件2 Project Root Path
    :return:
    """
    if Path(sys.path[1]).as_posix() == Path(__file__).parent.absolute().as_posix():
        servyou_print('当前路径不可创建配置文件')
        return None
    copyfile(Path(__file__).parent / Path('log_config.py'), Path(sys.path[1]) / Path('log_config.py'))
    return True


def servyou_print(*args, sep=' ', end='\n', file=None):
    """
    复写print
    :param args:
    :param sep:
    :param end:
    :param file:
    :return:
    """
    args = (str(arg) for arg in args)
    if file == sys.stderr:
        # 标准错误 保持原始的红色错误方式，不希望转成蓝色
        stderr_write(sep.join(args))
    else:
        # 获取被调用函数在被调用时所处代码行数
        line = sys._getframe().f_back.f_lineno
        # 获取被调用函数所在模块文件名
        file_name = sys._getframe(1).f_code.co_filename
        stdout_write(
            f'\033[0;34m{time.strftime("%Y-%m-%d %H:%M:%S")} {file_name}:{line}   {sep.join(args)} {end} \033[0m')
    return True


exec_load_log_config()
