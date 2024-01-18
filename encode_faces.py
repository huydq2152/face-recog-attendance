from imutils import paths
import pickle
import cv2
import os
import face_recognition

def encode(datasets_folder_name, encodings_folder_name, detection_method):
    folders = os.listdir(datasets_folder_name)
    for folder in folders:
        folder_path = os.path.join(datasets_folder_name, folder)

        if os.path.isdir(folder_path):
            imagePaths = list(paths.list_images(folder_path))

            folder_name = os.path.basename(folder_path)
            knownEncodings = []
            knownNames = []

            print(f"[INFO] quantifying faces of person_id = {folder_name} ...")
            for (i, imagePath) in enumerate(imagePaths):
                print("[INFO] processing image {}/{}".format(i+1, len(imagePaths)))
                name = imagePath.split(os.path.sep)[-2]
                image = cv2.imread(imagePath)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                boxes = face_recognition.face_locations(rgb, model=detection_method)    
                encodings = face_recognition.face_encodings(rgb, boxes)  

                for encoding in encodings:
                    knownEncodings.append(encoding)
                    knownNames.append(name)

            print(f"[INFO] serializing encodings of person_id = {folder_name} ...")
            data = {"encodings": knownEncodings, "names": knownNames}

            pickle_file_path = os.path.join(encodings_folder_name, f"{folder_name}.pickle")
            with open(pickle_file_path, "wb") as f:
                f.write(pickle.dumps(data))


    







