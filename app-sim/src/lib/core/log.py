#!/usr/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: log.py
#         Desc: 日志系统
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2016-05-24 10:03:44
#      History:
#=============================================================================
'''
import sys
import logging
import ConfigParser
from logging.handlers import RotatingFileHandler

from lib.core.enum import SYS
from lib.core.cmdLine import cmdLineParser

class ColorFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.WARNING:
            record.msg = '\033[93m%s\033[0m' % record.msg
        elif record.levelno == logging.ERROR:
            record.msg = '\033[91m%s\033[0m' % record.msg
        elif record.levelno == logging.DEBUG:
            record.msg = '\033[92ms%s\033[0m' % record.msg

        return logging.Formatter.format(self, record)


try:
    conf = ConfigParser.ConfigParser()
    conf.read(SYS.CONF_FILE)

    LEVEL = int(conf.get("LOG","Level"))
    TYPE = int(conf.get("LOG","Type"))
    DATA_TYPE = conf.get("LOG","Date")
    MAXBYTES = int(conf.get("LOG","MaxBytes"))
    BACKUPCOUNT = int(conf.get("LOG","BackupCount"))
    APP = (conf.get("APP","name"))
except:
    LEVEL = 0
    TYPE = 0
    DATA_TYPE = "%Y%m%d%H%M%S"
    MAXBYTES = 104857600 * 5	#500M
    BACKUPCOUNT = 5

#-------------------------------
SYS.RUN_MODULE = TYPE
SYS.APP = APP.split(',') 
for tmp in SYS.APP:
    if len(tmp.rstrip().lstrip()) == 0:
        SYS.APP.remove(tmp)
#判断是否为命令行提供启动参数
cmdLineParser()
#-------------------------------

log_format = "%(asctime)s,%(process)d,%(levelname)s > %(message)s"
time_format = DATA_TYPE
FORMAT = ColorFormatter(log_format,datefmt=time_format)


#FORMAT = logging.Formatter("%(asctime)s,%(process)d,%(levelname)s > %(message)s",DATA_TYPE)
LOG_NAME = SYS.LOG_FILE

LOGGER = logging.getLogger(LOG_NAME)
LOGGER.setLevel(LEVEL)
LOGGER_HANDLER = RotatingFileHandler(
    filename        = LOG_NAME,
    maxBytes        = MAXBYTES,
    backupCount     = BACKUPCOUNT,
    mode    ='a'
)
LOGGER_HANDLER.setFormatter(FORMAT)
LOGGER_HANDLER.setLevel(LEVEL)
LOGGER.addHandler(LOGGER_HANDLER)

if SYS.RUN_MODULE >=1:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
    LOGGER_HANDLER.setFormatter(FORMAT)
    LOGGER.addHandler(LOGGER_HANDLER)



