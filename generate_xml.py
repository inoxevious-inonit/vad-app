import os
from datetime import datetime
from xml.etree import ElementTree as ET
from utilities import *
NS1 = "http://www.w3.org/2001/XMLSchema-instance" 
NS2 = "http://www.dnbnorfinans.no/Factoring/2004 FACTINV-3-0.XSD"

ET.register_namespace("xsi", NS1) 
ET.register_namespace("schemaLocation", NS2)

qname = ET.QName(NS1, "schemaLocation")    # Attribute QName


def GenerateXMLFile(invoices_list):
    xmlns_xsi = 'xmlns:xsi'
    xsi_schemaLocation = 'xsi:schemaLocation'
    now = datetime.now().time().strftime("%H:%M:%S") # time object
    date = datetime.now().strftime("%Y-%m-%d") # date object
    print("date:",date)
    print("time =", now)
    tag = 'BatchCollection'
    elem = ET.Element(tag, {'xmlns':'http://www.dnbnorfinans.no/Factoring/2004',qname: NS2}, Version="3.0", DefinedBy="DnB NOR Finans")
    # elem.set('xmlns', 'http://www.dnbnorfinans.no/Factoring/2004')
    trans_time = str(date) + 'T' + str(now)
    child = ET.Element('TransferDateTime')
    child.text = str(str(trans_time))
    elem.append(child)
    batch = ET.Element('Batch')
    elem.append(batch)

# <ClientId>09891</ClientId>
    ClientId = ET.SubElement(batch,'ClientId')
    ClientId.text = str('09891')

# ClientName
    ClientName = ET.SubElement(batch,'ClientName')
    ClientName.text = str('VAD AS')

# BatchDate
    BatchDate = ET.SubElement(batch,'BatchDate')
    BatchDate.text = str(str(date))
# BatchNbr
    BatchNbr = ET.SubElement(batch,'BatchNbr')
    BatchNbr.text = str('1')
    # get invoices list
    try:
        # get invoices list
        invoices_list = models_object.execute_kw(db, uid, password,
        'account.move', 'search',
            [[['is_move_sent', '=', False]]])
        
        # print('list',invoices_list)

        for rec in invoices_list:
            print('rec', rec)
            record = models_object.execute_kw(db, uid, password,
                'account.move', 'read', [rec])

            print("============================INVOICE===================")
            # print('record',[record])
            for invoice in record:
                print('invoice', invoice)
                print('dsop',invoice['invoice_partner_display_name'])

            # invoice tag
            invoice_tag = ET.SubElement(batch,'Invoice')
            batch.append(invoice_tag)
            # invoice type
            invoice_type = ET.SubElement(invoice_tag,'InvType')
            invoice_type.text = str('Invoice')
            # invoice currency
            invoice_type = ET.SubElement(invoice_tag,'InvCcy')
            invoice_type.text = str('NOK')

            debtors =    models_object.execute_kw(db, uid, password,
                    'res.partner', 'read',
                    [invoices_list]
                    # ,{'fields': ['name', 'country_id', 'comment']}
                    )
            print("============================debtors===================")
            # print('Debtors', debtors)
            
            for debtor in debtors:
                # print('Debtor', debtor)
                if debtor['name'] == invoice['invoice_partner_display_name']:
                   
                    # <Debtor>
                    debtor_tag = ET.SubElement(invoice_tag,'Debtor')

                    # <DebtorName>Lindbak InteriÃ¸r Oslo as</DebtorName>
                    DebtorName = ET.SubElement(debtor_tag,'DebtorName')
                    DebtorName.text = str(debtor['name'])

                    # <ClientDebtorNbr>104900</ClientDebtorNbr>
                    ClientDebtorNbr = ET.SubElement(debtor_tag,'ClientDebtorNbr')
                    ClientDebtorNbr.text = str(invoice['invoice_partner_display_name'])


                    # 
                    # <DebtorVATNbr>NO 911 106 817 MVA</DebtorVATNbr>
                    DebtorVATNbr = ET.SubElement(debtor_tag,'DebtorVATNbr')
                    DebtorVATNbr.text = str(debtor['vat'])

                    # <DebtorPostalAddr>Postboks 2435 Torgard</DebtorPostalAddr>
                    DebtorPostalAddr = ET.SubElement(debtor_tag,'DebtorPostalAddr')
                    DebtorPostalAddr.text = str(debtor['contact_address'])

                    # <DebtorSuplAddr>Ã˜stensjÃ¸veien 29</DebtorSuplAddr>
                    DebtorSuplAddr = ET.SubElement(debtor_tag,'DebtorSuplAddr')
                    DebtorSuplAddr.text = str(debtor['contact_address_complete'])

                    # <DebtorPostalCode>7005</DebtorPostalCode>
                    DebtorPostalCode = ET.SubElement(debtor_tag,'DebtorPostalCode')
                    DebtorPostalCode.text = str(debtor['zip'])

                    # <DebtorCity>TRONDHEIM</DebtorCity>
                    DebtorCity = ET.SubElement(debtor_tag,'DebtorCity')
                    DebtorCity.text = str(debtor['city'])

                    # <DebtorCtryCode>NO</DebtorCtryCode>
                    DebtorCtryCode = ET.SubElement(debtor_tag,'DebtorCtryCode')
                    DebtorCtryCode.text = str(debtor['country_id'])

                    # <DebtorPhone>22 42 22 14</DebtorPhone>
                    DebtorPhone = ET.SubElement(debtor_tag,'DebtorPhone')
                    DebtorPhone.text = str(debtor['phone'])

                    # <DebtorEmail>lindbak-kontor@lindbak.no</DebtorEmail>
                    DebtorEmail = ET.SubElement(debtor_tag,'DebtorEmail')
                    DebtorEmail.text = str(debtor['email'])

                    # <DebtorRef>Bente Scheen</DebtorRef>
                    DebtorRef = ET.SubElement(debtor_tag,'DebtorRef')
                    DebtorRef.text = str(debtor['ref'])

        # <DeliveryDetails>
                    delivery_tag = ET.SubElement(invoice_tag,'DeliveryDetails')
                    print('================================SALES===========================')
                    print('com prt', invoice['commercial_partner_id'][0])
                    partner_id = invoice['commercial_partner_id'][0]
                    sales = models_object.execute_kw(
                        db, uid, password, 'sale.order', 'search_read',
                        # []
                        [[['partner_invoice_id', '=', partner_id ]]]
                        )
                    for sale_data in sales:
                        
                        print('sales idddd', sale_data)               
                        # <DeliveryName>Lindbak InteriÃ¸r Oslo as</DeliveryName>
                        DeliveryName = ET.SubElement(delivery_tag,'DeliveryName')
                        DeliveryName.text = str(debtor['name'])

                        # <DeliveryAddr>Ã˜stensjÃ¸veien 29</DeliveryAddr>
                        DeliveryAddr = ET.SubElement(delivery_tag,'DeliveryAddr')
                        DeliveryAddr.text = str(debtor['contact_address_complete'])

                        # <DeliveryPostalCode>7005</DeliveryPostalCode>
                        DeliveryPostalCode = ET.SubElement(delivery_tag,'DeliveryPostalCode')
                        DeliveryPostalCode.text = str(debtor['zip'])

                        # <DeliveryCity>TRONDHEIM</DeliveryCity>
                        DeliveryCity = ET.SubElement(delivery_tag,'DeliveryCity')
                        DeliveryCity.text = str(debtor['city'])

                        # <DeliveryCtryCode>NO</DeliveryCtryCode>
                        DeliveryCtryCode = ET.SubElement(delivery_tag,'DeliveryCtryCode')
                        DeliveryCtryCode.text = str(debtor['zip'])

                        # <DeliveryDate>2020-11-03</DeliveryDate>
                        DeliveryDate = ET.SubElement(delivery_tag,'DeliveryDate')
                        DeliveryDate.text = str(sale_data['commitment_date'])

                        # <DeliveryType>Bring Cargo</DeliveryType>
                        DeliveryType = ET.SubElement(delivery_tag,'DeliveryType')
                        DeliveryType.text = str(sale_data['type_name'])

                        #<DeliveryTerms>DDP</DeliveryTerms>
                        DeliveryTerms = ET.SubElement(delivery_tag,'DeliveryTerms')
                        DeliveryTerms.text = str(sale_data['client_order_ref']  )


        # <InvoiceHeader>
            invoice_header_tag = ET.SubElement(invoice_tag,'InvoiceHeader')

            # <InvNbr>26738</InvNbr>
            InvNbr = ET.SubElement(invoice_header_tag,'InvNbr')
            InvNbr.text = str(invoice['name']  )

            # <InvDate>2020-11-03</InvDate>
            InvDate = ET.SubElement(invoice_header_tag,'InvDate')
            InvDate.text = str(invoice['invoice_date']  )

            # <DueDate>2020-12-03</DueDate>
            DueDate = ET.SubElement(invoice_header_tag,'DueDate')
            DueDate.text = str(invoice['invoice_date_due']  )

            # <PmtTerms>
            PmtTerms = ET.SubElement(invoice_header_tag,'PmtTerms')

            # <PmtTermsText>Netto pr 30 dager</PmtTermsText>
            PmtTermsText = ET.SubElement(PmtTerms,'PmtTermsText')
            PmtTermsText.text = str(invoice['invoice_payment_term_id']  )

            # <OrderRef>30555</OrderRef>
            OrderRef = ET.SubElement(invoice_header_tag,'OrderRef')
            OrderRef.text = str(invoice['ref']  )

            # <Kid>609891000267382</Kid>
            Kid = ET.SubElement(invoice_header_tag,'Kid')
            Kid.text = str(invoice['partner_id']  )

            # <Items>
            items_tag = ET.SubElement(invoice_tag,'Items')

            # <OrderDetails>
            order_details_tag = ET.SubElement(items_tag,'OrderDetails')
            # <Item> 
            print("============================Invoice Items===================")
    
            items = models_object.execute_kw(db, uid, password,
                    'account.move.line', 'search_read',
                    [[['move_name', '=', invoice['name']]]],
                    # {'fields': ['name', 'move_id','quantity', 'price_total', 'price_unit', 'discount', 'tax_base_amount']}
                    )
            # print('invoice items', items)

            for item in items:
                item_tag = ET.SubElement(order_details_tag,'Item')

                # <ItemId>4093sua</ItemId>
                item_id_tag = ET.SubElement(item_tag,'ItemId')
                Kid.text = str(item['id']  )

                # <ItemDescr>Santana 3-seter uten armlener</ItemDescr>
                ItemDescr = ET.SubElement(item_tag,'ItemDescr')
                ItemDescr.text = str(item['display_name']  )


                # <NbrOfUnits>1</NbrOfUnits>
                NbrOfUnits = ET.SubElement(item_tag,'NbrOfUnits')
                NbrOfUnits.text = str(item['quantity']  )


                # <UnitPrice>10727</UnitPrice>
                UnitPrice = ET.SubElement(item_tag,'UnitPrice')
                UnitPrice.text = str(item['price_unit']  )


                # <DiscPercent>55</DiscPercent>
                DiscPercent = ET.SubElement(item_tag,'DiscPercent')
                DiscPercent.text = str(item['discount']  )


                # <Amt>4827.15</Amt>
                Amt = ET.SubElement(item_tag,'Amt')
                Amt.text = str(item['price_total']  )


                # <VATPct>25</VATPct>
                VATPct = ET.SubElement(item_tag,'VATPct')
                VATPct.text = str(item['tax_base_amount']  )

                
    except Exception as err:
        print(err)

    return elem