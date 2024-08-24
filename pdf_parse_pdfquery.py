import pandas as pd
import pdfquery

file = "assets/request.pdf"

# #read the PDF
pdf = pdfquery.PDFQuery(file)
pdf.load()

pdf.pq('LTTextLineHorizontal:contains("Customer")')

left_corner = 37.0
bottom_corner = 333.777
name = pdf.pq(f'LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner, bottom_corner-30, left_corner+150, bottom_corner)).text()
name

#convert the pdf to XML
pdf.tree.write('customers.xml', pretty_print = True)
pdf
...

