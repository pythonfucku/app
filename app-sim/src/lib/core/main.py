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


def lookupApp():
    for app in conf.apps:
        fileList = []
        try: 
            for f in os.listdir(paths.APP_PATH):
                if os.path.isdir(os.path.join(paths.APP_PATH,f)):
                    appfile = os.path.join(paths.APP_PATH,f,"run.py")
                    if os.path.isfile(appfile):
                        fileList.append({f:appfile})

            for file in fileList:
                if app.name in file.keys():
                    app.file = file[app.name]
                    app.imp = "app." + str(app.name) + ".run"

            logger.debug("APP NAME:{0}".format(app.name))
            logger.debug("APP FILE:{0}".format(app.file))
            logger.debug("APP IMPORT:{0}".format(app.imp))
        except Exception,e:
            raise AppLookupException(str(e))


def addApp():
    for app in conf.apps:
        try:
            module = __import__(app.imp, globals(), locals(), "main")
            app.func = getattr(module, "main", None)
            app.if_runForever = getattr(module, "if_runForever",None)
        except Exception,e:
           raise AppLoadException(str(e))

def checkEnv():
    for app in conf.apps:
        if not app.name:
            print "app name is empty can't load"
            raise AppLoadException("app name is empty can't load")

def initApp():
    conf.apps = []
    for app_name in SYS.APP:
        app = AttribDict()
        app.file = None
        app.imp = None
        app.func =	None
        app.name = app_name
        app.if_runForever = False

        conf.apps.append(app)

def runAppProcess():
    appProcess = []

    for app in conf.apps:
        appProcess.append(
            (app.func,app.if_runForever,app.name,()),
        )

    a = mpServer(appProcess)
    a.run()
    return a

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
    mp = None
    try:
        initApp()
        #判断是否转换到后台执行
        detachProcess()

        setPaths()
        checkEnv()
        lookupApp()
        for app in conf.apps:
            if not app.imp:
                errMessage = "can not import app"
                logger.error(errMessage)
                sys.exit(1)
        addApp()

        mp = runAppProcess()

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

    exitcode = mp.check_serve()
    a = "System exit!"
    b = "-"*20 +" System running over "+"-"*20
    if not exitcode:
        logger.info(a)
        logger.info(b)
    else:
        logger.error(a)
        logger.error(b)
    sys.exit(exitcode)


