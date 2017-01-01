#!/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: main.py
#         Desc: 
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 2.0.1
#   LastChange: 2017-01-01 17:23:26
#      History:
#=============================================================================
'''
import os,time,sys,signal,ConfigParser

from lib.core.exception import AppBaseException,AppLookupException,AppLoadException
from lib.server.MPServer import mpServer
from lib.core.cmdLine import cmdLineParser
import lib.core.common as core
from lib.core.data import asys

def main():
    #set_signal()
    mp = None
    exitcode = -1

    initSys()
    initApp()
    try:
        core.detachProcess()

        lookupApp()
        addApp()

        mp = runAppProcess()

    except AppBaseException as ex:
        asys.log.error(str(ex))
    except AppLookupException as ex:
        asys.log.error(str(ex))
    except Exception,e:
        print str(e)
        asys.log.error(str(e))
        call_child_shutdown(0)
        sys.exit(1)

    if mp:
        exitcode = mp.check_serve()
    a = "System exit!"
    b = "-"*20 +" System running over "+"-"*20
    if not exitcode:
        asys.log.info(a)
        asys.log.info(b)
    else:
        asys.log.error(a)
        asys.log.error(b)
    sys.exit(exitcode)

def initSys():
    set_sys_path()
    initConfig()
    cmdLineParser()

def set_sys_path():
    _ = os.path.abspath(os.path.dirname(__file__))
    asys.ROOT_PATH = _.split('src')[0]

    asys.CONF_PATH = os.path.join(asys.ROOT_PATH, "conf")
    asys.LOG_PATH = os.path.join(asys.ROOT_PATH, "log")
    asys.SRC_PATH = os.path.join(asys.ROOT_PATH, "src")
    asys.APP_PATH = os.path.join(asys.SRC_PATH, "app")
    asys.LOCK_PATH = os.path.join(asys.ROOT_PATH, "locks")
    
    asys.CONF_FILE = os.path.join(asys.CONF_PATH, "sysconfig.conf")
    asys.LOG_FILE = os.path.join(asys.LOG_PATH, "system.log")
    asys.LOCK_FILE = os.path.join(asys.LOCK_PATH, "app-sim.lock")
    
    asys.RUN_MODULE = 0
    asys.RUN_APPS_NAME = None
    asys.APPS = {}

    asys.log =core.set_app_log(asys.LOG_FILE) 


def initConfig():
    conf = ConfigParser.ConfigParser()
    conf.read(asys.CONF_FILE)

    run_module = int(conf.get("LOG","Type"))
    app_names = (conf.get("APP","name"))

    asys.RUN_MODULE = run_module
    asys.RUN_APPS_NAME = app_names.split(',')

def initApp():
    """
    {
        'file': None, 
        'name': 'test', 
        'imp': None, 
        'func': None, 
        'log_file': '/home/crow/py_proj/app/app/app-sim/log/test.log', 
        'if_runForever': False, 
        'log': <logging.Logger object at 0x7f0876ff3ad0>
    }
    """
    for app_name in asys.RUN_APPS_NAME:
        asys.APPS[app_name] = {}
        asys.APPS[app_name]["name"] = app_name
        asys.APPS[app_name]["file"] = None
        asys.APPS[app_name]["imp"] = None
        asys.APPS[app_name]["func"] =	None
        asys.APPS[app_name]["if_runForever"] = False
        asys.APPS[app_name]["log_file"] = os.path.join(asys.LOG_PATH,app_name+".log")
        asys.APPS[app_name]["log"] = core.set_app_log(asys.APPS[app_name]["log_file"])


def lookupApp():
    for app in asys.APPS.keys():
        fileList = []
        try: 
            for f in os.listdir(asys.APP_PATH):
                if os.path.isdir(os.path.join(asys.APP_PATH,f)):
                    appfile = os.path.join(asys.APP_PATH,f,"run.py")
                    if os.path.isfile(appfile):
                        fileList.append({f:appfile})

            for file in fileList:
                if asys.APPS[app]["name"] in file.keys():
                    asys.APPS[app]["file"] = file[asys.APPS[app]["name"]]
                    asys.APPS[app]["imp"] = "app." + str(asys.APPS[app]["name"]) + ".run"

            asys.log.debug("APP NAME:{0}".format(asys.APPS[app]["name"]))
            asys.log.debug("APP FILE:{0}".format(asys.APPS[app]["file"]))
            asys.log.debug("APP IMPORT:{0}".format(asys.APPS[app]["imp"]))
            asys.log.debug("APP LOG FILE:{0}".format(asys.APPS[app]["log_file"]))
        except Exception,e:
            raise AppLookupException(str(e))


def addApp():
    for app in asys.APPS.keys():
        try:
            module = __import__(asys.APPS[app]["imp"], globals(), locals(), "main")
            asys.APPS[app]["func"] = getattr(module, "main", None)
            asys.APPS[app]["if_runForever"] = getattr(module, "if_runForever",None)
        except Exception,e:
           raise AppLoadException(str(e))

def runAppProcess():
    appProcess = []

    for app in asys.APPS.keys():
        appProcess.append(
            (asys.APPS[app]["func"],asys.APPS[app]["if_runForever"],asys.APPS[app]["name"],()),
        )

    a = mpServer(appProcess)
    a.run()
    return a

def call_child_shutdown(signum):
    asys.log.info("[main] call children shutdown")

def wait_child_shutdown():
    asys.log.info("wait_child_shutdown")

def shutdown(signum,frame):
    asys.log.info("System recv a signal message!")
    call_child_shutdown(signal.SIGUSR1)
    wait_child_shutdown()
    asys.log.info("System exit!")
    asys.log.info("-"*20 +" System running over "+"-"*20)
    sys.exit(0)

def no_signal(signum,frame):
    asys.log.info("no_signal:{0}".format(signum))
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

