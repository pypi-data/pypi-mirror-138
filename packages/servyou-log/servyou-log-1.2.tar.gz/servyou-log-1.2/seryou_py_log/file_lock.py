import os
import abc

# 根据os导包
if os.name == 'nt':
    import win32con
    import win32file
    import pywintypes

    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    # The default value
    LOCK_SH = 0
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    _overlapped = pywintypes.OVERLAPPED()
else:
    import fcntl


class BaseLock(metaclass=abc.ABCMeta):
    def __init__(self, lock_file_path: str):
        self.file_path = open(lock_file_path, 'a')

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplemented

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplemented


class WindowsFileLock(BaseLock):
    """
    windows os file lock
    """

    def __enter__(self):
        # 文件描述符
        self.hfile = win32file._get_osfhandle(self.file_path.fileno())
        win32file.LockFileEx(self.hfile, LOCK_EX, 0, 0xffff0000, _overlapped)

    def __exit__(self, exc_type, exc_val, exc_tb):
        win32file.UnlockFileEx(self.hfile, 0, 0xffff0000, _overlapped)


class LinuxFileLock(BaseLock):
    """
        linux os file lock
    """

    def __enter__(self):
        fcntl.flock(self.file_path, fcntl.LOCK_EX)

    def __exit__(self, exc_type, exc_val, exc_tb):
        fcntl.flock(self.file_path, fcntl.LOCK_UN)


FileLock = WindowsFileLock if os.name == 'nt' else LinuxFileLock
