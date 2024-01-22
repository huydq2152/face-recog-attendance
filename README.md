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

5. Cài đặt các thư viện cần thiết

```
pip install --upgrade -r requirements.txt
```

6. Run app

```
py .\app.py
```

7. Ảnh để test trong thư mục test_img

### Deploy qua IIS

1. https://mtuseeq.medium.com/how-to-deploy-flask-app-on-windows-server-using-fastcgi-and-iis-73d8139d5342 ( chú ý do dùng venv để run project nên cài đặt FastCGI cũng phải cài đặt trong venv)
2. Cần chuyển identity của application pool từ 'ApplicationPoolIdentity' thành 'LocalSystem'
3. Có thể phải sửa ở cả handlemapping trong IIS: https://www.youtube.com/watch?v=aJfHVXg-Tu8&ab_channel=TechieBlogging (7:20)
