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

from lib.core.exception import ZoomeyeAccessKeyException
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

	#if or not init here
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
			conf.zoomeye.key = r_decoded['access_token']
			saveStrToFile(paths.APP_KEY_FILE,conf.zoomeye.key)
		except Exception,e:
			errMessage = "username or password is wrong\n"
			errMessage +=str(e)
			logger.error(errMessage)
			raise ZoomeyeBaseException(errMessage)

	else:
		if not os.path.isfile(paths.APP_KEY_FILE):
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

	headers = {
		'Authorization' : 'JWT ' + conf.zoomeye.key,
	}

	try:
		r = requests.get(setSearchStr(),headers = headers)
		#TODO
		r_decoded = json.loads(r.text)
		setSearchOutput(r_decoded)
		#for x in r_decoded['matches']:
		#	logger.info(x['ip'])
		#	conf.ip_list.append(x['ip'])
		#logger.info('[-] info : count ' + str(page * 10))

	except Exception,e:
		#if str(e.message) == 'matches':
		#	logger.info('[-] info : account was break, excceeding the max limitations')
		#	break
		#else:
		#	logger.info('[-] info : ' + str(e.message))

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

def setSearchOutput(obj):
	setSearchResult(obj)
	"""
	for x in obj['matches']:
		for mk in x.keys():
			#print mk
			if mk == "geoinfo":
				#print x["geoinfo"]
				matches.geoinfo = x["geoinfo"]
				#print matches.geoinfo
			
		break
		print matches.geoinfo
	"""

 
def main():
	init()
	login()
 
	apiTest()
	saveListToFile(paths.APP_RESULT_FILE,conf.ip_list)
 
if __name__ == '__main__':
	main()
