# The comparison of storing images from OpenCV and PyTorch to Database
In the practical way of ML, the original and processed image need to store in a database. Whether it is temporary or persistent. The testing is separated into the in-memory database (Redis) and the NoSQL database (MongoDB), which support the binary data. The Redis can be used to store the temporary image or transfer between processes. Let's see the testing results.

## Results
```
(venv) root@384133966dff:/app# python test_img_db.py 
type <class 'numpy.ndarray'>
T1_WRITE 0.0017538070678710938 Redis bytes
T1_READ  0.0024712085723876953
T2_WRITE 0.0070111751556396484 Redis base64
T2_READ  0.005830287933349609
T3_WRITE 0.017976045608520508 Mongodb GridFS BytesIO
T3_READ  0.014397144317626953
T4_WRITE 0.008107900619506836 Mongodb GridFS base64
T4_READ  0.0066640377044677734
T5_WRITE 0.006702423095703125 Mongodb base64
T5_READ  0.006209611892700195
T6_WRITE 0.006687164306640625 Mongodb bytes
T6_READ  0.005991220474243164
```

## Known issue
`ImportError: libGL.so.1: cannot open shared object file: No such file or directory`

This problem can be solved by install the package below.
```
apt-get update
apt-get install ffmpeg libsm6 libxext6  -y
```

## Reference
https://stackoverflow.com/questions/40928205/python-opencv-image-to-byte-string-for-json-transfer
https://stackoverflow.com/questions/56944497/how-to-share-opencv-images-in-two-python-programs


