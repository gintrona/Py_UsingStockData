from lxml import etree
import sys
import data
from datetime import date,datetime
import fitting
from sklearn import preprocessing

#db - mongo --port 20017 to connect to shell
import pymongo
from pymongo import MongoClient

# Connect to database
connection = MongoClient('localhost', 27017)

# The db collection
db = connection.dbValues

parser = etree.HTMLParser()

# Define the list with the stock's whose data will be fetch
listStockIds = data.getSelectedStocks();#['BPAT','CRES' , 'TECO2','APBR'];

now = date.today()
currentDate = datetime(now.year,now.month,now.day,0,0)

## Open file to write errors
f_errors = open('logs', "w")

# Table uses an index:
# db.valuesH.createIndex({name:1 , date:1},{unique:true})

for elem in listStockIds:
	try:
		tree = etree.parse('http://www.puentenet.com/cotizaciones/accionesCotizaciones!getAccionPorId?id=ACCION_'+elem,parser)
		temp = {}	
		temp = data.extractValues(tree);
		temp['name'] = elem;
		temp['date'] = currentDate;
		db.valuesH.insert(temp)
		print "Stock ",elem," has been inserted"
	except Exception as e:
		f_errors.write("Error ("+str(e)+" ) occured for "+elem+"\n----\n")
	
# The resulting dataSet is a dict with keys X:training dataSet and y:targetValues

f_errors.close()

## Analyse stage

