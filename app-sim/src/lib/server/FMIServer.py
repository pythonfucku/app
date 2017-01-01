#!/bin/env python
# encoding: utf-8
'''
#=============================================================================
#     FileName: FMIServer.py
#         Desc: �����tcp server
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2016-05-24 10:00:35
#      History:
#=============================================================================
'''

from SocketServer import TCPServer, StreamRequestHandler, ForkingMixIn
import os
import time
import Queue
from multiprocessing import Process
import threading

import sys
sys.path.append("../../")
from lib.core.data import asys
from lib.core.exception import TcpServerException
from MPServer import mpServer



class Server(ForkingMixIn, TCPServer):
    
    max_children = 40

    def __init__(self, server_address, RequestHandlerClass,func):
        TCPServer.__init__(self,server_address,RequestHandlerClass,bind_and_activate=True)
        self.func = func
        asys.log.info("FMIServer start listening...")

class MyRequestHandler(StreamRequestHandler): 

    rbufsize =1024

    def handle(self): 
        """
        self.server:TCPServer
            server_address
            RequestHandlerClass
            socket
        """
        asys.log.info("FMIServer new client:{0},login".format(str(self.client_address)))

        while(1):
            try:
                data = self.request.recv(self.rbufsize)
            except Exception,e:
                errMessage = "FMIServer client:{0},recv message error:{1}".format(str(self.client_address),str(e))
                asys.log.error(errMessage)
                #raise TcpServerException(errMessage)
                return

            if not data:
                errMessage = "FMIServer socket error:client exit"
                #raise TcpServerException(errMessage)
                return

            asys.log.debug("FMIServer recv:{0}".format(data))

            #�ص���socketԭʼ���ݣ�û�д���
            try:
                send_msg = self.server.func(data)
            except Exception,e:
                errMessage = "FMIServer call:{0} error:{1}".format(self.server.func,str(e))
                #raise TcpServerException(errMessage)
                return

            try:
                if send_msg:
                    self.request.send(send_msg)
                    asys.log.debug("FMIServer send:{0}".format(send_msg))
            except Exception,e:
                errMessage = "FMIServer running error:{0}".format(str(e))
                asys.log.error(errMessage)
                #raise TcpServerException(errMessage)
                return

    def finish(self):
        asys.log.error("FMIServer client:{0} logout".format(str(self.client_address)))
        StreamRequestHandler.finish(self)

class tcpServer():
    def __init__(self,port,func,host=None):
        if host:
            self.host = host
        else:
            self.host = ""

        self.port = port
        self.__ADDR = (self.host, self.port)
        self.__queue = Queue.Queue()
        self.func = func
        pass

    def run(self):
        server = Server(self.__ADDR,MyRequestHandler,self.func)
        a = [
            (server.serve_forever,"TCP SERVER MODULE",()),
        ]
        mps = mpServer(a)
        mps.run()

        #w = Process(target=server.serve_forever,)
        #w.daemon = True
        #w.start()


        return 


        #while(1):
            #print "main run"
            #time.sleep(1)

#--------------------------------------------------------------------------------
def test(recv_msg):
    asys.log.info("test:{0}".format(recv_msg))
    return "aaa"
#--------------------------------------------------------------------------------


a = tcpServer(1234,test)
a.run()
#while(1):
    #asys.log.info("tcpServer start ,�����������ɱ��")
    #time.sleep(5)


