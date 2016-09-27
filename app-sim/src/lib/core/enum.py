#!/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: enum.py
#         Desc: 系统路径和配置文件
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2016-05-24 10:03:20
#      History:
#=============================================================================
'''


import os

class SYS:
    _ = os.path.abspath(os.path.dirname(__file__))
    ROOT_PATH = _.split('src')[0]

    CONF_PATH = os.path.join(ROOT_PATH, "conf")
    LOG_PATH = os.path.join(ROOT_PATH, "log")
    SRC_PATH = os.path.join(ROOT_PATH, "src")
    APP_PATH = os.path.join(SRC_PATH, "app")
    LOCK_PATH = os.path.join(ROOT_PATH, "locks")

    CONF_FILE = os.path.join(CONF_PATH, "sysconfig.conf")
    LOG_FILE = os.path.join(LOG_PATH, "system.log")
    LOCK_FILE = os.path.join(LOCK_PATH, "app-sim.lock")

    APP = None
    RUN_MODULE = 0
