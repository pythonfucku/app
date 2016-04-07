#!/bin/env python
#encoding:utf-8
import sys
sys.path.append("../../")

from lib.core.data import conf

def setSearchResult(r_search):
	for x in r_search["matches"]:
		#conf.zoomeye.hostResult = x
		#print conf.zoomeye.hostResult
		#print x["ip"]
		#conf.zoomeye.hostResult.ip = x["ip"]
		#print conf.zoomeye.hostResult.ip
		#conf.aaaaaaa = x["ip"]
		#conf["bbbb"] = x["ip"]
		#print conf.aaaaaaa
		#print conf.bbbb
		#print x.ip
		ab(x)
		print conf.zoomeye.hostResult
		break

def ab(obj,keyname=None):
	for x in obj.keys():
		print x
		#print obj[x]
		if type(obj[x]) is dict:
			ab(obj[x],x)
			conf.zoomeye.hostResult[x] = obj[x]
