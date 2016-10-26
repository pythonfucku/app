#!/bin/env python
#-*- encoding: UTF-8 -*-
'''
#=============================================================================
#     FileName: MPServer.py
#         Desc: �ṩ���̹�����
#               1.�ɲ����ӽ����쳣�˳�����������(SERVER_FOREVER ģʽ��)
#               2.������֪ͨ�ӽ��������˳�
#               3.�ӽ��������˳�,֪ͨ������
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
from lib.core import exception

MYEXITCODE = 126

class mpServer:
    def __init__(self,funcList,if_runForever=False,myselfname=""):
        """
        processObjects����Ҫ�������ӽ����б�
        ��ʽ��
        processes = [
        (test1,"test1",(10,20,)),
        (func,"�ӽ�����",(����1������2������)),
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

        self.killed = 0

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
        

    def start_process(self,obj,*arg):
        w = Process(target=obj.run,args=obj.args,name=obj.name)
        w.start()
        logger.info("APP process:[{0},pid:{1}],START! ".format(w.name,w.pid))
        return w

    def check_serve(self):
        returnCode = 0
        while not self.children_exit_flag:
            returnCode = 0
            for obj in self._processList:
                #�����˳���ɾ���ӽ���
                exitcode = obj.process.exitcode

                if (not exitcode and exitcode == 0) or exitcode == MYEXITCODE:
                    returnCode += exitcode
                    Message = "APP process[{0},pid{1}],STOP.".format(obj.process.name,obj.process.pid)
                    if exitcode == 0:
                        logger.warning(Message)
                    elif exitcode == MYEXITCODE:
                        logger.error(Message)

                    for pid,process in self.children.items():
                        if obj.process.pid == pid:
                            self.children.pop(pid)
                            self._processList.remove(obj)
                    if not len(self.children):
                        self.children_exit_flag = True
                #�쳣�˳��������ӽ���
                elif obj.process.exitcode:
                    returnCode += exitcode
                    for pid,process in self.children.items():
                        if obj.process.pid == pid:
                            logger.error("process name:{0},pid:{1}] is down,need RESTART!".format(obj.name,obj.pid,))

                            self.children.pop(pid)

                            w = self.start_process(obj)
                            self.children[w.pid] = w
                            obj.process = w
                            obj.pid = w.pid
                else:
                    #logger.info("process[name:{0},pid:{1}],running normal".format(obj.process.name,obj.process.pid))
                    pass

            if not len(self.children):
                self.children_exit_flag = True
            time.sleep(1)

        #logger.warning("MPserver recv children exit singal,exited.")
        return returnCode


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
        self.killed += 1
        for pid,process in self.children.items():
            if self.killed >10:
                os.kill(pid,9)
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
                    #obj._runForever = False
                    os.kill(pid,9)




class app(mpServer):
    def __init__(self,runFlag,func,processName,args):
        """
        processes = [
            (test1,"test1",run_flag,(10,20,)),
            (���еĺ���,"�ӽ�����",�Ƿ�һֱ����,(����1������2������)),
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

    def exit(self,Message):
        if(self.exitcode):
            logger.error(Message)
        else:
            logger.warning(Message) 
        sys.exit(self.exitcode)

    def run(self,*args):
        self.exitcode = 0
        self.set_signal()
        try:
            if self._runForever:
                while(self._runForever):
                    self.func(*args)
                    time.sleep(1)
            else:
                self.func(*args)

            Message = "APP process:[{0},pid:{1}] exit[{2}]".format(self.name,os.getpid(),self.exitcode)

            self.exit(Message)

        #except Exception as e:
            #if hasattr(exception,e.__class__.__name__):
                #self.exitcode = MYEXITCODE
                #sys.exit(self.exitcode)

        except(
                exception.ExceShellCommandException,
                exception.ServerException,
                exception.TcpServerException
            ) as e:
            self.exitcode = MYEXITCODE
            sys.exit(self.exitcode)


    def shutdown(self,signum,frame):
        print "-"*100
        logger.error("APP process:[:{0},pid:{1}] get exit code:{2}".format(self.name,os.getpid(),signum))
        logger.error("waitting for func running over")
        self._runForever = False
        self.exitcode = signum
        self.exit("APP process:[{0},pid:{1}] exit[{2}]".format(self.name,os.getpid(),self.exitcode))

    def set_signal(self):
        signal.signal(signal.SIGINT,self.shutdown)
        signal.signal(signal.SIGTERM,self.shutdown)
        signal.signal(signal.SIGUSR1,self.shutdown)



