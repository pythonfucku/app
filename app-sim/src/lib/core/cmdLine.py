#!/bin/evn python
# encoding:utf-8
"""
Author:liangrt
Date:2016-03-10
"""

from optparse import OptionError
from optparse import OptionGroup
from optparse import OptionParser
from optparse import SUPPRESS_HELP

def cmdLineParser(argv=None):

	if not argv:
		argv = sys.argv

	parser = OptionParser()

	try:
		parser.add_option("--hh",dest="advancedHelp",
							action="store_true",
							help="Show advanced help message and exit")
		parser.add_option("--version",dest="showVersion",
							action="store_true",
							help="Show program's version number and exit")
		parser.add_option("-v",dest="verbose",type="int",
							help="Verbosity level: 0-6 (default %d)" % defaults.verbose)
