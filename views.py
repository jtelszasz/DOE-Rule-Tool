## export FLASK_APP=views.py

from flask import Flask, render_template, request, url_for, app
import rule_info as rule
import pandas as pd
app = Flask(__name__)

df = pd.read_csv("temp.csv")
#df = rule.buildDataFrame()

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
    	return show_product_dockets(request.form['product'])
    return render_template('index.html')

@app.route('/product-dockets', methods=['POST'])
def show_product_dockets():

  product_name = request.form['product']
  
  product_docs, STD_dockets, TP_dockets = rule.subsetProduct(df, product_name)
  final_rules, noprs, other_notices, tsds = rule.getDocsByDocType(product_docs)

  latest_STD_docket, latest_STD_postedDate = rule.getLatest(product_docs[product_docs["docketId"].str.contains("STD",case=False) == True])
  latest_TP_docket, latest_TP_postedDate = rule.getLatest(product_docs[product_docs["docketId"].str.contains("TP",case=False) == True])
  latest_STD_stage = rule.getRuleStage(latest_STD_docket)
  latest_TP_stage = rule.getRuleStage(latest_TP_docket)

  STD_docket_info = rule.docketInfo(STD_dockets)
  TP_docket_info = rule.docketInfo(TP_dockets)
  
  final_rules, noprs, other_notices, tsds = rule.getDocsByDocType(product_docs)


  DOE_docs = rule.docsByDocketChrono(product_docs)

  return render_template('product-dockets.html', product_name=product_name,
    DOE_docs=DOE_docs,
    final_rules=final_rules,
    noprs=noprs,
    other_notices=other_notices,
    tsds=tsds,
    STD_docket_info=STD_docket_info,
    TP_docket_info=TP_docket_info,
    latest_STD_docket=latest_STD_docket,
    latest_TP_docket=latest_TP_docket,
    latest_STD_postedDate=latest_STD_postedDate,
    latest_TP_postedDate=latest_TP_postedDate,
    latest_STD_stage=latest_STD_stage,
    latest_TP_stage=latest_TP_stage)

@app.route('/docket-info/<docketId>')
def show_docket_info(docketId):
  return render_template('docket.html', docketId=docketId)    

with app.test_request_context():
	url_for('static', filename='style.css')

'''
# Run the app :)
if __name__ == '__main__':
  app.run( 
        host="0.0.0.0",
        port=int("80")
  )
'''