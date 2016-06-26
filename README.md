# Py_UsingStockData

The purpose of this code to retrieve relevant financial information for a selected set of assets specified in 
a list in data.py (getSelectedStocks). Each element contains the code that identifies an asset in the Buenos Aires' Stock Exchange.
For each of those elements we fetch a page html (from www.puentenet.com) that displays the corresponding information, parse it and 
extract the information of interest. 

The data is then saved in a local mongo DB. 

The final goal is to analyze this data in order to determine whether an asset is under or overrated.

The program is scheduled (it's actually a cron job) to be launched when my computer boots up.
