from flask import Flask, render_template, request, jsonify
import os

# webserver gateway interface
app = Flask(__name__)

UPLOAD_PATH = ('static/upload/')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        upload_file = request.files['image_name']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(path_save)
        isConfirmAttendance = 'Đúng'

        return render_template('index.html', upload=True, upload_image=filename, isConfirmAttendance = isConfirmAttendance)

    return render_template('index.html', upload=False)

if __name__ == "__main__":
    app.run(debug=True)
