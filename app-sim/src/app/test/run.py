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

from lib.core import common 

def test1(j,a):
    i = 0
    processes = [
        (test2,"test2",(200,30)),
    ]
    for i in range(j):
        i += 1
        logger.info("test11111 working:{0}".format(i)) 
        time.sleep(1)

def test2(j,a):
    i = 0
    for i in range(j):
        i += 1
        logger.info("test22222 working:{0}".format(i) )
        time.sleep(1)

if_runForever = False

def main():   
    #a = testapp()
    #a.main()



    #stdout= shell("iiostat 2 2")
    #print stdout

    print common.cp("b","c")




class testapp():
    processes = [
        (test1,False,"test1-1",(30,20)),
        (test2,False,"test2-2",(30,30)),
    ]
    def main(self):
        a = mpServer(self.processes)
        a.run()

