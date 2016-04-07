#!/bin/env python
#encoding:utf-8

import sys
sys.path.append("../../")

from optparse import OptionParser

from lib.core.datatype import AttribDict
from lib.core.data import conf

def initConf():
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

	conf.zoomeye = AttribDict()

	conf.zoomeye.type = options.type
	conf.zoomeye.query = options.query
	conf.zoomeye.facets = options.facets
	conf.zoomeye.page = options.page

def initZoomeye():
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

def initSearchHostResult():
	print "initSearchHostResult"
	conf.zoomeye.hostResult = AttribDict()	

	#conf.zoomeye.hostResult.ip = None
	conf.zoomeye.hostResult.timestamp = None
	
	conf.zoomeye.hostResult.geoinfo = AttribDict()
	conf.zoomeye.hostResult.geoinfo.asn = None

	conf.zoomeye.hostResult.geoinfo.city = AttribDict()
	conf.zoomeye.hostResult.geoinfo.city.en = None
	conf.zoomeye.hostResult.geoinfo.city.zh = None

	conf.zoomeye.hostResult.geoinfo.continent = AttribDict()
	conf.zoomeye.hostResult.geoinfo.continent.code =None

	conf.zoomeye.hostResult.geoinfo.continent.names = AttribDict()
	conf.zoomeye.hostResult.geoinfo.continent.names.en = None
	conf.zoomeye.hostResult.geoinfo.continent.names.zh = None

	conf.zoomeye.hostResult.geoinfo.contry = AttribDict()
	conf.zoomeye.hostResult.geoinfo.contry.code = None

	conf.zoomeye.hostResult.geoinfo.contry.names = AttribDict()
	conf.zoomeye.hostResult.geoinfo.contry.names.en = None
	conf.zoomeye.hostResult.geoinfo.contry.names.zh = None

	conf.zoomeye.hostResult.geoinfo.location = AttribDict()
	conf.zoomeye.hostResult.geoinfo.location.lat = None
	conf.zoomeye.hostResult.geoinfo.location.lon = None

	conf.zoomeye.hostResult.geoinfo.portinfo = AttribDict()
	conf.zoomeye.hostResult.geoinfo.portinfo.app = None
	conf.zoomeye.hostResult.geoinfo.portinfo.banner = None
	conf.zoomeye.hostResult.geoinfo.portinfo.device = None
	conf.zoomeye.hostResult.geoinfo.portinfo.extrainfo = None
	conf.zoomeye.hostResult.geoinfo.portinfo.hostname = None
	conf.zoomeye.hostResult.geoinfo.portinfo.os = None
	conf.zoomeye.hostResult.geoinfo.portinfo.port = None
	conf.zoomeye.hostResult.geoinfo.portinfo.service = None
	conf.zoomeye.hostResult.geoinfo.portinfo.version = None

