import json
import urllib2
import pandas as pd
from pandas.io.json import json_normalize
from pprint import pprint

docket_endpoint = "https://api.data.gov/regulations/v3/docket.json?"
document_endpoint = "https://api.data.gov/regulations/v3/documents.json?"
api_key = "1XZff8WqSe32dEApK208iOAWYzJ47O4uTBb2ZS03"
results_per_page = 1000
url = document_endpoint + "&api_key=" + api_key + "&a=EERE&rpp=" + str(results_per_page)


def buildDataframe():

	json_obj = urllib2.urlopen(url)
	data = json.load(json_obj)

	number_of_pages = data['totalNumRecords'] / results_per_page

	df = pd.DataFrame(json_normalize(data['documents']))

	for page in range(1,number_of_pages+2):
		page_offset = (page-1) * results_per_page
		urlp = url + "&po=" + str(page_offset)
		
		json_obj = urllib2.urlopen(urlp)
		data = json.load(json_obj)
		
		df = df.append(pd.DataFrame(json_normalize(data['documents'])))

	return df

def subsetProduct(df):

	all_product_docs = df[df['docketTitle'].str.contains(product_name, case=False) == True]
	return all_product_docs

def docsByChrono():
	void
def docsByDoctype():
	void
def getCurrentRuleState():
	void
def getLastFinalRuleEffDate():
	void

if __name__ == "__main__":

	df = buildDataframe()
	
	subset = subsetProduct(df)

	print subset.docketTitle.unique()

#df.to_csv("temp.csv", encoding="utf-8")




