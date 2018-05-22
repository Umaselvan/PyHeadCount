from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask.templating import render_template
from werkzeug.utils import secure_filename
import os

import pandas as pd

UPLOAD_FOLDER = os.path.expanduser('~') 
#str(pathlib.Path.home())
#os.path.expanduser('~') 
# 'C:/Users/L. RAMYA/'
ALLOWED_EXTENSIONS = set(['xlsx', 'xls', 'csv'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '64357e3c28259bf2fc08c4491bc1d0f0'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/headcount', methods = ['GET', 'POST'])
def main():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash(u'No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash(u'No selected file', 'error')
            return redirect(request.url)
        if file and not allowed_file(file.filename):
            flash(u'Please upload a valid excel document', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # xlsx = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))            
            # return render_template("tableview.html", tables = [xlsx.to_html()])
            return redirect(url_for('table_view', filename=filename))
            
    return render_template("index.html")

@app.route('/table/<filename>')
def table_view(filename):
    xlsx = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("tableview.html", tables = [xlsx.to_html(classes=["table-bordered", "table-striped", "table-hover"])])


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(debug=True)

