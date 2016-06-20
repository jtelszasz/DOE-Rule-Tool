from flask import Flask, render_template, request, url_for, app
app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def index():

    if request.method == 'POST':
    	return show_product_history(request.form['product'])

    return render_template('index.html')

@app.route('/products', methods=['POST'])
def show_product_history():
	product = request.form['product']
	return render_template('product.html', product=product)

with app.test_request_context():
	url_for('static', filename='style.css')
	url_for('show_product_history', product='asdf')

'''
# Run the app :)
if __name__ == '__main__':
  app.run( 
        host="0.0.0.0",
        port=int("80")
  )
'''