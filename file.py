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