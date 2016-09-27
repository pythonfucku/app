#!/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: exception.py
#         Desc: �쳣��
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2016-05-24 10:03:32
#      History:
#=============================================================================
'''

class AppBaseException(Exception):
	pass

class AppLookupException(AppBaseException):
	pass

class AppLoadException(AppBaseException):
	pass

#---------------------------------------------------------------

class ZoomeyeBaseException(Exception):
	pass


class ZoomeyeSearchException(ZoomeyeBaseException):
	pass

#--------------------------------------------------------------
class ServerException(Exception):
	pass

class TcpServerException(Exception):
    pass
