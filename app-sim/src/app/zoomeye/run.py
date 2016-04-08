#!/bin/evn python
#encoding:utf-8

import os
import sys
import requests
import json

from optparse import OptionParser

sys.path.append("../../")

from lib.core.data import conf
from lib.core.data import logger
from lib.core.data import paths

from lib.core.exception import ZoomeyeSearchException

from lib.core.common import checkFile

from init import initConf
from init import initZoomeye
from init import initSearchHostResult

from setResut import setSearchResult
 
def init():
	paths.APP_ROOT_PATH = os.path.abspath(os.path.dirname(__file__)) 
	paths.APP_KEY_FILE = os.path.join(paths.APP_ROOT_PATH,"access_token.txt")
	paths.APP_RESULT_FILE = os.path.join(paths.APP_ROOT_PATH,"output.txt")

	initConf()
	initZoomeye()

	'''
	if or not init here
	no use
	'''
	#initSearchHostResult()

def login():
	data = {}
	if conf.user:
		if not conf.passwd:
			conf.passwd = raw_input('[-] input : password :')

		data = {
			'username' : conf.user,
			'password' : conf.passwd
		}	
		data_encoded = json.dumps(data) 
		try:
			r = requests.post(url = conf.zoomeye.login,data = data_encoded)
			r_decoded = json.loads(r.text)
			if r_decoded.has_key("access_token"):
				conf.zoomeye.key = r_decoded['access_token']
				saveStrToFile(paths.APP_KEY_FILE,conf.zoomeye.key)
				return
			else:
				errMessage = r_decoded["message"]
				logger.error(errMessage)
				setLoginStr()
				login()
		except Exception,e:
			errMessage = "loggin error.\n"
			errMessage += str(e)
			errMessage += "\nPlease try it again"
			logger.error(errMessage)
			setLoginStr()
			login()
	else:
		try:
			getKeyFromFile()
			return
		except:
			logger.info("zoomeye api key is emprty,please login")
			setLoginStr()
			login()

def setLoginStr():
	conf.user = raw_input('[-] input : user:')
	conf.passwd = raw_input('[-] input : password :')

def apiSearch():
	headers = {
		'Authorization' : 'JWT ' + conf.zoomeye.key,
	}

	try:
		count = int(conf.zoomeye.page)
		for i in range(count):
			conf.zoomeye.page = i
			r = requests.get(setSearchStr(),headers = headers)
			r_decoded = json.loads(r.text)

			#TEST
			for x in r_decoded['matches']:
				logger.info(x['ip'])
				conf.ip_list.append(x['ip'])

	except Exception,e:
		if str(e.message) == 'matches':
			logger.info("account was break, excceeding the max limitations")
		else:
			logger.info( str(e.message))

		errMessage = str(e)
		logger.error(errMessage)
		raise ZoomeyeSearchException(errMessage)


def saveStrToFile(file,str):
	with open(file,'w') as output:
		output.write(str)
 
def saveListToFile(file,list):
	s = '\n'.join(list)
	with open(file,'w') as output:
		output.write(s)

def getKeyFromFile():
	with open(paths.APP_KEY_FILE,'rb') as output:
		conf.zoomeye.key = output.read()

def setSearchStr():
	if not conf.zoomeye.query :
		conf.zoomeye.query = ""	

	if conf.zoomeye.type =="host":
		conf.zoomeye.url = conf.zoomeye.hostSearchUrl
	elif conf.zoomeye.type == "web":
		conf.zoomeye.url = conf.zoomeye.webSearchUrl
	else:
		errMessage ="Zoomeye search error,url is error"
		logger.error(errMessage)
		raise ZoomeyeSearchException(errMessage)


	if not conf.zoomeye.page or  type(conf.zoomeye.page) != int:
		conf.zoomeye.page = 1

	if not conf.zoomeye.facets:
		conf.zoomeye.facets = ""
	else:
		tmp = conf.zoomeye.facets.split(',')
		for _ in tmp: 
			if _ not in(conf.zoomeye.hostSearchFacets) and _ not in(conf.zoomeye.webSearchFacets):
				errMessage = "Zoomeye search error,facets is error"
				logger.error(errMessage)
				raise ZoomeyeSearchException(errMessage)

		_ = ",".join(tmp)

	return ("%s?query=\"%s\"&facet=%s&page=%d") % (conf.zoomeye.url,conf.zoomeye.query,conf.zoomeye.facets,conf.zoomeye.page)


 
def main():
	init()
	login()
	apiSearch()
	saveListToFile(paths.APP_RESULT_FILE,conf.ip_list)
 
if __name__ == '__main__':
	main()
