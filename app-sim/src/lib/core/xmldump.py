#!/bin/env python
'''
#=============================================================================
#     FileName: xmldump.py
#         Desc: 转换cms中各话单格式
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2016-05-24 10:04:09
#      History:
#=============================================================================
'''


from xml.dom import minidom
import struct

C2P_TYPES = {
	"int":          "i",
	"char":         "s",
	"string":       "s",
	"uint8":        "B",
	"uint16":       "H",
	"uint32":       "I",
	"uint64":       "Q"
}

def readXmlFile(xmlFile):
	"""
	Reads XML file content and returns its DOM representation
	"""
	root = minidom.parse(xmlFile).documentElement
	return root

def getXmlList(xmlFile):
	"""
	Reads XML file content and returns TagName List 
	e.g.
	output:
		packetList = [
            ("msgid","Q","1",),
            ("statr","s","12",),
            ("end"  ,"I","1",)
        ]
	"""
	outList = []
	root = readXmlFile(xmlFile)
	employees = root.getElementsByTagName("field")
	for em in employees:
		if(em.getAttribute("enable") != "1"):
			continue
		type = C2P_TYPES[em.getAttribute("type")]
		outList.append((em.getAttribute("name"),type,em.getAttribute("nitems")))
	return outList

def getXmlNameList(xmlFile):
	"""
	Reads XML file content and returns TagName Dict
	e.g.
	output:
		packetDict = {
			"msgid":None,
			"start":None,
			"end":None
		}
	"""
	outDictList = []
	root = readXmlFile(xmlFile)
	employees = root.getElementsByTagName("field")
	for em in employees:
		if(em.getAttribute("enable") != "1"):
			continue
		outDictList.append(em.getAttribute("name"))
		
	return outDictList

def xmlFmtPacket(packetList,pragmaPack=1):
	"""
	Reads fmtXmlList and returns fmtPacket str
	e.g.input:(name,type,nitems,enable)
		packetList = [
			("msgid","Q","1"),
			("statr","s","12"),
			("end"  ,"I","1")
		]
	output:	
		Q12SI
	"""
	fmtPacket = ""	
	if(pragmaPack ==1):
		fmtPacket += "<"

	for u in packetList:
		fmtPacket = _padding(fmtPacket,u[1],u[2],pragmaPack)
	return str(fmtPacket)+"0l"

def _padding(fmtPacket,type,len,pragmaPack):
	if(type == "s"):
		fmtPacket += len + "s"
	elif(type == "B"):
		fmtPacket += "B"
	else:
		a = struct.calcsize(str(fmtPacket)) % pragmaPack
		tmp =  a - int(len) if a >= int(len) else a 
		fmtPacket += type if tmp >= 0 else str(tmp) + "s" + type
	return fmtPacket


def getCDRXmlList(xmlFile): 
	#TODO
	pass
	"""
	root = readXmlFile(xmlFile)
	#if root.hasAttribute("separator"):
	print root.getAttribute("separator")
	print root.getAttribute("haveSeparatorAtTail")
	print root.getAttribute("haveCR")
	print root.getAttribute("haveLF")
	print root.getAttribute("depends")
	employees = root.getElementsByTagName("field")
	outDictList = []
	for em in employees:
	"""
