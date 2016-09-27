#!/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: main.py
#         Desc: 
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2016-08-11 16:02:35
#      History:
#=============================================================================
'''
import os,time,sys,signal
from multiprocessing import Process

from lib.core.data import paths
from lib.core.data import logger
from lib.core.data import conf
from lib.core.datatype import AttribDict
from lib.core.common import setPaths
from lib.core.exception import AppBaseException
from lib.core.exception import AppLookupException
from lib.core.exception import AppLoadException
from lib.core.common import detachProcess
from lib.server.MPServer import mpServer
from lib.core.cmdLine import cmdLineParser
from lib.core.enum import SYS


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
        conf.app.if_runForever = getattr(module, "if_runForever",None)
    except Exception,e:
       raise AppLoadException(str(e))

def checkEnv():
    if not conf.app.name:
        print "app name is empty can't load"
        raise AppLoadException("app name is empty can't load")
    pass

def initApp():
    conf.app = AttribDict()
    conf.app.file = None
    conf.app.imp = None
    conf.app.func =	None
    conf.app.name = SYS.APP
    conf.app.if_runForever = False
    #conf.app.runModule = None

def runAppProcess():
    appProcess = [
        (conf.app.func,conf.app.name,()),
    ]
    a = mpServer(appProcess,conf.app.if_runForever,conf.app.name)
    a.run()


def call_child_shutdown(signum):
    logger.info("[main] call children shutdown")

def wait_child_shutdown():
    logger.info("wait_child_shutdown")

def shutdown(signum,frame):
    logger.info("System recv a signal message!")
    call_child_shutdown(signal.SIGUSR1)
    wait_child_shutdown()
    logger.info("System exit!")
    logger.info("-"*20 +" System running over "+"-"*20)
    sys.exit(0)

def no_signal(signum,frame):
    logger.info("no_signal:{0}".format(signum))
    pass


def set_signal():
    #信号屏蔽，确保children不会触发这些状态，而只接收father发送归来的user1
    signal.signal(signal.SIGINT,shutdown)
    signal.signal(signal.SIGTERM,shutdown)
    signal.signal(signal.SIGCHLD,wait_child_shutdown)

    #signal.signal(signal.SIGINT,no_signal)
    #signal.signal(signal.SIGTERM,no_signal)
    #signal.signal(signal.SIGCHLD,no_signal)
    pass


def main():
    #set_signal()
    try:
        initApp()
        #判断是否转换到后台执行
        detachProcess()

        setPaths()
        checkEnv()
        lookupApp(conf.app.name)
        if not conf.app.imp:
            errMessage = "can not import app"
            logger.error(errMessage)
            sys.exit(1)
        addApp()

        runAppProcess()
        #conf.app.func()

        logger.info("System exit!")
        logger.info("-"*20 +" System running over "+"-"*20)
        sys.exit(0)
        logger.info("liangrttttttt")

    except AppBaseException as ex:
        logger.error(str(ex))
        pass
    except AppLookupException as ex:
        logger.error(str(ex))
        pass

    except Exception,e:
        logger.error(str(e))
        call_child_shutdown(0)
        sys.exit(1)


