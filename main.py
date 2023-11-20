from flask import Flask,render_template,request
import pandas as pd

app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        file = request.files['csvFile']
        df = pd.read_csv(file)
        top_rows = df.head()
        bottom_rows = df.tail()
        top_rows_html = top_rows.to_html(classes='table table-striped', index=False)
        bottom_rows_html = bottom_rows.to_html(classes='table table-striped', index=False)
        return render_template('index.html', display = True, top_rows_html = top_rows_html, bottom_rows_html = bottom_rows_html)

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)
