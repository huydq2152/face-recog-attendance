# USAGE
# python recognize_faces_image.py --personId 1 --encodings encodings --image .\test_images\toi.png 
import os
import face_recognition
import argparse
import pickle
import cv2

ap = argparse.ArgumentParser()
# đường dẫn đến folder encodings chứa file pickle đã lưu
ap.add_argument("-pId", "--personId", required=True, help="person id for recognition")
ap.add_argument("-e", "--encodings", required=True, help="path to the serialized db of facial encodings")
ap.add_argument("-i", "--image", required=True, help="path to the test image")
# nếu chạy trên CPU hay embedding devices thì để hog, còn khi tạo encoding vẫn dùng cnn cho chính xác
ap.add_argument("-d", "--detection_method", type=str, default="hog", help="face dettection model to use: cnn or hog")
args = vars(ap.parse_args())

# load encodings đã lưu từ file
print("[INFO] loading encodings...")
id = args["personId"];
pickle_file_path = os.path.join(args["encodings"], f"{id}.pickle")
data = pickle.loads(open(pickle_file_path, "rb").read())     

# load image và chuyển từ BGR to RGB (dlib cần để chuyển về encoding)
image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# detect faces trong ảnh và trích xuất các encodings
print("[INFO] recognizing faces...")
boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
encodings = face_recognition.face_encodings(rgb, boxes)

# khởi tạo list chứa tên các khuôn mặt phát hiện được
# nên nhớ trong 1 ảnh có thể phát hiện được nhiều khuôn mặt nhé
names = []

# duyệt qua các encodings của faces phát hiện được trong ảnh
for encoding in encodings:
    # khớp encoding của từng face phát hiện được với known encodings (từ datatset)
    # so sánh list of known encodings và encoding cần check, sẽ trả về list of True/False xem từng known encoding có khớp với encoding check không
    # có bao nhiêu known encodings thì trả về list có bấy nhiêu phần tử
    # trong hàm compare_faces sẽ tính Euclidean distance và so sánh với tolerance=0.6 (mặc định), nhó hơn thì khớp, ngược lại thì ko khớp (khác người), tham số cuối càng nhỏ càng strict
    match = any(face_recognition.compare_faces(data["encodings"], encoding, 0.3))      
    name = "Unknown"    

    # Kiểm tra xem từng encoding có khớp với known encodings nào không,
    if match:
        # Nếu có khớp, thì đặt tên là tên trong dataset
        name = data["names"][0]  # Lấy tên từ dataset (giả sử chỉ có một tên trong dataset)

    names.append(name)

# Duyệt qua các bounding boxes và vẽ nó trên ảnh kèm thông tin
# Nên nhớ recognition_face trả bounding boxes ở dạng (top, rights, bottom, left)
for ((top, right, bottom, left), name) in zip(boxes, names):
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    y = top - 15 if top - 15 > 15 else top + 15

    cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1)

cv2.imshow("Image", image)
cv2.waitKey(0)




