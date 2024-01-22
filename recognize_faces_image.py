import os
import face_recognition
import pickle
import cv2

def recognition(person_id, encodings_folder_name, image_path, detection_method):
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
    isConfirmAttendance = False
    percent_similarity = 0
    for encoding in encodings:
        match = any(face_recognition.compare_faces(data["encodings"], encoding, 0.5))      
        name = "Unknown"    
        if match:
            percent_similarity = calculate_similarity_percent(encoding, data["encodings"])
            name = data["names"][0]
            isConfirmAttendance = True
        names.append(name)
        break

    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

    filename = os.path.basename(image_path)
    cv2.imwrite(os.path.join('static/img/face-detect-and-recognition/predict/{}').format(filename), image)

    return isConfirmAttendance, name, percent_similarity

def recognition_not_save_img(person_id, encodings_folder_name, image, detection_method):
    id = person_id
    pickle_file_path = os.path.join(encodings_folder_name, f"{id}.pickle")
    data = pickle.loads(open(pickle_file_path, "rb").read())     

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb, model=detection_method)
    encodings = face_recognition.face_encodings(rgb, boxes)

    isConfirmAttendance = False
    percent_similarity = 0
    for encoding in encodings:
        match = any(face_recognition.compare_faces(data["encodings"], encoding, 0.5))      
        name = "Unknown"    
        if match:
            percent_similarity = calculate_similarity_percent(encoding, data["encodings"])
            name = data["names"][0]
            isConfirmAttendance = True
        break

    return isConfirmAttendance, name, percent_similarity

def calculate_similarity_percent(encodings, face_to_check):
    distances = face_recognition.face_distance(encodings, face_to_check)
    similarities = [(1 - distance) for distance in distances]  
    max_similarity = max(similarities)
    return max_similarity * 100  
    





