#!/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: TMIServer.py
#         Desc: ���߳�tcp serve
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
        print ('�Ѿ�����:', self.client_address)  
        self.wfile.write(('[%s] %s' % (ctime(), self.rfile.readline().decode("UTF-8"))).encode("UTF-8"))  
        tcpServ = Server(ADDR, MyRequestHandler)
        print ('�ȴ��µ����ӡ�������')  
        tcpServ.serve_forever()  
