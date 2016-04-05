#!/bin/env python
# encoding utf-8

"""
Author:liangrt
Date:2016-03-30
"""
import os
from data import paths
from exception import AppBaseException
from enum import SYS

def setPaths():
	paths.ROOT_PATH	=SYS.ROOT_PATH
	paths.APP_PATH	= SYS.APP_PATH
	paths.SYSTEM_LOG_PATH	= SYS.LOG_PATH
	paths.SYSTEM_CONF_PATH	= SYS.CONF_PATH

	paths.SYSTEM_CONF	= SYS.CONF_FILE

	for path in paths.values():
		if any(path.endswith(_) for _ in (".txt",".conf",".xml",".zip")):
			checkFile(path)
		
def checkFile(filename):
	valid = True

	if filename is None or not os.path.isfile(filename):
		valid = False

	if valid:
		try:
			with open(filename, "rb"):
				pass
		except:
			valid = False

	if not valid:
		raise AppBaseException("unable to read file '%s'" % filename)
