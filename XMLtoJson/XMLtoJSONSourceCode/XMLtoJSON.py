'''
class MyException(Exception)
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
'''
"""
if type(root) is list:
	print('list')
if type(root) is dict:
	print('dict')
if type(root) is str:
	print('str')
if type(root) is int:
	print('int')
"""

import sys
import json
import urllib
import dicttoxml
from xml.dom.minidom import parse, parseString
from XmlDictConfig import XmlDictConfig
import xml.etree.cElementTree as ElementTree
#import xml.etree.ElementTree as ElementTree

def test_1():
	try:
		fp = open("./test.json")
	except IOError as e:
		if e.errno == errno.EACCES:
			print e
		raise NameError('Not permission error')
	else:
		with fp:
			jsonString = fp.read()
	#Test1
	print("Read before work: {0}".format(jsonString))
	#Json -> dict
	if not(type(jsonString) is str):
		print('jsonString is not a str')
		sys.exit(1)	
	jsonDict = json.loads(jsonString)
	#dict -> xml
	if not(type(jsonDict) is dict):
		print('jsonDict is not a dict')
		sys.exit(1)
	#my_item_func = lambda x: ' '
	#xmlString = dicttoxml.dicttoxml(jsonDict, attr_type=False, custom_root='rootElement', item_func=my_item_func)
	xmlString = dicttoxml.dicttoxml(jsonDict, attr_type=False, custom_root='rootElement')
	print(xmlString)
	#print it beautiful
	#xmldom = parseString(xmlString)
	#print xmldom.toprettyxml()

	#xml-> dict
	if not(type(xmlString) is str):
		print('xmlString is not a str')
		sys.exit(1)
	#xmlRoot = ElementTree.fromstring(xmlString)  Per a la classe ElementTree
	xmlRoot = ElementTree.XML(xmlString)
	xmlDict = XmlDictConfig(xmlRoot)
	#dict -> json
	if not(type(xmlDict) is dict):
		print('xmlDict is not a dict')
		#sys.exit(1)
	jsonString = json.dumps(xmlDict, skipkeys=False, ensure_ascii=True,check_circular=True, allow_nan=True, cls=None,indent=None, separators=None, encoding='utf-8',default=None)

	#Finished
	print("Read after work: {0}".format(jsonString))

test_1()
