#!/bin/env python
#-*- encoding: UTF-8 -*-
'''
#=============================================================================
#     FileName: common.py
#         Desc: 公共方法库 
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2016-05-24 10:02:43
#      History:
#=============================================================================
'''
import os,fcntl,sys
import subprocess
import shutil

from lib.core.exception import AppBaseException
from lib.core.exception import ExceShellCommandException
from lib.core.enum import SYS
from lib.core.data import logger
from lib.core.data import paths
from lib.core.data import conf

def setPaths():
    paths.ROOT_PATH	=SYS.ROOT_PATH
    paths.APP_PATH	= SYS.APP_PATH
    paths.SYSTEM_LOG_PATH	= SYS.LOG_PATH
    paths.SYSTEM_CONF_PATH	= SYS.CONF_PATH

    paths.SYSTEM_CONF	= SYS.CONF_FILE

    for path in paths.values():
        if any(path.endswith(_) for _ in (".txt",".conf",".xml",".zip")):
            checkFile(path)

def checkFile(filename):
    valid = True

    if filename is None or not os.path.isfile(SYS.LOCK_FILE):
        valid = False
        if valid:
            try:
                with open(filename, "rb"):
                    pass
            except:
                valid = False
                if not valid:
                    raise AppBaseException("Unable to read file:{0}".format( filename))

pidfile = 0 
def lockFile():
    checkFile(SYS.LOCK_FILE)

    global pidfile
    pidfile = open(SYS.LOCK_FILE ,"r")

    try:
        fcntl.flock(pidfile,fcntl.LOCK_EX| fcntl.LOCK_NB)
        file(SYS.LOCK_FILE,"w+").write("%s\n" % os.getpid())
    except Exception,e:
        print "Lock file error:{0}".format(str(e))
        print ("System is alread running...")
        sys.exit(1)

def detachProcess():
    lockFile()

    if SYS.RUN_MODULE:
        return

    stdin = "/dev/null"
    stdout = "/dev/null"
    stderr = "/dev/null" 

    try:
        pid = os.fork()
        if pid > 0:
            print "System start running on backgrounder"
            sys.exit(0)
    except Exception,e:
        errMessage = "System detach daemon process error:{0}".format(str(e))
        logger.error(errMessage)
        sys.exit(1)

    os.chdir(SYS.ROOT_PATH)
    os.setsid()
    os.umask(0)

    if os.fork() > 0:
        sys.exit(0)

    for f in sys.stdout, sys.stderr: 
        f.flush()
        si = open(stdin, 'r')  
        so = open(stdout, 'a+')  
        se = open(stderr, 'a+', 0)  
        os.dup2(si.fileno(), sys.stdin.fileno())    #dup2函数原子化关闭和复制文件描述符  
        os.dup2(so.fileno(), sys.stdout.fileno())  
        os.dup2(se.fileno(), sys.stderr.fileno())  

    pid=str(os.getpid())
    file(SYS.LOCK_FILE,'w+').write("%s\n" % pid)

    logger.info("-"*20 +" System start running on backgrounder,pid:{0}".format(pid) +"-"*20) 


def print_exce_command(args):
    logger.info("Exec command:{0}".format(args))

def print_err_exce_command(code,stderr):
    logger.error("Exec command error,code:{0}".format(code))
    logger.error("{0}".format(stderr))

def base_shell(args):
    print_exce_command(args)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    stdout, stderr = p.communicate()
    
    if stderr:
        print_err_exce_command(p.returncode,stderr)
        raise ExceShellCommandException(stderr)

    return stdout

def bash(command):
    args = ['bash','-c',command]
    return base_shell(args)
        
        
def cp(localfile,remotefile):
    args = ['cp', '-rf', localfile,remotefile]
    base_shell(args)


def mv(src,dest):
    args = ['mv',src,dest]
    base_shell(args)

def scp(user,node,localfile,remotefile):
    #local to remote
    args = ['scp','-oConnectTimeout=15','-r',localfile, '%s@%s:%s' % (user,node,remotefile)]
    base_shell(args)

def rscp(user,node,localfile,remotefile):
    #remote to local
    args = ['scp','-oConnectTimeout=15','-r', '%s@%s:%s' % (user,node,remotefile),localfile]
    base_shell(args)

def rrscp(user,node1,node1_file,node2,node2_file):
    args = ['scp','-oConnectTimeout=15','r', '%s@%s:%s' % (user,nodel1,nodel_file), '%s@%s:%s' % (user,node2,node2_file)]
    base_shell(args)

def pdsh(user,nodes,command):
    # many nodes,so nodes must to be list
    _nodes = []
    for node in nodes:
        _nodes.append("%s@%s" % (user,node))
    _nodes = ",".join(_nodes)

    args = ['pdsh','-R','exce','-w' ,_nodes,'-f',str(len(nodes)),'ssh','%h','-oConnectTime=15',command]


    return base_shell(args)
