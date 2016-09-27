#!/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: TMIServer.py
#         Desc: 多线程tcp serve
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2016-05-24 10:02:04
#      History:
#=============================================================================
'''
from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH,ThreadingMixIn as TMI)
from time import ctime
   
HOST = ''  
PORT = 1234  
ADDR = (HOST, PORT)  
class Server(TMI, TCP):
    pass  
         
class MyRequestHandler(SRH):  
    def handle(self):  
        print ('已经连接:', self.client_address)  
        self.wfile.write(('[%s] %s' % (ctime(), self.rfile.readline().decode("UTF-8"))).encode("UTF-8"))  
        tcpServ = Server(ADDR, MyRequestHandler)
        print ('等待新的连接。。。。')  
        tcpServ.serve_forever()  
