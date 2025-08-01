import os
import shutil
import schedule
import time
from threading import Thread
from flask import Flask, render_template, redirect, flash, url_for, request, abort, after_this_request, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import safe_join
import tensorflow as tf
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from keras.preprocessing.image import load_img
from keras.applications import ResNet50V2
from keras.applications.resnet50 import preprocess_input

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = ['.png', '.jpeg', '.jpg', '.JPEG', '.JPG', '.gif']
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['TEMP_FOLDER'] = 'static/temp/'
app.config['MAX_CONTENT_LENGTH'] = 12 * 1024 * 1024
app.config['SECRET_KEY']= 'd0e868c63d531755d47bc2c66ac4647087a63ecdc330bde71c17adb7aef2cc1b'

base_model = ResNet50V2(weights='imagenet', include_top=False)
model = load_model('pigeons_cnn.keras')

def clear_uploads():
    file_names = os.listdir(app.config['UPLOAD_FOLDER'])
    for file_name in file_names:
        shutil.move(os.path.join(app.config['UPLOAD_FOLDER'], file_name), app.config['TEMP_FOLDER'])
        os.remove(os.path.join(app.config['TEMP_FOLDER'], file_name))

def read_image(filename):
    img = load_img(filename, target_size=(224,224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis = 0)
    x = preprocess_input(x) / 255
    return x

@app.route('/', methods=['GET'])
def index():
    thread = Thread(target=clear_uploads)
    thread.start()
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['ALLOWED_EXTENSIONS']:
                flash('Images must be in jpeg, png, or gif format')
                return redirect('/')
            
            file_path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(file_path)
            img = read_image(file_path)
            y = base_model.predict(img)
            prediction = model.predict(y)
            if prediction[0][0] == 0:
                pred_class = 'A Pigeon'
            else :
                pred_class = 'Not A Pigeon'
        else:
            flash('No file selected')
            return redirect('/')
    
    return render_template('predict.html', pred_class=pred_class, filename=filename)

@app.route('/predict/<filename>', methods=['GET'])
def serve_file(filename):

        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



