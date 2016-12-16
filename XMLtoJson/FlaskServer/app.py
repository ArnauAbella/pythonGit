# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask,Response, render_template, request, url_for, redirect
import sys
import os
import json
import urllib
import dicttoxml
from xml.dom.minidom import parse, parseString
from XmlDictConfig import XmlDictConfig
import xml.etree.cElementTree as ElementTree
#Necessary to check file extension
from werkzeug.utils import secure_filename
import ssl

# Initialize the Flask application
app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['xml', 'json'])
PEM_PRIVATEKEY_PASS = "1234"
ABS_PATH = os.path.abspath(__file__)

def getpswd():
	return PEM_PRIVATEKEY_PASS

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def form():
	return render_template('form.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is
# accepting: POST requests in this case
@app.route('/translate', methods=['POST'])
def translate():
	# check if the post request has the file part
	if 'jsonXML' not in request.files:
		print('User modified html')
		return render_template('response.html', jsonXML="DON'T BE TRICKY")
	jsonXML=request.files['jsonXML']
	# if user does not select file, browser also
	# submit a empty part without filename
	if jsonXML.filename == '':
		print('No selected file')
		return render_template('response.html', jsonXML="YOU MUST SELECT A FILE TO CONVERT")
	#Check file type
	if jsonXML and allowed_file(jsonXML.filename):
		#Avoid OS attacks /../../../systemd.xml
		filename = secure_filename(jsonXML.filename)
		#Get type of file and transform file multipart to String :)
		mode = jsonXML.filename.rsplit('.', 1)[1]
		text = jsonXML.read().decode('utf-8')
		res = "SOMETHING WENT WRONG :("
		#Lets do real work
		if mode == 'xml': #XML TO JSON
			if not(type(text) is str):
				print('xml text is not a str')
			else:
				#XML -> dict
				xmlRoot = ElementTree.XML(text)
				xmlDict = XmlDictConfig(xmlRoot)
				#dict -> json
				res = json.dumps(xmlDict, skipkeys=False, ensure_ascii=True,check_circular=True, allow_nan=True, cls=None,indent=None, separators=None,default=None)
				#Write it on local folder
				if not os.path.exists("convertedFiles"):
					os.makedirs("convertedFiles")
				filepath = './convertedFiles/'+filename.rsplit('.', 1)[0]+".json"
				with open(filepath, 'w') as f:
					f.write(json.dumps(xmlDict, skipkeys=False, ensure_ascii=True,check_circular=True, allow_nan=True, cls=None,indent=4, separators=None,default=None))
				f.closed
		else: #JSON TO XML
			if not(type(text) is str):
				print('json text is not a str')
			else:
				#JSON -> dict 	
				jsonDict = json.loads(text)
				#dict -> XML
				res = dicttoxml.dicttoxml(jsonDict, attr_type=False, custom_root='rootElement').decode('utf-8')
				#Write it on local folder
				if not os.path.exists("convertedFiles"):
					os.makedirs("convertedFiles")
				filepath = './convertedFiles/'+filename.rsplit('.', 1)[0]+".xml"
				with open(filepath, 'w') as f:
					xmldom = parseString(res)
					f.write(xmldom.toprettyxml())
				f.closed
		#Return function
		return render_template('response.html', jsonXML=res)
	else:
		print('Wrong File Extension')
		return render_template('response.html', jsonXML="FILE IS NOT .json or .xml")

# Run the app :)
if __name__ == '__main__':
  context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  context.load_cert_chain('keyCertRSA/cert.pem', keyfile='keyCertRSA/key.pem', password=getpswd)	
  app.run(port=9000, ssl_context=context)
