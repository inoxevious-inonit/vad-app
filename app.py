import xml.etree.ElementTree as gfg 
import sys, os,json
from datetime import datetime
from optparse import OptionParser
import random

from flask import Flask,request, url_for, redirect, render_template, jsonify, abort
import requests
from xmlrpc.server import SimpleXMLRPCServer
import wget
import xmlrpc.client
from xml.etree.ElementTree import Element,tostring
from xml.etree import ElementTree as ET
from generate_xml import GenerateXMLFile as xml_generator
from generate_pdf import generate_pdf
from generate_for_vat_pdf import generate_for_vat_pdf
from utilities import *
from flask import send_from_directory,send_file

# create  
application = Flask(__name__, template_folder='templates')
# get_file()

@application.route("/")
def hello():
    return "Hello VAD"

# ----------------------------------------INVOICE XML BUNDLE START---------------------------------------

@application.route('/api/export_xml', methods=['GET','POST'])
def get_xml_file():
    # request_json = request.get_json()("{",
    request_json = request.args.get("records")
    ids = clean_response(request_json)
    print('ids', ids)
    xml_file_name = generate_xml(ids)
    print('xml_file_name', xml_file_name)
    if xml_file_name is None:
        self.Error(400)
    try:
        return send_file(xml_file_name, as_attachment=True, download_name='Invoice_file.xml')
        # return send_from_directory(directory=full_path, filename=fileName)
    except Exception as e:
        return render_template("index.html", message=e)
        
# Generate xml
def generate_xml(ids):
    try:
        xml_file_name = xml_generator(ids)
    except Exception as err:
        print(err)
    return xml_file_name

# ----------------------------------------INVOICE XML BUNDLE END---------------------------------------


# -------------------------------------Factoring PDF Invoice START-----------------------------------------

@application.route('/api/export_pdf', methods=['GET','POST'])
def get_pdf_file():
    request_json = request.args.get("records")
    ids = clean_response(request_json)
    print('ids', ids)
    pdf_file_name = generate_pdf_bundle(ids)
    # print('pdf_file_name', pdf_file_name)
    if pdf_file_name is None:
        self.Error(400)
    try:
        return send_file(pdf_file_name, as_attachment=True, download_name='Invoice_file.pdf')
        # return send_from_directory(directory=full_path, filename=fileName)
    except Exception as e:
        return render_template("index.html", message=e)
    

# Generate pdf
def generate_pdf_bundle(ids) :
    try:
        invoice_dictionary = generate_invoice_dictionary(ids)

        # print('invoice_dictionary pdf', invoice_dictionary)
        
        invoice_json_file = write_dict_to_json(invoice_dictionary)
        pdf_file_name =    generate_invoice_pdf(invoice_json_file)
        print('pdf_file_name', pdf_file_name)
    except Exception as err:
        print(err)
    return pdf_file_name
# -------------------------------------Factoring Invoice  PDF END-----------------------------------------

# ----------------------------------------FOR VAT INVOICE BUNDLE START-----------------------------------------


@application.route('/api/export_for_vat_invoices_pdf', methods=['GET','POST'])
def get_vat_invoices_pdf_file():
    request_json = request.args.get("records")
    ids = clean_response(request_json)
    print('ids', ids)
    for_vat_pdf_file_name = generate_for_vat_invoices_pdf_bundle(ids)
    # print('pdf_file_name', for_vat_pdf_file_name)
    if for_vat_pdf_file_name is None:
        self.Error(400)
    try:
        return send_file(for_vat_pdf_file_name, as_attachment=True, download_name='Invoice_file.pdf')
        # return send_from_directory(directory=full_path, filename=fileName)
    except Exception as e:
        return render_template("index.html", message=e)
    

# Generate pdf
def generate_for_vat_invoices_pdf_bundle(ids) :
    try:
        invoice_dictionary = generate_invoice_dictionary(ids)
        # print('invoice_dictionary pdf', invoice_dictionary)
        
        invoice_json_file = write_dict_to_json(invoice_dictionary)
        pdf_file_name =    generate_for_vat__invoice_pdf(invoice_json_file)
        print('pdf_file_name', pdf_file_name)
    except Exception as err:
        print(err)
    return pdf_file_name
    
def generate_for_vat__invoice_pdf(invoice_json_file):
    parser = parser_options()
    options, args = parser.parse_args()
    # print('invoice_json_file in app', invoice_json_file)
    try:
        pdf_file_name = generate_for_vat_pdf(invoice_json_file, options)
    except Exception as err:
        print(err)
    return pdf_file_name 
# ----------------------------------------INVOICE PDF BUNDLE END-----------------------------------------




def generate_invoice_dictionary(invoices_list):
    invoice_orders = []
    # create empty list
    dates_group = []
    # invoices_list = [25, 27]
    invoices_dictionary = {}
    invoices_dictionary['Bunt_nr'] = str(random.randint(0,9))[0:6]
    invoices_dictionary['Buntdato'] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    invoices_dictionary['Bunttype'] = '1'
    invoices_dictionary['Antall_bilag'] = str(len(invoices_list))
    invoices_dictionary['Valutakode_pa_konto'] = 'NOK'
    invoices_dictionary['Valutakode_for_bunten'] = ''
    invoices_dictionary['Registrert_av'] = 'Per Magne Mork'
    invoices_dictionary['Kundenr_hos_factoringselskap'] = '09891'
    invoices_dictionary['Debitor_FCI'] = '530'
    invoices_dictionary['Sendt'] = 'YES'
    invoices_dictionary['Belop'] = 0
    invoices_dictionary['total_untaxed'] = 0
    invoices_dictionary['total_tax'] = 0

    for rec in invoices_list:
        # print('rec', rec)
        record = models_object.execute_kw(db, uid, password,
            'account.move', 'read', [rec])
        for invoice in record:
            # print('invoice', invoice)
            invoice_dic = {}
            invoice_dic['invoice_id'] = invoice['id']
            invoice_dic['amount_tax'] = invoice['amount_tax']
            invoice_dic['amount_untaxed'] = invoice['amount_untaxed']
            invoice_dic['amount_total'] = invoice['amount_total']
            if invoice['invoice_payment_term_id']:
                invoice_dic['payement_terms'] = invoice['invoice_payment_term_id'][1]
            else:
                invoice_dic['payement_terms'] = invoice['invoice_payment_term_id']

            invoice_dic['invoice_date'] = invoice['invoice_date']
            dates_group.append(invoice['invoice_date'])
            invoice_dic['invoice_date_due'] = invoice['invoice_date_due']
            invoice_dic['partner_id'] = invoice['partner_id'][0]
            invoice_dic['partner_name'] = invoice['partner_id'][1]
            invoices_dictionary['total_untaxed'] = invoices_dictionary['total_untaxed'] + invoice['amount_untaxed']
            invoices_dictionary['total_tax'] = invoices_dictionary['total_tax'] + invoice['amount_tax']
            invoices_dictionary['Belop'] = invoices_dictionary['Belop'] + invoice['amount_total']
            # print('invoice_dict', invoice_dic)
            invoice_orders.append(invoice_dic)
    dates_group.sort()
    invoices_dictionary['start_date'] = dates_group[0]
    invoices_dictionary['end_date'] = dates_group[-1]

    
    invoices_dictionary['orders'] = invoice_orders
    print('dates----------------')
    print('dates----------------', dates_group[0], 'last', dates_group[-1])
    print('dates----------------')
    # print('invoice_dict invoices_dictionary', invoices_dictionary)
    return invoices_dictionary

def write_dict_to_json(invoices_dictionary):
    # Serializing json   
    # json_object = json.dumps(invoices_dictionary, indent = 4)  
    # print('invoices_dictionary json',invoices_dictionary) 
    json_file = 'invoices-' + str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S")) + '.json'
    # full_path = os.path.join(application.root_path)
    downloads = '/data'
    full_path = os.path.abspath(os.path.dirname('__file__'))
    downloads_folder = full_path + downloads
    absolute_file_path = downloads_folder + '/' + json_file
    print('absolute_file_path', absolute_file_path)

    with open(absolute_file_path, "w") as outfile: 
        json.dump(invoices_dictionary, outfile)
        
    return absolute_file_path
    

def parser_options():
    usage = "usage: runme.py [--long] myfile.json"
    parser = OptionParser(usage=usage)
    parser.add_option("-l", "--long",
                        action="store_true", dest="longformat", default=False,
                        help="Do long profile (rather than short)")
    parser.add_option("-r","--rml",
                        action="store_true", dest="saverml", default=False,
                        help="save a copy of the generated rml")
    parser.add_option("-s","--showb",
                        action="store_true", dest="showBoundary", default=False,
                        help="tuen on global showBoundary flag")
    parser.add_option("-o", "--output",
                        action="store", dest="output", default='output',
                        help="where to store result")
    options, args = parser.parse_args()
    return parser

def generate_invoice_pdf(invoice_json_file):
    parser = parser_options()
    options, args = parser.parse_args()
    # print('invoice_json_file in app', invoice_json_file)
    try:
        pdf_file_name = generate_pdf(invoice_json_file, options)
    except Exception as err:
        print(err)
    return pdf_file_name    


# helper functions

def clean_response(response):
    print('response raw', response)
    response =response.replace("{", "")
    response =response.replace("}", "")
    response =response.replace(",", " ")
    print('response cleaned', response)
    ids = [int(n) for n in response.split()]
    return ids

# Driver Code
if __name__ == "__main__": 
    application.run(host='0.0.0.0', debug=True)
    # GenerateXML("Catalog.xml")