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


# create application server
application = Flask(__name__)


@application.route("/")
def hello():
    return "Hello VAD"

@application.route('/api/xml_download', methods=['GET'])
def get_file():
    request_json = request.get_json()
    xml_data = GenerateXML(request_json)
    # print('file', tostring(xml_data))
    # return xml file
    xml_file = tostring(xml_data)
    fileName = 'training_gunnar_Invoice_file.xml'
    with open (fileName, "wb") as files :
        file = files.write(xml_file)
    return 'file'

def Get_InvoiceData():
    # Query the invoice data from model
    try:
        # get invoices list
        invoices_list = models_object.execute_kw(db, uid, password,
        'account.move', 'search',
            [[['is_move_sent', '=', False]]])

        for rec in invoices_list:
            [record] = models_object.execute_kw(db, uid, password,
                'account.move', 'read', [rec])
            # print("============================INVOICE===================")
            # print('record',[record])
            # print("============================INVOICE ITEMS===================")
            items = models_object.execute_kw(db, uid, password,
                    'account.move.line', 'search_read',
                    [[['move_name', '=', record['name']]]],
                    # {'fields': ['name', 'move_id','quantity', 'price_total', 'price_unit', 'discount', 'tax_base_amount']}
                    )
            # print(items)

    except Exception as err:
        # Print any error messages to stdout
        print(err)
    return invoices_list


# define a function to
# convert a simple dictionary
# of key/value pairs into XML
def GenerateXML(request_json) :
    fileName = 'Invoices.xml'
    try:
        invoices_list = Get_InvoiceData()
        xml_data = xml_generator(invoices_list)
    except Exception as err:
        print(err)

    return xml_data

# Driver Code
if __name__ == "__main__": 
    application.run(host='0.0.0.0', debug=True)
    # GenerateXML("Catalog.xml")