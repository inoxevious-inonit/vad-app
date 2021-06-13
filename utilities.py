import os
import xmlrpc.client

url = 'https://training-gunnar.odoo.com'
db = 'training-gunnar'
username = 'innocent.mpasi@inonit.no'
password = 'Sanna@1#'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# common.version()
# print(common.version())
uid = common.authenticate(db, username, password, {})
print('uuid', uid)
models_object = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))