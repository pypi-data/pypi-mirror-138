# Copyright 2022-2027 by Servyou PubDesktop group . All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# 该配置文件均为默认配置，会被具体实例参数覆盖

# TYPE:bool 控制台是否使用有彩的日志
DEFAULUT_USE_COLOR_HANDLER = True
# TYPE:bool 是否同时将日志记录到记log文件中
DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE = True
"""
LOG_FILE_HANDLER_TYPE
日志切片方式, 该配置必须依赖 DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE_HANDLER开启
值可以设置为：
1）为使用多进程安全按日志文件大小切割的文件日志,这是本人实现的批量写入日志，减少操作文件锁次数，测试10进程快速写入文件，win上性能比第5种提高了100倍，linux提升5倍
2）为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个新的日志文件。日志文件名字后缀自动加上日期。
3）为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题) 
"""
LOG_FILE_HANDLER_TYPE = 2

# TYPE:int 单位是M,每个文件的切片大小，超过多少后就自动切割
LOG_FILE_SIZE = 100
# TYPE:int 对同一个日志文件，默认最多备份几个文件，超过就删除了。
LOG_FILE_BACKUP_COUNT = 3
# TYPE:int 默认日志级别
LOG_LEVEL_FILTER = 10

# TYPE:str 默认为dev环境 该env日志文件生成在项目根路径下
ENV = 'dev'
LOG_ENV_PATH = {
    'test': '/usr/local/logs/daqworker/',
    'prod': '/usr/local/logs/daqworker/'
}
# TYPE:str
LOG_NAME = 'servyou_log'

FORMATTER_TEMPLATE_DEMO = {
    1: '[日志时间%(asctime)s][日志名称%(name)s][文件%(filename)s][第%(lineno)d行][日志等级%(levelname)s]日志信息:%(message)s',
    2: '%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s',
    3: '%(asctime)s - %(name)s - [ File "%(pathname)s", line %(lineno)d, in %(funcName)s ] - %(levelname)s - %(message)s',
    4: '%(asctime)s - %(name)s - "%(filename)s" - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s -               File "%(pathname)s", line %(lineno)d ',
    5: '%(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
    6: '%(name)s - %(asctime)-15s - %(filename)s - %(lineno)d - %(levelname)s: %(message)s',
    7: '%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s',
    8: '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
    9: '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s',
    10: '%(computer_ip)s %(computer_name)s-[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s',
    11: '%(asctime)s - [process:%(process)d][%(levelname)s][%(filename)s][line:%(lineno)d]: %(message)s ',

}
# 日志模板 TYPE:str/int
# FORMATTER_STYLE_CODE = FORMATTER_TEMPLATE_DEMO[10]
FORMATTER_STYLE_CODE = 11
