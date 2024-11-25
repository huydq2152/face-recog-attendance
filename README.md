### Reference

1. https://github.com/ageitgey/face_recognition/blob/master/face_recognition/api.py#L213
2. https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
3. https://github.com/huytranvan2010/Face-Recognition-with-OpenCV-Python-DL

### Setting and run project

1. Setting python in your computer https://www.python.org/downloads/
2. Setting visual c++ (can use visual studio) (contain Window SDK, C++ complier, ... all necessary portion for setup dlib)
3. Open project and cd to the root folder
4. Setting virtual environment

```
python -m venv venv
cd .\venv\Scripts\
.\Activate.ps1
```

5. Setting necessary lib (if run in machine that has GPU, can remove dlib and face_recognition in requirements.txt file)

```
pip install -r requirements.txt
```

6. Run app

```
py .\app.py
```

# Setting for running on GPU

1. Setup cuda toolkit và cuDNN : https://www.youtube.com/watch?v=lw5dpTl0yZE
2. cd to venv/Lib folder
3. Setting dlib with GPU

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

4. Setup face_recognition

```
pip install face_recognition
```

5. After setup, if have error when run app, go to file **init**.py of dlib folder just install and edit the code that add GPU

```
if 'ON' == 'ON':
```

### Deploy via IIS

1. https://mtuseeq.medium.com/how-to-deploy-flask-app-on-windows-server-using-fastcgi-and-iis-73d8139d5342 ( note: because use venv to run project so FastCGI also need to install in venv)
2. Need change identity of application pool from 'ApplicationPoolIdentity' to 'LocalSystem'
3. Maybe need to change handlemapping in IIS: https://www.youtube.com/watch?v=aJfHVXg-Tu8&ab_channel=TechieBlogging (7:20)
