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

document_fields = ["docketId", "docketTitle", "rin", "documentId", "frNumber", "documentType", "title", "postedDate", "openForComment"]

def buildDataFrame():

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

def subsetProduct(df, product_name):
	all_product_docs = df[df['docketTitle'].str.contains(product_name, case=False) == True]
	all_product_docketIds = pd.DataFrame(all_product_docs["docketId"].unique())
	all_product_docs["postedDate"] = pd.to_datetime(all_product_docs["postedDate"])
	all_product_docs.sort("postedDate", inplace=True, ascending=False)

	TP_dockets = all_product_docketIds[0][all_product_docketIds[0].str.contains("TP", case=False) == True]
	STD_dockets = all_product_docketIds[0][all_product_docketIds[0].str.contains("STD", case=False) == True]
	return all_product_docs, STD_dockets, TP_dockets

# Return dataframe of docket information
def docketInfo(docketIds):

	cols = ["title", "agendaStageOfRulemaking", "rin", "cfrCitation"]
	docket_info = pd.DataFrame(index=docketIds, columns=cols)

	for ID in docketIds:
		url = docket_endpoint + "&api_key=" + api_key + "&docketId=" + ID
		json_obj = urllib2.urlopen(url)
		data = json.load(json_obj)

		#docket_html_link = "<a href='{{ url_for(docket-info/" + data["docketId"] +")'>" + data["docketId"] + "</a>"

		docket_info["title"].ix[ID] = data["title"]
		docket_info["agendaStageOfRulemaking"].ix[ID] = data["agendaStageOfRulemaking"]["value"]
		docket_info["rin"].ix[ID] = data["rin"]
		docket_info["cfrCitation"].ix[ID] = data["cfrCitation"]

	docket_info = docket_info.to_html()

	return docket_info



# Returns the rulemaking stage for a docketId.
def getRuleStage(docketId):
 	url = docket_endpoint + "&api_key=" + api_key + "&docketId=" + docketId
	json_obj = urllib2.urlopen(url)
	data = json.load(json_obj)
 	rule_stage = data["agendaStageOfRulemaking"]["value"]

 	return rule_stage

def docsByDocketChrono(all_product_docs):
	
	DOE_docs = all_product_docs[(all_product_docs["documentType"] == "Rule") | (all_product_docs["documentType"] == "Proposed Rule") | (all_product_docs["documentType"] == "Notice") | ((all_product_docs["documentType"] == "Supporting & Related Material") & (all_product_docs["title"].str.contains("technical support document", case=False) == True))]
	DOE_docs.sort(["docketId","postedDate"], ascending=[False,False], inplace=True)

	return DOE_docs[document_fields].to_html()


def getDocsByDocType(all_product_docs, docketId=None):
	
	if docketId != None:
		tsds = all_product_docs[(all_product_docs["docketId"] == docketId) & (all_product_docs["documentType"] == "Supporting & Related Material") & (all_product_docs["title"].str.contains("technical support document", case=False) == True)]
		final_rules = all_product_docs[(all_product_docs["docketId"] == docketId) & (all_product_docs["documentType"] == "Rule") ]
		noprs = all_product_docs[(all_product_docs["docketId"] == docketId) & (all_product_docs["documentType"] == "Proposed Rule") ]
		other_notices = all_product_docs[(all_product_docs["docketId"] == docketId) & (all_product_docs["documentType"] == "Notice") ]

	else:
		tsds = all_product_docs[(all_product_docs["documentType"] == "Supporting & Related Material") & (all_product_docs["title"].str.contains("technical support document", case=False) == True)]
		final_rules = all_product_docs[all_product_docs["documentType"] == "Rule"]
		noprs = all_product_docs[all_product_docs["documentType"] == "Proposed Rule"]
		other_notices = all_product_docs[all_product_docs["documentType"] == "Notice"]


	return final_rules[document_fields].to_html(), noprs[document_fields].to_html(), other_notices[document_fields].to_html(), tsds[document_fields].to_html()
	
# Takes the dataframe of all documents related to product, sorts by "postedDate", 
# and returns the "docketId" for the most recent document.
def getLatest(product_docs):
	
	latest_docket = product_docs["docketId"].iloc[0]
	latest_postedDate = product_docs["postedDate"].iloc[0].strftime('%b %d, %Y')

	return latest_docket, latest_postedDate

	
def getLastFinalRuleEffDate():
	void

if __name__ == "__main__":

	df = buildDataframe()
	
	

#df.to_csv("temp.csv", encoding="utf-8")




