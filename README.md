### Tài liệu tham khảo

1. https://github.com/ageitgey/face_recognition/blob/master/face_recognition/api.py#L213
2. https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
3. https://github.com/huytranvan2010/Face-Recognition-with-OpenCV-Python-DL

### Cài đặt và chạy project

1. Cài đặt python https://www.python.org/downloads/
2. Cài visual c++ trong visual studio (chứa Window SDK, C++ complier, ... để có thể cài được thư viện dlib)
3. Mở project và cd vào thư mục gốc
4. Cài môi trường ảo

```
python -m venv venv
cd .\venv\Scripts\
.\Activate.ps1
```

5. Cài đặt các thư viện cần thiết (nếu chạy trên máy có GPU thì bỏ dlib và face_recognition trong file requirements.txt)

```
pip install --upgrade -r requirements.txt
```

6. Run app

```
py .\app.py
```

7. Ảnh để test trong thư mục test_img

# Cài đặt để chạy trên gpu

1. Cài cuda toolkit và cuDNN : https://www.youtube.com/watch?v=lw5dpTl0yZE
2. cd vào thư mục venv/Lib
3. Cài đặt dlib với GPU

```
git clone https://github.com/davisking/dlib.git
cd dlib
mkdir build
cd build
cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1
cmake --build .
cd ..
python setup.py install --set USE_AVX_INSTRUCTIONS=1 --set DLIB_USE_CUDA=1
```

4. Cài face_recognition

```
pip install face_recognition
```

5. Nếu sau khi cài, run app lỗi thì vào file **init**.py của thư mục dlib vừa cài đặt và sửa đoạn code thêm GPU

```
if 'ON' == 'ON':
```

### Deploy qua IIS

1. https://mtuseeq.medium.com/how-to-deploy-flask-app-on-windows-server-using-fastcgi-and-iis-73d8139d5342 ( chú ý do dùng venv để run project nên cài đặt FastCGI cũng phải cài đặt trong venv)
2. Cần chuyển identity của application pool từ 'ApplicationPoolIdentity' thành 'LocalSystem'
3. Có thể phải sửa ở cả handlemapping trong IIS: https://www.youtube.com/watch?v=aJfHVXg-Tu8&ab_channel=TechieBlogging (7:20)
