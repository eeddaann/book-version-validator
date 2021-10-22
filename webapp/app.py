import imghdr
import os, sys
from multiprocessing import Process
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory,json,jsonify
from werkzeug.utils import secure_filename
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # import from parent
from iterate_pages import generate_change_lst, squeeze

app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf',".PDF"]
app.config['UPLOAD_PATH'] = 'uploads'
txt = [['AIB blank', 19, (19, 19), '1']]

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400
        upload_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(upload_path)
        Process(target=preform_ocr, args=(upload_path,)).start()
        print('/status/'+filename)
    return jsonify({"filename":filename}), 200

def preform_ocr(upload_path):
    f = open(upload_path+".json", "w")
    f.write(json.dumps({"status":"processing","page":1, "pct":0}))
    f.close()
    data = squeeze(generate_change_lst(upload_path,logfile=upload_path+".json"))
    f = open(upload_path+".json", "w")
    f.write(json.dumps(data))
    f.close()
    #return jsonify(json.dumps(data)), 200


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/status/<filename>')
def status(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename+".json")

@app.route('/list')
def list_uploades():
    return jsonify(json.dumps(os.listdir("./uploads"))), 200

@app.route('/delete/<filename>')
def delete(filename):
    os.remove(os.path.join("./uploads",filename))
    return "deleted", 200