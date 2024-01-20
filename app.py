import uuid
import cv2
from flask import Flask, render_template, request, jsonify
import os

import numpy as np
from encode_faces import encode
from helper import resize_image
from recognize_faces_image import recognition

app = Flask(__name__)

UPLOAD_PATH = ('static/img/upload/')
DATESET_PATH = ('dataset/')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        person_id = request.form['person_id']
        request_file = request.files['image_name']
        image = cv2.imdecode(np.fromstring(request_file.read(), np.uint8), cv2.IMREAD_COLOR)
        resized_image = resize_image(image, (300, 300))
        filename = person_id + os.path.splitext(request_file.filename)[1]
        path_save = os.path.join(UPLOAD_PATH, filename)
        cv2.imwrite(path_save, resized_image)
        isConfirmAttendance, person_id, percent_similarity = recognition(person_id, 'encodings', path_save, 'hog')
        return render_template('index.html', upload=True, upload_image = filename, isConfirmAttendance = isConfirmAttendance, person_id = person_id, percent_similarity = percent_similarity)
    return render_template('index.html', upload=False)

@app.route('/check_attendance', methods=['POST'])
def check_attendance():
    if('person_id' not in request.form):
        return jsonify({'message': 'Person_id is empty.'})
    if('person_image' not in request.files):
        return jsonify({'message': 'Person_image is empty.'})
    person_id = request.form['person_id']
    request_file = request.files['image_name']
    image = cv2.imdecode(np.fromstring(request_file.read(), np.uint8), cv2.IMREAD_COLOR)
    resized_image = resize_image(image, (300, 300))
    filename = person_id + os.path.splitext(request_file.filename)[1]
    path_save = os.path.join(UPLOAD_PATH, filename)
    cv2.imwrite(path_save, resized_image)
    isConfirmAttendance, person_id, percent_similarity = recognition(person_id, 'encodings', path_save, 'hog')
    return jsonify({'message': 'Check attendance done.', 'isConfirmAttendance': isConfirmAttendance, 'person_id': person_id, 'percent_similarity': percent_similarity})

@app.route('/get_all_person_id', methods=['GET'])
def get_all_person_id():
    person_ids = os.listdir(DATESET_PATH)
    return jsonify({'person_ids': person_ids})

@app.route('/encode_faces', methods=['POST'])
def encode_faces():
    encodings_folder = 'encodings'
    dataset_folder = 'dataset'
    
    encodings_files = set(os.listdir(encodings_folder))
    encodings_files_name = set()
    for encodings_file in encodings_files:
        if encodings_file.endswith('.pickle'):
            encodings_files_name.add(encodings_file.split('.')[0])
    
    dataset_folders = set(os.listdir(dataset_folder))
    
    person_id_still_not_encode = dataset_folders - encodings_files_name
    encode(dataset_folder, encodings_folder, 'hog', person_id_still_not_encode)
    
    return jsonify({'message': 'Encode_faces done.'})

@app.route('/encode_face', methods=['POST'])
def encode_face():
    if('person_id' not in request.form):
        return jsonify({'message': 'Person_id is empty.'})
    person_id = request.form['person_id']
    encode('dataset', 'encodings', 'hog', [person_id])
    return jsonify({'message': 'Encode_face done.'})

@app.route('/upload_dataset', methods=['POST'])
def upload_dataset():
    if('person_id' not in request.form):
        return jsonify({'message': 'Person_id is empty.'})
    if('person_image' not in request.files):
        return jsonify({'message': 'Person_image is empty.'})
    person_id = request.form['person_id']
    request_file = request.files['person_image']
    image = cv2.imdecode(np.fromstring(request_file.read(), np.uint8), cv2.IMREAD_COLOR)
    resized_image = resize_image(image, (300, 300))

    folder_path = os.path.join(DATESET_PATH, person_id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    unique_filename = str(uuid.uuid4()) + os.path.splitext(request_file.filename)[1]
    path_save = os.path.join(folder_path, unique_filename)
    cv2.imwrite(path_save, resized_image)
    return jsonify({'message': 'Upload dataset done.'})

if __name__ == "__main__":
    app.run(debug=True)
