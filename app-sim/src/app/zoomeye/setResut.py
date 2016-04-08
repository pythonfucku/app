#!/bin/env python
#encoding:utf-8
import sys
sys.path.append("../../")

from lib.core.data import conf
from lib.core.data import logger
from lib.core.datatype import AttribDict

def setSearchResult(r_search):
	result_list = []
	logger.debug("setSearchResult")
	for x in r_search["matches"]:
		tmp = AttribDict()
		ab(x,tmp)
		result_list.append(tmp)
	return result_list

def ab(src_dict,dest_dict=None,keyname=None):
	for x in src_dict.keys():
		dest_dict[x] = src_dict[x]
		if type(src_dict[x]) is dict:
			ab(src_dict[x],dest_dict[x],x)




