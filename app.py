import time
import uuid
import cv2
from flask import Flask, render_template, request, jsonify
import os
import hashlib

import numpy as np
from encode_faces import encode
from helper import resize_image
from recognize_faces_image import recognition, recognition_not_save_img
# import dlib
# dlib.DLIB_USE_CUDA
# print(dlib.cuda.get_num_devices())

app = Flask(__name__)

UPLOAD_PATH = ('static/img/upload/')
DATESET_PATH = ('dataset/')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        person_id = request.form['person_id']
        detect_face_method = request.form['detect_face_method']
        request_file = request.files['image_name']
        image = cv2.imdecode(np.fromstring(request_file.read(), np.uint8), cv2.IMREAD_COLOR)
        resized_image = resize_image(image, (300, 300))
        filename = person_id + os.path.splitext(request_file.filename)[1]
        path_save = os.path.join(UPLOAD_PATH, filename)
        cv2.imwrite(path_save, resized_image)
        start = time.time()
        isConfirmAttendance, person_id, percent_similarity = recognition(person_id, f'encodings/{detect_face_method}', path_save, detect_face_method)
        end = time.time()
        excution_time_str = f'{detect_face_method} - excution time: {end - start}'
        return render_template('index.html', upload=True, upload_image = filename, isConfirmAttendance = isConfirmAttendance, person_id = person_id, percent_similarity = percent_similarity, excution_time_str = excution_time_str)
    return render_template('index.html', upload=False)

@app.route('/check_attendance', methods=['POST'])
def check_attendance():
    if('person_id' not in request.form):
        return jsonify({'message': 'Person_id is empty.'})
    if('detect_face_method' not in request.form):
        return jsonify({'message': 'Detect_face_method is empty.'})
    if('person_image' not in request.files):
        return jsonify({'message': 'Person_image is empty.'})
    person_id = request.form['person_id']
    detect_face_method = request.form['detect_face_method']
    request_file = request.files['person_image']
    image = cv2.imdecode(np.fromstring(request_file.read(), np.uint8), cv2.IMREAD_COLOR)
    resized_image = resize_image(image, (300, 300))
    isConfirmAttendance, person_id, percent_similarity = recognition_not_save_img(person_id, f'encodings/{detect_face_method}', resized_image, detect_face_method)
    return jsonify({'message': 'Check attendance done.', 'isConfirmAttendance': isConfirmAttendance, 'person_id': person_id, 'percent_similarity': percent_similarity})

@app.route('/get_all_person_id', methods=['GET'])
def get_all_person_id():
    person_ids = os.listdir(DATESET_PATH)
    return jsonify({'person_ids': person_ids})

@app.route('/encode_faces', methods=['POST'])
def encode_faces():
    if('detect_face_method' not in request.form):
        return jsonify({'message': 'Detect_face_method is empty.'})
    detect_face_method = request.form['detect_face_method']
    encodings_folder = f'encodings/{detect_face_method}'
    dataset_folder = 'dataset'
    
    encodings_files = set(os.listdir(encodings_folder))
    encodings_files_name = set()
    for encodings_file in encodings_files:
        if encodings_file.endswith('.pickle'):
            encodings_files_name.add(encodings_file.split('.')[0])
    
    dataset_folders = set(os.listdir(dataset_folder))
    
    person_id_still_not_encode = dataset_folders - encodings_files_name
    encode(dataset_folder, encodings_folder, detect_face_method, person_id_still_not_encode)
    
    return jsonify({'message': 'Encode_faces done.'})

@app.route('/encode_face', methods=['POST'])
def encode_face():
    if('person_id' not in request.form):
        return jsonify({'message': 'Person_id is empty.'})
    if('detect_face_method' not in request.form):
        return jsonify({'message': 'Detect_face_method is empty.'})
    person_id = request.form['person_id']
    detect_face_method = request.form['detect_face_method']

    encodings_folder = f'encodings/{detect_face_method}'
    dataset_folder = 'dataset'

    encode(dataset_folder, encodings_folder, detect_face_method, [person_id])
    return jsonify({'message': 'Encode_face done.'})

@app.route('/upload_dataset', methods=['POST'])
def upload_dataset():
    if('person_id' not in request.form):
        return jsonify({'message': 'Person_id is empty.'})
    person_id = request.form['person_id']

    request_files = request.files.getlist('person_image')
    if not request_files:
        return jsonify({'message': 'Person_image is empty.'})
    
    for request_file in request_files:
        image = cv2.imdecode(np.fromstring(request_file.read(), np.uint8), cv2.IMREAD_COLOR)
        resized_image = resize_image(image, (300, 300))

        folder_path = os.path.join(DATESET_PATH, person_id)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        image_hash = hashlib.md5(resized_image.tobytes()).hexdigest()
        unique_filename = f"{image_hash}{os.path.splitext(request_file.filename)[1]}"
        path_save = os.path.join(folder_path, unique_filename)
        cv2.imwrite(path_save, resized_image)
        
    return jsonify({'message': 'Upload dataset done.'})

if __name__ == "__main__":
    app.run()
