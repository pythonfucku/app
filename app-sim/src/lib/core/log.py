#!/usr/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: log.py
#         Desc: 
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2017-01-01 17:53:15
#      History:
#=============================================================================
'''
import sys,logging,ConfigParser
from logging.handlers import RotatingFileHandler
from lib.core.data import asys


class ColorFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.WARNING:
            record.msg = '\033[93m%s\033[0m' % record.msg
        elif record.levelno == logging.ERROR:
            record.msg = '\033[91m%s\033[0m' % record.msg
        elif record.levelno == logging.DEBUG:
            record.msg = '\033[92m%s\033[0m' % record.msg

        return logging.Formatter.format(self, record)


class mylog:
    def __init__(self,log_file_name):
        try:
            conf = ConfigParser.ConfigParser()
            conf.read(asys.CONF_FILE)

            LEVEL       = int(conf.get("LOG","Level"))
            TYPE        = int(conf.get("LOG","Type"))
            DATA_TYPE   = conf.get("LOG","Date")
            MAXBYTES    = int(conf.get("LOG","MaxBytes"))
            BACKUPCOUNT = int(conf.get("LOG","BackupCount"))
            LOG_MODULE  = conf.get("LOG","Log module")
        except:
            LEVEL       = 0
            TYPE        = 0
            DATA_TYPE   = "%Y%m%d%H%M%S"
            MAXBYTES    = 104857600 * 5	#500M
            BACKUPCOUNT = 5
            LOG_MODULE  = "w"

        if LOG_MODULE.upper() == "W":
            MAXBYTES = 0
            BACKUPCOUNT = 0

        format_str = "%(asctime)s,%(process)d,%(levelname)s > %(message)s"
        file_format = logging.Formatter(format_str,DATA_TYPE)
        stdout_format = ColorFormatter(format_str,datefmt=DATA_TYPE)

        LOGGER_HANDLER = RotatingFileHandler(
            filename    = log_file_name,
            maxBytes    = MAXBYTES,
            backupCount = BACKUPCOUNT,
            mode = LOG_MODULE,
        )
        LOGGER_HANDLER.setFormatter(file_format)
        LOGGER_HANDLER.setLevel(LEVEL)


        self.LOGGER = logging.getLogger(log_file_name)
        self.LOGGER.setLevel(LEVEL)
        self.LOGGER.addHandler(LOGGER_HANDLER)

        if TYPE >=1:
            LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
            LOGGER_HANDLER.setFormatter(stdout_format)
            self.LOGGER.addHandler(LOGGER_HANDLER)



