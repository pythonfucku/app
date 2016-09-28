#!/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: run.py
#         Desc: APP自定义函数入口
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2016-05-29 14:27:43
#      History:
#=============================================================================
'''
import time,signal,sys

from lib.core.data import logger
from lib.server.MPServer import mpServer

def test1(j,a):
    i = 0
    for i in range(j):
        i += 1
        logger.info("test33333 working:{0}".format(i)) 
        time.sleep(1)

def test2(j,a):
    i = 0
    for i in range(j):
        i += 1
        logger.info("test44444 working:{0}".format(i) )
        time.sleep(1)

if_runForever = False

def main():   
    a = testapp()
    a.main()

class testapp():
    processes = [
        (test1,False,"test3-3",(30,20)),
        (test2,False,"test4-4",(30,30)),
    ]
    def main(self):
        a = mpServer(self.processes)
        a.run()

