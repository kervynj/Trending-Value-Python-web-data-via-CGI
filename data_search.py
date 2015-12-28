#!/usr/bin/python
import cgi
import csv
import cgitb; cgitb.enable()

print "Content-Type: text/html\n"
#Get requested company from user form input
form = cgi.FieldStorage()
ticker = form.getvalue('ticker')

if ".to" in ticker:
	#Open  TSX daily data
	TSX_object = open('TSX_master.csv','rU')
	TSX_data = csv.reader(TSX_object)

	data = []

	#Search File for requested company
	for row in TSX_data:
		data.append(row)
	for row in data:
		if row[0] == ticker:
			retrieved_values = row
			break
else:
	#Open  NYSE daily data
	NYSE_object = open('NYSE_master.csv','rU')
	NYSE_data = csv.reader(NYSE_object)

	data = []

	#Search File for requested company
	for row in NYSE_data:
		data.append(row)
	for row in data:
		if row[0] == ticker.upper():
			retrieved_values = row
			break
try:
	retrieved_values
except NameError:
	print """<p>Invalid Ticker Entry</p>"""
else:
	print """
		<p>
		<strong>Company:</strong>          %s<br><strong>Overall Rank:</strong>     %s<br><strong>6 Month Change:</strong>   %s<br>Price/Earning:    %s<br>Price/Sales:	  %s<br>Price/Book:		  %s<br>Dividend Yield:   %s<br>Market Cap/EBITDA %s
		</p> """ %(retrieved_values[1],retrieved_values[2],retrieved_values[3],retrieved_values[4],retrieved_values[5],retrieved_values[6],retrieved_values[7],retrieved_values[8])
	
	
