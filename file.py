ET.register_namespace('', "http://www.dnbnorfinans.no/Factoring/2004")

schema_tree = ET.parse('schema.xml')
root = schema_tree.getroot()
sampple_schems = ET.parse('factoring448000.xml')
sample_root = sampple_schems.getroot()

invoice_tree = ET.parse('Invoice.xml')
invoice_root = invoice_tree.getroot()
batch = invoice_root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch")


TransferDateTime =  invoice_root.find("./{http://www.dnbnorfinans.no/Factoring/2004}TransferDateTime")
TransferDateTime.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

ClientId =  invoice_root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}ClientId")
print('ClientId', ClientId)
ClientId.text = '09891'

ClientName =  invoice_root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}ClientName")
ClientName.text = 'VAD AS'

BatchDate =  invoice_root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}BatchDate")
BatchDate.text = datetime.now().strftime("%Y-%m-%d")

invoice_element = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice")
print("invoice to be appended",invoice_element)
invoices_list = [25, 27, 34]
# debtors =    models_object.execute_kw(db, uid, password,
# 'res.partner', 'search_read',
# []
# # ,{'fields': ['name', 'country_id', 'comment']}
# )

for rec in invoices_list:
	record = models_object.execute_kw(db, uid, password,
		'account.move', 'read', [rec])
	for invoice in record:
		print('dsop',invoice['invoice_partner_display_name'])
		partner_id = invoice['commercial_partner_id'][0]
		debtors = models_object.execute_kw(db, uid, password,
		'res.partner', 'search_read',
		[[['commercial_partner_id', '=', partner_id ]]]
		# ,{'fields': ['name', 'country_id', 'comment']}
		)
		sales = models_object.execute_kw(
			db, uid, password, 'sale.order', 'search_read',
			[[['partner_invoice_id', '=', partner_id ]]]
			)
		items = models_object.execute_kw(db, uid, password,
				'account.move.line', 'search_read',
				[[['move_name', '=', invoice['name']]]],
				# {'fields': ['name', 'move_id','quantity', 'price_total', 'price_unit', 'discount', 'tax_base_amount']}
				)
		for invoice_tag in invoice_element:
			# print('tags', invoice_tag.tag)
			if invoice_tag.tag =='{http://www.dnbnorfinans.no/Factoring/2004}InvType':
				invoice_tag.text = 'Invoice' 
			if invoice_tag.tag =='{http://www.dnbnorfinans.no/Factoring/2004}InvCcy':
				invoice_tag.text = 'NOK' 
			if invoice_tag.tag =='{http://www.dnbnorfinans.no/Factoring/2004}Debtor':

				Debtor_element = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorName")
				print('debt eleme', Debtor_element.tag)
				Debtor_n_element = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorName")
				print(Debtor_n_element.text)
				# print('debtors', debtors)
				for debtor in debtors:
					# print('debtttt', debtor)
					if debtor['name'] == invoice['invoice_partner_display_name']:
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorName")
						debtor_tag.text = debtor['name']
						
						
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}ClientDebtorNbr")
						debtor_tag.text = str(debtor['id'])
						
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorVATNbr")
						debtor_tag.text = debtor['vat']
						
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorPostalAddr")
						debtor_tag.text = debtor['contact_address']
						
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorSuplAddr")
						debtor_tag.text = debtor['contact_address']
						
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorPostalCode")
						debtor_tag.text = debtor['zip']
						
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorCity")
						debtor_tag.text = debtor['city']
						
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorCtryCode")
						debtor_tag.text = invoice['country_code']
						
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorPhone")
						debtor_tag.text = debtor['phone']
						
						
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorMobile")
						debtor_tag.text = debtor['phone']
						
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorEmail")
						debtor_tag.text = debtor['email']
						
						debtor_tag = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Debtor/{http://www.dnbnorfinans.no/Factoring/2004}DebtorRef")
						debtor_tag.text = debtor['name']
		
					
				for sale_data in sales:
					# print('sale_data', sale_data)
					# print("sale_data['partner_id'][1]", sale_data['partner_id'][1])
					# print("invoice['invoice_partner_display_name']", invoice['invoice_partner_display_name'])
					
					if sale_data['partner_id'][1] == invoice['invoice_partner_display_name']:
						delivery_tags = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryDetails/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryName")
						delivery_tags.text = sale_data['client_order_ref']
						delivery_tags = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryDetails/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryAddr")
						delivery_tags.text = debtor['contact_address_complete']
						delivery_tags = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryDetails/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryPostalCode")
						delivery_tags.text = debtor['zip']
						delivery_tags = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryDetails/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryCity")
						delivery_tags.text = debtor['city']
						delivery_tags = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryDetails/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryCtryCode")
						delivery_tags.text = invoice['country_code']
						delivery_tags = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryDetails/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryDate")
						delivery_tags.text = sale_data['commitment_date']
						delivery_tags = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryDetails/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryType")
						delivery_tags.text = sale_data['type_name']
						delivery_tags = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryDetails/{http://www.dnbnorfinans.no/Factoring/2004}DeliveryTerms")
						delivery_tags.text = sale_data['type_name']

			if invoice_tag.tag =='{http://www.dnbnorfinans.no/Factoring/2004}InvoiceHeader':
				InvRef = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}InvoiceHeader/{http://www.dnbnorfinans.no/Factoring/2004}InvRef")
				InvRef.text = invoice['ref'] 
				InvNbr = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}InvoiceHeader/{http://www.dnbnorfinans.no/Factoring/2004}InvNbr")
				InvNbr.text = str(invoice['id'])
				InvDate = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}InvoiceHeader/{http://www.dnbnorfinans.no/Factoring/2004}InvDate")
				InvDate.text = str(invoice['invoice_date'] )
				DueDate = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}InvoiceHeader/{http://www.dnbnorfinans.no/Factoring/2004}DueDate")
				DueDate.text = str(invoice['invoice_date_due'])   
				PmtTermsText = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}InvoiceHeader/{http://www.dnbnorfinans.no/Factoring/2004}PmtTerms/{http://www.dnbnorfinans.no/Factoring/2004}PmtTermsText")
				PmtTermsText.text = str(invoice['invoice_payment_term_id'])

				# ValueDate = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}InvoiceHeader/{http://www.dnbnorfinans.no/Factoring/2004}ValueDate")
				# ValueDate.text = invoice['invoice_partner_display_name']

				OrderRef = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}InvoiceHeader/{http://www.dnbnorfinans.no/Factoring/2004}OrderRef")
				OrderRef.text = invoice['ref']

				Kid = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}InvoiceHeader/{http://www.dnbnorfinans.no/Factoring/2004}Kid")
				Kid.text = str(invoice['partner_id'])
			for item in items:
				ItemId = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Items/{http://www.dnbnorfinans.no/Factoring/2004}OrderDetails/{http://www.dnbnorfinans.no/Factoring/2004}Item/{http://www.dnbnorfinans.no/Factoring/2004}ItemId")
				ItemId.text = str(item['id'])

				ItemDescr = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Items/{http://www.dnbnorfinans.no/Factoring/2004}OrderDetails/{http://www.dnbnorfinans.no/Factoring/2004}Item/{http://www.dnbnorfinans.no/Factoring/2004}ItemDescr")
				ItemDescr.text = str(item['display_name'])

				NbrOfUnits = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Items/{http://www.dnbnorfinans.no/Factoring/2004}OrderDetails/{http://www.dnbnorfinans.no/Factoring/2004}Item/{http://www.dnbnorfinans.no/Factoring/2004}NbrOfUnits")
				NbrOfUnits.text = str(item['quantity'])
				
				UnitPrice = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Items/{http://www.dnbnorfinans.no/Factoring/2004}OrderDetails/{http://www.dnbnorfinans.no/Factoring/2004}Item/{http://www.dnbnorfinans.no/Factoring/2004}UnitPrice")
				UnitPrice.text = str(item['price_unit'])

				DiscPercent = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Items/{http://www.dnbnorfinans.no/Factoring/2004}OrderDetails/{http://www.dnbnorfinans.no/Factoring/2004}Item/{http://www.dnbnorfinans.no/Factoring/2004}DiscPercent")
				DiscPercent.text = str(item['discount'])

				Amt = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Items/{http://www.dnbnorfinans.no/Factoring/2004}OrderDetails/{http://www.dnbnorfinans.no/Factoring/2004}Item/{http://www.dnbnorfinans.no/Factoring/2004}Amt")
				Amt.text = str(item['price_total'])

				VATPct = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Items/{http://www.dnbnorfinans.no/Factoring/2004}OrderDetails/{http://www.dnbnorfinans.no/Factoring/2004}Item/{http://www.dnbnorfinans.no/Factoring/2004}VATPct")
				VATPct.text = str(item['tax_ids'])

			NetAmt = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Total/{http://www.dnbnorfinans.no/Factoring/2004}NetAmt")
			NetAmt.text = str(invoice['amount_untaxed']) 

			VATAmt = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Total/{http://www.dnbnorfinans.no/Factoring/2004}VATAmt")
			VATAmt.text = str(invoice['amount_tax'])  

			TotalAmt = root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}Total/{http://www.dnbnorfinans.no/Factoring/2004}TotalAmt")
			TotalAmt.text = str(invoice['amount_total'])

	print('invoice name',invoice['invoice_partner_display_name'])
	batch.append(invoice_element)
	print("invoice appended",invoice_element)
xml_file = 'invoices-' + str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S")) + '.xml'
invoice_tree.write(xml_file)




        fileName = 'Invoices.xml'
        print(request_json)
        root = gfg.Element("Catalog")
        
        m1 = gfg.Element("mobile")
        root.append (m1)
        
        b1 = gfg.SubElement(m1, "brand")
        b1.text = "Redmi"
        b2 = gfg.SubElement(m1, "price")
        b2.text = "6999"
        
        m2 = gfg.Element("mobile")
        root.append (m2)
        
        c1 = gfg.SubElement(m2, "brand")
        c1.text = "Samsung"
        c2 = gfg.SubElement(m2, "price")
        c2.text = "9999"
        
        m3 = gfg.Element("mobile")
        root.append (m3)
        
        d1 = gfg.SubElement(m3, "brand")
        d1.text = "RealMe"
        d2 = gfg.SubElement(m3, "price")
        d2.text = "11999"
        
        tree = gfg.ElementTree(root)
        
        with open (fileName, "wb") as files :
            file = tree.write(files)





for key, val in invoice.items():
    # create an Element
    # class object
    if key == 'invoice_date':
        child = ET.SubElement(invoice_tag,'InvcDt')
        child.text = str(val)
        # invoice_tag.append(child)
    if key == 'amount_total':
        child = ET.SubElement(invoice_tag,'AmtTtl')
        child.text = str(val)
        # invoice_tag.append(child)
    if key == 'invoice_date_due':
        child = ET.SubElement(invoice_tag,'InvcDtDue')
        child.text = str(val)
        # invoice_tag.append(child)

    for a in invoices:
        root = gfg.Element("Data")
        current_inv = 't'+str(a['id'])
        
        print('invoice id',current_inv)
        current_inv = gfg.Element("invoice")
        root.append (current_inv)

        b1 = gfg.SubElement(current_inv, "invoice_date")
        b1.text = str(a['invoice_date'])
        b2 = gfg.SubElement(current_inv, "amount_total")
        b2.text = str(a['amount_total'])
        
        tree = gfg.ElementTree(root)
            
        with open (fileName, "wb") as files :
            file = tree.write(files)


# print(ET.tostring(root, encoding='utf8').decode('utf8'))

# print('attrib', root.attrib)
# for child in root:
#     print(child.tag, child.attrib)
# [print(elem.text )for elem in root.iter('{http://www.dnbnorfinans.no/Factoring/2004}VATAmt')]
# print(ET.tostring(root, encoding='utf8').decode('utf8'))
# for movie in root.iter('4233.18'):
#     print('OrderDetails',movie.attrib)

# [print("ele",elem.attrib ) for elem in root.findall('4233.18')]

# for invoice in root.find("./{http://www.dnbnorfinans.no/Factoring/2004}Batch/{http://www.dnbnorfinans.no/Factoring/2004}Invoice/{http://www.dnbnorfinans.no/Factoring/2004}InvType"):
# 	print("invoice",invoice.text)
# 	invoice.text = 'Invoiced'
# 	print("invoice",invoice.text)

# invoice.text = 'Inovice'

# [print(elem.text )for elem in root.iter('{http://www.dnbnorfinans.no/Factoring/2004}ItemId')]

[print("ele",elem.attrib ) for elem in root.findall('4233.18')]
