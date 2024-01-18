### Tài liệu tham khảo

1. https://github.com/ageitgey/face_recognition/blob/master/face_recognition/api.py#L213
2. https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
3. https://github.com/huytranvan2010/Face-Recognition-with-OpenCV-Python-DL

### Cài đặt và chạy project

1. Cài visual c++ trong visual studio (chứa Window SDK, C++ complier, ... để có thể cài được thư viện dlib)
2. Cài môi trường ảo

```
python -m venv myenv
cd .\venv\Scripts\
.\Activate.ps1

```

3. Cài đặt dlib (không có GPU support)

```
git clone https://github.com/davisking/dlib.git
cd dlib
mkdir build
cd build
cmake .. -DUSE_AVX_INSTRUCTIONS=1
cmake --build .
cd ..
python setup.py install --yes USE_AVX_INSTRUCTIONS
```

4. Cài đặt các thư viện cần thiết

```
pip install dlib
pip install face_recognition
pip install opencv-python
pip install imutils
pip install setuptools (do import thủ công face_recognition_models)
```
