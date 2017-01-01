#!/bin/evn python
# encoding:utf-8
'''
#=============================================================================
#     FileName: cmdLine.py
#         Desc: 解析命令行参数，供zoomeye使用
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 2.0.1
#   LastChange: 2017-01-01 17:25:04
#      History:
#=============================================================================
'''

import sys
#from optparse import OptionError
#from optparse import OptionGroup
from optparse import OptionParser
#from optparse import SUPPRESS_HELP

from lib.core.data import asys

def cmdLineParser(argv=None):

    if not argv:
        argv = sys.argv
    try:
        parser = OptionParser()

        """
        parser.add_option("--hh",dest="advancedHelp",
                          action="store_true",
                          help="Show advanced help message and exit")
        parser.add_option("--version",dest="showVersion",
                          action="store_true",
                          help="Show program's version number and exit")
        parser.add_option("-v",dest="verbose",type="int",
                          help="")
        """

        parser.add_option("-d", action="store_true",dest="qiantai",
                          help="")
        parser.add_option("-s", action="store_true",dest="houtai",
                          help="")

        parser.add_option("--app",dest="app",help="")

        (options, args) = parser.parse_args()


        if options.app:
            asys.RUN_APPS_NAME = options.app.split(',')

        if options.qiantai:
            asys.RUN_MODULE = 1
        elif options.houtai:
            asys.RUN_MODULE  = 0


    except Exception,e:
        print str(e)
        pass

    return parser
