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
# Table uses an index:
# db.valuesH.createIndex({name:1 , date:1},{unique:true})

#dataSet = data.buildDataSet(myDict)

f_errors.close()

## Analyse stage
#
# Normalize the data and store the params 
'''std_scale = preprocessing.StandardScaler().fit(dataSet['X'])
X_train_std = std_scale.transform(dataSet['X'])	

#fit the model
regressionModel = fitting.fitModel(( X_train_std , dataSet['y']) ) #return value is a model object
X_test_std = std_scale.transform(dataSet['X'][3,:])

print regressionModel.coef_ 
print myDict['APBR']['currentPrice'], " and the predicted value is ", regressionModel.predict(X_test_std) 
'''
