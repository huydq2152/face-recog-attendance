import os
import face_recognition
import pickle
import cv2

def recognition(person_id, encodings_folder_name, image_path, detection_method):
    # load encodings đã lưu từ file
    print("[INFO] loading encodings...")
    id = person_id
    pickle_file_path = os.path.join(encodings_folder_name, f"{id}.pickle")
    data = pickle.loads(open(pickle_file_path, "rb").read())     

    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    print("[INFO] recognizing faces...")
    boxes = face_recognition.face_locations(rgb, model=detection_method)
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []
    res = False
    for encoding in encodings:
        match = any(face_recognition.compare_faces(data["encodings"], encoding, 0.3))      
        name = "Unknown"    
        if match:
            name = data["names"][0]
            res = True
        names.append(name)
        break

    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15

        cv2.putText(image, f"person_id = {name}", (left, y), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)

    filename = os.path.basename(image_path)
    cv2.imwrite(os.path.join('static/img/face-detect-and-recognition/predict/{}').format(filename), image)

    return res




