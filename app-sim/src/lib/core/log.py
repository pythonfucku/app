#!/usr/bin/env python
# encoding:utf-8

"""
Author:liangrt
Date:2016-03-30
"""
import sys
import logging
import ConfigParser
from logging.handlers import RotatingFileHandler

from enum import SYS

try:
	conf = ConfigParser.ConfigParser()
	conf.read(SYS.CONF_FILE)

	LEVEL = int(conf.get("LOG","Level"))
	TYPE = int(conf.get("LOG","Type"))
	DATA_TYPE = conf.get("LOG","Date")
	MAXBYTES = int(conf.get("LOG","MaxBytes"))
	BACKUPCOUNT = int(conf.get("LOG","BackupCount"))
except:
	LEVEL = 0
	TYPE = 0
	DATA_TYPE = "%Y%m%d%H%M%S"
	MAXBYTES = 104857600 * 5	#500M
	BACKUPCOUNT = 5

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
	
if type >=1:
	LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
	LOGGER_HANDLER.setFormatter(FORMAT)
	LOGGER.addHandler(LOGGER_HANDLER)





