#!/bin/env python

from socket import *
import time

s = socket(AF_INET,SOCK_STREAM)
connect_str = ("10.10.126.249",1234)
s.connect(connect_str)
while(1):
    s.send("hello")
    print "hello"
    time.sleep(2)
    print s.recv(1024)
