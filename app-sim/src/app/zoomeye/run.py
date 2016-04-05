#!/bin/evn python
#encoding:utf-8

import os
import sys
import requests
import json

from optparse import OptionParser

sys.path.append("../../")

from lib.core.datatype import AttribDict
from lib.core.data import conf
from lib.core.data import logger
from lib.core.data import paths

from lib.core.exception import ZoomeyeAccessKeyException
from lib.core.exception import ZoomeyeSearchException

from lib.core.common import checkFile
 
def init():
	paths.APP_ROOT_PATH = os.path.abspath(os.path.dirname(__file__)) 
	paths.APP_KEY_FILE = os.path.join(paths.APP_ROOT_PATH,"access_token.txt")
	paths.APP_RESULT_FILE = os.path.join(paths.APP_ROOT_PATH,"output.txt")

	conf.zoomeye = AttribDict()

	parser = OptionParser()
	parser.add_option("-u",dest="user",help="")
	parser.add_option("-p",dest="passwd",help="")
	parser.add_option("--type",dest="type",help="")
	parser.add_option("--query",dest="query",help="")
	parser.add_option("--facets",dest="facets",help="")
	parser.add_option("--page",dest="page",help="")

	(options, args) = parser.parse_args()  


	conf.user = options.user
	conf.passwd = options.passwd
	conf.ip_list = []  

	conf.zoomeye.type = options.type
	conf.zoomeye.query = options.query
	conf.zoomeye.facets = options.facets
	conf.zoomeye.page = options.page


	conf.zoomeye.key = ""
	conf.zoomeye.login = "http://api.zoomeye.org/user/login"
	conf.zoomeye.hostSearchUrl = "http://api.zoomeye.org/host/search"
	conf.zoomeye.hostSearchFacets= [
		"app",
		"devic",
		"service",
		"os",
		"port",
		"country",
		"city"
	]
	conf.zoomeye.webSearchUrl = "http://api.zoomeye.org/web/search"
	conf.zoomeye.webSearchFacets= [
		"webapp",
		"component",
		"framework",
		"frontend",
		"server",
		"waf",
		"os",
		"country",
		"city"
	]

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
			conf.zoomeye.key = r_decoded['access_token']
			saveStrToFile(paths.APP_KEY_FILE,conf.zoomeye.key)
		except Exception,e:
			errMessage = "username or password is wrong\n"
			errMessage +=str(e)
			logger.error(errMessage)
			raise ZoomeyeBaseException(errMessage)

	else:
		if os.path.isfile(paths.APP_KEY_FILE) and not os.path.getsize(paths.APP_KEY_FILE):  
			errMessage = "access_key is empty"
			logger.error(errMessage)
			raise ZoomeyeAccessKeyException(errMessage)
		else:
			try:
				getKeyFromFile()
				return
			except Exception ,e:
				errMessage = "get access_key error"
				errMessage += str(e)
				raise ZoomeyeAccessKeyException(errMessage)
 
def apiTest():
	if not conf.zoomeye.key:
		with open(paths.APP_KEY_FILE,'r') as input:
			conf.zoomeye.key = input.read()

	page = 1
	headers = {
		'Authorization' : 'JWT ' + conf.zoomeye.key,
	}

	while(True):
		try:
			r = requests.get(setSearchStr(),headers = headers)
			#TODO
			r_decoded = json.loads(r.text)
            # print r_decoded
            # print r_decoded['total']
			for x in r_decoded['matches']:
				logger.info(x['ip'])
				conf.ip_list.append(x['ip'])
			logger.info('[-] info : count ' + str(page * 10))
 
		except Exception,e:
			if str(e.message) == 'matches':
				logger.info('[-] info : account was break, excceeding the max limitations')
				break
			else:
				logger.info('[-] info : ' + str(e.message))

			if page == 10:
				break
			page += 1

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
 
	apiTest()
	saveListToFile(paths.APP_RESULT_FILE,conf.ip_list)
 
if __name__ == '__main__':
	main()
