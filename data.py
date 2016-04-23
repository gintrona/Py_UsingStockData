from lxml.cssselect import CSSSelector
import re
import numpy as np

def extractValues(tree):

	dictData= {}

	################
	#Stock data
	################
	sel 	= CSSSelector('.valoresCotizacion > div:nth-child(1) > div:nth-child(1) > h2:nth-child(1) > a:nth-child(1)')
	element = sel(tree)
	currentPrice 		= re.findall('[0-9,]+' ,element[0].text)
	dictData['currentPrice']= float(re.sub(',' ,'.' , currentPrice[0]));

	################
	#Technical data
	################

	sel = CSSSelector('.datos')

	element 	= sel(tree) #returns th
	trHead 		= element[1].getparent() #returns tr
	siblings 	= iter([sibling for sibling in trHead.itersiblings() ])  #each sibling is a tr

	while True:
		try:
			list_tds = iter(siblings.next().getchildren())
			while True:
				try:
					label = re.findall( '[A-Za-z%_/()]+' , list_tds.next().text)
					value = re.findall( '[0-9%()\.,]+' , list_tds.next().text)
					if label:
						dictData[label[0]] = float(re.sub(',' ,'.' , \
									 re.sub('\.','',value[0]))) if value else "NN"; 
					else:
						0					
				except StopIteration:
					break
		except StopIteration:
			break
		
	return dictData

##
##
##

def buildDataSet(diccSpecies):

	nb_features = 9
	index=0
	keys  	= diccSpecies.keys()
	print keys
	data_y 	= np.zeros( len(keys) )
	data_X 	= np.zeros( (len(keys) , nb_features))
	
	for elem in keys:
		feature_vector = np.array([])
		raw_feature_vector = [diccSpecies[elem]['ROE(%)'],\
					diccSpecies[elem]['Beta'],\
					diccSpecies[elem]['P/BV'],\
					diccSpecies[elem]['Rtado'],\
					diccSpecies[elem][u'Capitalizaci'],\
					diccSpecies[elem]['P/E'],\
					diccSpecies[elem]['EBITDA'],\
					diccSpecies[elem]['P/Ventas'],\
					diccSpecies[elem]['Ventas']]
		for speci in range(len(raw_feature_vector)):
			feature_vector=np.append(feature_vector, raw_feature_vector[speci] if raw_feature_vector[speci] is not 'NN' else 0)

		data_X[index, :] = feature_vector
		data_y[index] 	 = diccSpecies[elem]['currentPrice']
		index = index+1

	return {'X':data_X, 'y':data_y}

def getSelectedStocks():
	return ['AGRO',
'ALUA', 
'APBR',
'AUSO',
'BHIP',
'BMA',
'BOLT',
'BPAT',
'BRIO',
'BRIO6',
'CADO',
'CAPU',
'CAPX',
'CARC',
'CECO2',
'CELU',
'CGPA2', 
'COLO',
'COME',
'CRES',
'CTIO',
'DGCU2',
'DYCA',
'EDN',
'ERAR',
'ESME',
'FERR',
'FIPL',
'FRAN',
'GARO',
'GBAN',
'GCLA',
'GGAL',
'GRIM',
'INAG',
'INDU',
'INTR',
'INVJ',
'IRSA',
'JMIN',
'LEDE',
'LONG',
'METR',
'MIRG',
'MOLI',
'MORI',
'OEST',
'PAMP',
'PATA',
'PATY',
'PESA',
'PETR',
'POLL',
'PSUR',
'REP',
'RIGO',
'ROSE',
'SAMI',
'SEMI',
'STD',
'TECO2', 
'TEF',
'TGLT',
'TGNO4',
'TGSU2',
'TRAN',
'TS',
'YPFD'
]

