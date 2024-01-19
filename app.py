import uuid
from flask import Flask, render_template, request, jsonify
import os
from encode_faces import encode
from recognize_faces_image import recognition

app = Flask(__name__)

UPLOAD_PATH = ('static/upload/')
DATESET_PATH = ('dataset/')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        person_id = request.form['selected_id']
        upload_file = request.files['image_name']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(path_save)
        if recognition(person_id, 'encodings', path_save, 'hog') == True:
            isConfirmAttendance = 'Đúng'
        else:
            isConfirmAttendance = 'Sai'
        return render_template('index.html', upload=True, upload_image = filename, isConfirmAttendance = isConfirmAttendance)
    return render_template('index.html', upload=False)

@app.route('/encode_faces', methods=['POST'])
def encode_faces():
    encode('dataset', 'encodings', 'hog')
    return jsonify({'message': 'Encode_faces done.'})

@app.route('/upload_dataset', methods=['POST'])
def upload_dataset():
    person_id = request.form['person_id']
    upload_file = request.files['person_image']

    folder_path = os.path.join(DATESET_PATH, person_id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    unique_filename = str(uuid.uuid4()) + os.path.splitext(upload_file.filename)[1]
    path_save = os.path.join(folder_path, unique_filename)
    upload_file.save(path_save)
    return jsonify({'message': 'Upload dataset done.'})

if __name__ == "__main__":
    app.run(debug=True)
