import sys


def stdout_write(msg: str):
    """
    :param msg:
    :return:
    """
    sys.stdout.write(msg)
    sys.stdout.flush()
    return True


def stderr_write(msg: str):
    sys.stderr.write(msg)
    sys.stderr.flush()
    return True
