from flask import Flask,render_template,request,session
import pandas as pd

from engine import process

app = Flask(__name__)
app.secret_key = 'A7x2bL#8pK9!'

@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        file = request.files['csvFile']
        session['file_name'] = file.filename
        file.save(f'static\data\{file.filename}')
        vals = process(session['file_name'])
        return render_template('display.html', table = vals['table'],table_name = vals['table_name'],data = vals['data'])
            
    else:
        return render_template('index.html')

@app.route('/data_clean')
def cleaning():
    return render_template('clean.html')

@app.route('/fill_missing')
def fill_missing():
    return render_template('fill_missing.html')

@app.route('/encode_features')
def encode_features():
    return render_template('encode_features.html')

@app.route('/scale_normalize')
def scale_normalize():
    return render_template('scale_normalize.html')

if __name__ == '__main__':
    app.run(debug = True)
