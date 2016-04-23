import numpy as np
from sklearn import linear_model

def fitModel(dataSet): #the dataSet must be normalized
		
	# Create linear regression object
	regr = linear_model.LinearRegression()

	# Train the model using the training sets
	regr.fit(dataSet[0], dataSet[1])

	return regr
	
