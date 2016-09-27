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
    #while(1):
    processes = [
        (test2,"test2",(200,30)),
    ]
    #a = mpServer(processes)
    #a.run()
    for i in range(j):
        i += 1
        logger.info("test11111 working:{0}".format(i)) 
        time.sleep(1)

def test2(j,a):
    i = 0
    #while(1):
    for i in range(j):
        i += 1
        logger.info("test22222 working:{0}".format(i) )
        time.sleep(1)

#if_runForever = True
if_runForever = False

#系统接入点
def main():   
    a = testapp()
    a.main()

##---------第二种类的写法:继承app,重写main()和shutdown()----------
class testapp():
    processes = [
        (test1,"test1",(30,20)),
        (test2,"test2",(40,30)),
    ]
    def main(self):
        a = mpServer(self.processes)
        a.run()

