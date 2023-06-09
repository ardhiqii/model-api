from flask import Flask, request,jsonify,make_response
from datetime import datetime, timedelta
from prediction import model_predict
from functools import wraps
import os
import jwt
from werkzeug.utils import secure_filename
import time
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'storageBucket': 'fresh-detection.appspot.com'
})

app = Flask(__name__)


def token_required(func):
    """ 
    decorator factory which invoks update_wrapper() method and passes decorated function as an argument

    1. asshfiawfa
    2. dfawf    
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:

            data = jwt.decode(token, app.config['SECRET_KEY'])
        # You can use the JWT errors in exception
        # except jwt.InvalidTokenError:
        #     return 'Invalid token. Please log in again.'
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})
        try:
            content_type = file.mimetype
            bucket = storage.bucket()
            blob = bucket.blob(("uploads/"+file.filename))
            blob.content_type = content_type
            blob.upload_from_file(file)
            blob.make_public()
            return jsonify({'image_url':blob.public_url})
        except Exception as e:
            return jsonify({"error": str(e)})
    return "OK"

@app.route('/upload',methods=['POST'])
def upload():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})
        try:
            content_type = file.mimetype
            bucket = storage.bucket()
            blob = bucket.blob(("uploads/"+file.filename))
            blob.content_type = content_type
            blob.upload_from_file(file)
            blob.make_public()
            return jsonify({'image_url':blob.public_url})
        except Exception as e:
            return jsonify({"error": str(e)})
    return "OK"

@app.route('/predict',methods=['POST'])
def predict():
    url = request.get_json()['url']
    if url is None or url == "":
        return jsonify({"error":"no url"})
    try:
        result = model_predict(url)
        return jsonify({'result':result})
    except Exception as e:
            return jsonify({"error": str(e)})

@app.route('/upload-predict',methods=['POST'])
def uploadThenPredict():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})
        try:
            content_type = file.mimetype
            bucket = storage.bucket()
            blob = bucket.blob(("uploads/"+file.filename))
            blob.content_type = content_type
            blob.upload_from_file(file)
            blob.make_public()
            url = blob.public_url
            result = model_predict(url)
            return jsonify({'result':result,"imageUrl":url})
        except Exception as e:
            return jsonify({"error": str(e)})
    return "OK"
if __name__ == '__main__':
	app.run(host="127.0.0.1",port=8080,debug=True)

