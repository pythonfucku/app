#!/bin/env python
# encoding:utf-8

"""
Author:liangrt
Date:2016-03-10
"""

import os

class SYS:
	_ = os.path.abspath(os.path.dirname(__file__))
	ROOT_PATH = _.split('src')[0]

	CONF_PATH = os.path.join(ROOT_PATH, "conf")
	LOG_PATH = os.path.join(ROOT_PATH, "log")
	SRC_PATH = os.path.join(ROOT_PATH, "src")
	APP_PATH = os.path.join(SRC_PATH, "app")

	CONF_FILE = os.path.join(CONF_PATH, "sysconfig.conf")
	LOG_FILE = os.path.join(LOG_PATH, "system.log")
