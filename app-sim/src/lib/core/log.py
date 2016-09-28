#!/usr/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: log.py
#         Desc: ��־ϵͳ
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
#�ж��Ƿ�Ϊ�������ṩ��������
cmdLineParser()
#-------------------------------

FORMAT = logging.Formatter("%(asctime)s,%(process)d,%(levelname)s > %(message)s",DATA_TYPE)
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





