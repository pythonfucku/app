#!/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: run.py
#         Desc: use log system
#                   asys.log is system log
#                   from lib.core.common.log(__name__)  is app log
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2017-01-01 17:28:36
#      History:
#=============================================================================
'''
import time,signal,sys
from lib.core.data import asys
import lib.core.common as core


def main():   
    sys_log_test()
    app_log_test()

def app_log_test():
    log = core.log(__name__)
    log.info("11111test11111111")


def sys_log_test():
    asys.log.info("test,this log use system log file")

    





