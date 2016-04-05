#!/bin/env python
# encoding:utf-8
"""
Author:liangrt
Date:2016-03-10
"""

class AppBaseException(Exception):
	pass

class AppLookupException(AppBaseException):
	pass

class AppLoadException(AppBaseException):
	pass

#---------------------------------------------------------------

class ZoomeyeBaseException(Exception):
	pass

class ZoomeyeAccessKeyException(ZoomeyeBaseException):
	pass

class ZoomeyeSearchException(ZoomeyeBaseException):
	pass
