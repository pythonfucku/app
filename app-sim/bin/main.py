#!/bin/env python
# encoding:utf-8
import os
import sys
sys.path.append(os.path.join(os.path.split(sys.path[0])[0],"src"))


from lib.core.data import paths
from lib.core.data import logger
from lib.core.data import conf
from lib.core.datatype import AttribDict
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
				conf.app.file = apps[startName]
				conf.app.imp = "app." + str(conf.app.name) + ".run"

		logger.debug("APP NAME:{0}".format(conf.app.name))
		logger.debug("APP FILE:{0}".format(conf.app.file))
		logger.debug("APP IMPORT:{0}".format(conf.app.imp))
	except Exception,e:
		raise AppLookupException(str(e))
		

def addApp():
	try:
		module = __import__(conf.app.imp, globals(), locals(), "main")
		conf.app.func = getattr(module, "main", None)
	except Exception,e:
		raise AppLoadException(str(e))

def checkEnv():
	if not conf.app.name:
		raise AppLoadException("app name is empty can't load")
	pass

def initApp():
	conf.app = AttribDict()
	conf.app.name = None
	conf.app.file = None
	conf.app.imp = None
	conf.app.func =	None

	if len(sys.argv)>1:
		conf.app.name = sys.argv[1]

def main():
	try:
		setPaths()
		initApp()
		checkEnv()

		lookupApp(conf.app.name)
		if not conf.app.imp:
			errMessage = "can not import app"
			logger.error(errMessage)
			return

		addApp()
		logger.info("APP[{0}] running".format(conf.app.name))
		conf.app.func()

	except AppBaseException as ex:
		logger.error(str(ex))
	except AppLookupException as ex:
		logger.error(str(ex))

	except Exception,e:
		logger.error(str(e))

	finally:
		logger.info("-"*20 +"OVER"+"-"*20)

main()
