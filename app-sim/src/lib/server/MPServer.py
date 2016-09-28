#!/bin/env python
#-*- encoding: UTF-8 -*-
'''
#=============================================================================
#     FileName: MPServer.py
#         Desc: 提供进程管理框架
#               1.可捕获子进程异常退出，重新拉起(SERVER_FOREVER 模式下)
#               2.父进程通知子进程正常退出
#               3.子进程正常退出,通知父进程
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 1.0.0
#   LastChange: 2016-08-11 16:00:45
#      History: 
#=============================================================================
'''

import time,signal,os,sys
from multiprocessing import Process
import multiprocessing

sys.path.append("../../")
from lib.core.datatype import AttribDict
from lib.core.data import logger
from lib.core.exception import ServerException

class mpServer:
    def __init__(self,funcList,if_runForever=False,myselfname=""):
        """
        processObjects：需要创建的子进程列表，
        格式：
        processes = [
        (test1,"test1",(10,20,)),
        (func,"子进程名",(参数1，参数2，……)),
        ]
        """
        self.myselfname = myselfname
        self._pCount = len(funcList) 
        if not self._pCount:
            errMessage = "mp server args[funcList] is empty"
            logger.error(errMessage)
            raise ServerException(errMessage)
        self.children_exit_flag = False

        self.children = {}
        self._processList = []

        for f,if_runForever,name,args in funcList:
            tmp = app(if_runForever,f,name,args)
            self._processList.append(tmp)

    def run(self):
        self.main()

    def main(self):
        self.set_signal()
        for obj in self._processList:
            try:
                w = self.start_process(obj)
                obj.process = w
                obj.pid = w.pid

                self.children[obj.pid] = w
            except Exception,e:
                errMessage = "start process error:{0}".format(e)
                logger.error(errMessage)
                raise ServerException(errMessage)
        
        self.check_serve()

    def start_process(self,obj,*arg):
        w = Process(target=obj.run,args=obj.args,name=obj.name)
        w.start()
        logger.debug("New process:{0},pid:{1} start to work".format(w.name,w.pid))
        return w

    def check_serve(self):
        while not self.children_exit_flag:
            for obj in self._processList:
                #正常退出，删除子进程
                if not obj.process.exitcode and obj.process.exitcode == 0:
                    if obj.process.exitcode == 0:
                        logger.debug("process[name:{0},pid{1}],run over.".format(obj.process.name,obj.process.pid))
                        for pid,process in self.children.items():
                            if obj.process.pid == pid:
                                self.children.pop(pid)
                                self._processList.remove(obj)
                        if not len(self.children):
                            self.children_exit_flag = True
                #异常退出，重启子进程
                elif obj.process.exitcode:
                    for pid,process in self.children.items():
                        if obj.process.pid == pid:
                            self.children.pop(pid)

                            w = self.start_process(obj)
                            self.children[w.pid] = w
                            obj.process = w
                            obj.pid = w.pid
                            logger.error("process name:{0},pid:{1}] is down,need restart,new pid:{2}".format(obj.name,obj.pid,w.pid))
                else:
                    #logger.info("process[name:{0},pid:{1}],running normal".format(obj.process.name,obj.process.pid))
                    pass

            if not len(self.children):
                self.children_exit_flag = True
            time.sleep(1)

        logger.error("main process exit")


    def set_signal(self):
        signal.signal(signal.SIGINT,self.shutdown)
        signal.signal(signal.SIGTERM,self.shutdown)
        #signal.signal(signal.SIGCHLD,self.wait_child_shutdown)
        signal.signal(signal.SIGUSR1,self.shutdown)
        pass

    def call_child_shutdown(self,signum,frame):
        self.children_exit_flag = True
        for pid,process in self.children.items():
            logger.error("call children process[name:{0},pid:{1}] exit[{2}]".format(process.name,pid,signum))
            os.kill(pid,signum)

    def wait_child_shutdown(self):
        for pid,process in self.children.items():
            logger.error("wait process[name:{0},pid:{1}] shutdown".format(process.name,pid))
            process.join()
            self.children.pop(pid)
            logger.error("main process[name:{0},pid:{1}] exit".format(process.name,pid))

    def shutdown(self,signum,frame):
        logger.error("process:{0} get exit code:{1}".format(self.myselfname,signum))
        if len(self.children):
            self.call_child_shutdown(signal.SIGUSR1,frame)
            self.wait_child_shutdown()
            sys.exit(signum)
        else:
            logger.error("pp {0}".format(os.getpid()))
            for obj in self._processList:
                if obj.pid == os.getpid():
                    obj._runForever = False



class app(mpServer):
    def __init__(self,runFlag,func,processName,args):
        """
        processes = [
            (test1,"test1",run_flag,(10,20,)),
            (运行的函数,"子进程名",是否一直运行,(参数1，参数2，……)),
        ]
        """
        self._runForever = runFlag
        self.func = func
        self.name = processName
        self.args = args
        self.pid = None
        self.process = None
        self.children = []
        self.exitcode = 0
        pass

    def run(self,*args):
        self.exitcode = 0
        self.set_signal()
        if self._runForever:
            while(self._runForever):
                self.func(*args)
                time.sleep(1)
        else:
            self.func(*args)

        logger.error("child process[name:{0},pid:{1}] exit[{2}]".format(self.name,os.getpid(),self.exitcode))
        sys.exit(self.exitcode)

    def shutdown(self,signum,frame):
        logger.error("child process[name:{0},pid:{1}] get exit code:{2}".format(self.name,os.getpid(),signum))
        logger.error("waitting for func running over")
        self._runForever = False
        self.exitcode = signum

    def set_signal(self):
        signal.signal(signal.SIGINT,self.shutdown)
        signal.signal(signal.SIGTERM,self.shutdown)
        signal.signal(signal.SIGUSR1,self.shutdown)



