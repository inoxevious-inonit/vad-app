import xml.etree.ElementTree as gfg 
import os
from datetime import datetime
from flask import Flask,request, url_for, redirect, render_template, jsonify, abort
import requests
from xmlrpc.server import SimpleXMLRPCServer
import wget
import xmlrpc.client
from xml.etree.ElementTree import Element,tostring

from generate_xml import GenerateXMLFile as xml_generator
from utilities import *
from flask import send_from_directory,send_file

# create  
application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello VAD"

@application.route('/api/xml_download', methods=['GET','POST'])
def get_file():
    # request_json = request.get_json()("{",
    request_json = request.args.get("records")
    request_json =request_json.replace("{", "")
    request_json =request_json.replace("}", "")
    request_json =request_json.replace(",", " ")
    print('request_json', request_json)

    ids = [int(n) for n in request_json.split()]
    print('ids', ids)
    xml_data = GenerateXML(ids)
    print(application.root_path)
    full_path = os.path.join(application.root_path)
    print(full_path)
    xml_file = tostring(xml_data, encoding="ISO-8859-1", method="xml")
    fileName = 'training_gunnar_Invoice_file.xml'
    with open (fileName, "wb") as files :
        file = files.write(xml_file)
    file_path = full_path + '/' + fileName
    print('file_path', file_path)
    if file_path is None:
        self.Error(400)
    try:
        return send_file(file_path, as_attachment=True, download_name='Invoice_file.xml')
    except Exception as e:
        log = self.log.exception(e)
        self.Error(400)
        return render_template("index.html", message=log)

    
# define a function to
# convert a simple dictionary
# of key/value pairs into XML
def GenerateXML(ids) :
    try:
        
        xml_data = xml_generator(ids)
    except Exception as err:
        print(err)
    return xml_data

# Driver Code
if __name__ == "__main__": 
    application.run(host='0.0.0.0', debug=True)
    # GenerateXML("Catalog.xml")