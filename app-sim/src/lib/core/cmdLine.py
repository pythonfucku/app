#!/bin/evn python
# encoding:utf-8
"""
Author:liangrt
Date:2016-03-10
"""
import sys
#from optparse import OptionError
#from optparse import OptionGroup
from optparse import OptionParser
#from optparse import SUPPRESS_HELP

from data import conf
from datatype import AttribDict

def cmdLineParser(argv=None):

	if not argv:
		argv = sys.argv

	try:
		parser = OptionParser()

		parser.add_option("--hh",dest="advancedHelp",
							action="store_true",
							help="Show advanced help message and exit")
		parser.add_option("--version",dest="showVersion",
							action="store_true",
							help="Show program's version number and exit")
		parser.add_option("-v",dest="verbose",type="int",
							help="")

		parser.add_option("--app",dest="app",help="")
		
		(options, args) = parser.parse_args()

		conf.app = AttribDict()
		conf.app.name = options.app
		conf.app.file = None
		conf.app.imp = None
		conf.app.func = None

	except:
		pass

	return parser
