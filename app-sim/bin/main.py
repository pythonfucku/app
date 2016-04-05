#!/bin/env python
# encoding:utf-8
import os
import sys
sys.path.append(os.path.join(os.path.split(sys.path[0])[0],"src"))

from lib.core.enum import SYS
from lib.core.data import paths
from lib.core.data import logger
from lib.core.data import app
from lib.core.common import setPaths
from lib.core.exception import AppBaseException
from lib.core.exception import AppLookupException
from lib.core.exception import AppLoadException


def lookupApp(startName):
	fileList = []
	try: 
		for f in os.listdir(paths.APP_PATH):
			if os.path.isdir(os.path.join(paths.APP_PATH,f)):
				appfile = os.path.join(paths.APP_PATH,f,"run.py")
				if os.path.isfile(appfile):
					fileList.append({f:appfile})

		for apps in fileList:
			if startName in apps.keys():
				app.name = startName
				app.file = apps[startName]
				app.imp = "app." + str(app.name) + ".run"

		#logger.debug(app.name)
		#logger.debug(app.file)
		#logger.debug(app.imp)
	except Exception,e:
		raise AppLookupException(str(e))
		

def addApp():
	if not app.name:
		raise AppLoadException("app name is empty can't load")

	try:
		module = __import__(app.imp, globals(), locals(), "main")
		app.func = getattr(module, "main", None)
	except Exception,e:
		raise AppLoadException(str(e))

def main():

	startName = "zoomeye"


	try:
		setPaths()

		lookupApp(startName)

		addApp()

		app.func()


	except AppBaseException as ex:
		logger.error(str(ex))
	
	except AppLookupException as ex:
		logger.error(str(ex))

	finally:
		print "-"*100

main()
