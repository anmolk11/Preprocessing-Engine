from flask import Flask,render_template,request
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        file = request.files['csvFile']
        return process(file)
    else:
        return render_template('index.html')

def highlighter(x):
    if x['Num of Missing Values'] > 0:
        return ['background-color: pink'] * 4
    else:
        return ['background-color: white'] * 4

def process(file):
    file_name = file.filename
    df = pd.read_csv(file)
    cols = df.columns
    cats = []
    for i in cols:
        if df[i].dtype == 'int64':
            cats.append('Numerical / Discrete')
        elif df[i].dtype == 'float64':
            cats.append('Numerical / Continues')
        else:
            cats.append('Categorical')
    
    data_miss = df.isna().sum()
    num_miss = data_miss.values
    perc_miss = np.round(num_miss / df.shape[0] * 100,2)
    table_df = df.head().to_html(index = False, classes = 'table table-striped')


    data = {
        'Feature' : cols,
        'Category' : cats,
        'Num of Missing Values' : data_miss,
        '% of Missing Values' : perc_miss
    }
    data_df = pd.DataFrame(data)
    # data_df = data_df.to_html(index = False, classes = 'table table-striped')
    styled_df = data_df.style.apply(highlighter, axis = 1)
    styled_df.relabel_index(range(1,len(num_miss) + 1))
    data_df = styled_df.to_html(index = False,classes = 'table table-striped')
    return render_template('display.html', table = table_df,table_name = file_name,data = data_df)


if __name__ == '__main__':
    app.run(debug = True)
