from flask import Flask,render_template,request,session
import pandas as pd
import atexit


from engine import *
from cleanup import cleanup_folder

atexit.register(cleanup_folder)

app = Flask(__name__)
app.secret_key = 'A7x2bL#8pK9!'

@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        file = request.files['csvFile']
        session['file_name'] = file.filename
        file.save(f'static\data\{file.filename}')
        vals = process(session['file_name'])
        miss = {
            'Feature' : [],
            'Category' : [],
            'Missing' : []
        }
        for f,c,v in zip(vals['Feature'],vals['Category'],vals['% of Missing Values']):
            if v > 0:
                miss['Feature'].append(f)
                miss['Category'].append(c)
                miss['Missing'].append(v)
        session['miss_info'] = miss
        return render_template('display.html', table = vals['table'],table_name = vals['table_name'],data = vals['data'])
            
    else:
        return render_template('index.html')

@app.route('/data_clean')
def cleaning():
    return render_template('clean.html')

@app.route('/fill_missing')
def fill_missing():
    df = pd.DataFrame(session['miss_info'])
    df.sort_values(by = 'Missing',ascending = False,inplace = True)
    df_html = df.to_html(index = False)
    prompt_data = []
    for feat,cat in zip(session['miss_info']['Feature'],session['miss_info']['Category']):
        if cat == 'Categorical' or cat == 'Binary':
            prompt = {
                'question' : feat,
                'options' : ['Drop the Feature','Fill with Mode']
            }
        else:
            prompt = {
                'question' : feat,
                'options' : ['Drop the feature','Fill with Mean','Fill with Median']
            }
        prompt_data.append(prompt) 
    return render_template('fill_missing.html',data = df_html,prompt_data = prompt_data)

@app.route('/process_fill_missing',methods=['POST'])
def process_fill_missing():
    selected_values = {}
    for question in request.form:
        selected_values[question] = request.form[question]

    # Process the selected values as needed
    source = fill_missing_vals(selected_values,session['file_name'])
    return render_template('download.html',file_name = source)


@app.route('/encode_features')
def encode_features():
    return render_template('encode_features.html')

@app.route('/scale_normalize')
def scale_normalize():
    return render_template('scale_normalize.html')

# ----------------------------- Testing area -----------------------------------------------


if __name__ == '__main__':
    app.run(debug = True)
    # os.remove(f"static\data\{session['file_name']}")
