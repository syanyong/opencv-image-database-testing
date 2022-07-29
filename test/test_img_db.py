import cv2
import struct
import redis
import numpy as np
import base64
import time
import io
from PIL import Image, ImageDraw

# MONGODB
from pymongo import MongoClient
import gridfs


def writeImgRedis1(r, key, img):
    h, w = img.shape[:2]
    shape = struct.pack('>II',h,w)
    encoded = shape + img.tobytes()
    r.set(key, encoded)

def readImgRedis1(r, key):
   encoded = r.get(key)
   h, w = struct.unpack('>II',encoded[:8])
   img = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
   return img

def writeImgRedis2(r, key, img):
    _, data = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(data)
    r.set(key, jpg_as_text)

def readImgRedis2(r, key):
    encoded = r.get(key)
    jpg_original = base64.b64decode(encoded)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img

def writeImgMongo1(fs, img):
    _, data = cv2.imencode('.jpg', img)
    file_id = fs.put(data.tobytes())
    return file_id

def readImgMongo1(fs, file_id):
    encoded = fs.get(file_id).read()
    data = io.BytesIO(encoded)
    img = Image.open(data)
    jpg_as_np = np.array(img)
    jpg_as_np = cv2.cvtColor(jpg_as_np, cv2.COLOR_BGR2RGB)
    return jpg_as_np

def writeImgMongo2(fs, img):
    _, data = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(data)
    file_id = fs.put(jpg_as_text)
    return file_id

def readImgMongo2(fs, file_id):
    encoded = fs.get(file_id).read()
    jpg_original = base64.b64decode(encoded)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img

def writeImgMongo3(db, img):
    _, data = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(data)
    mycol = db["img"]
    mycol.insert_one({"img": jpg_as_text})

def readImgMongo3(db):
    mycol = db["img"]
    bs = mycol.find_one({})
    jpg_original = base64.b64decode(bs["img"])
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img

def writeImgMongo4(db, img):
    h, w = img.shape[:2]
    shape = struct.pack('>II',h,w)
    encoded = shape + img.tobytes()
    mycol = db["img"]
    mycol.insert_one({"img": encoded})

def readImgMongo4(db):
    mycol = db["img"]
    bs = mycol.find_one({})
    encoded = bs["img"]
    h, w = struct.unpack('>II',encoded[:8])
    img = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
    return img

if __name__ == '__main__':
    # Redis connection
    r = redis.Redis(host='redis', port=6379, db=0)

    # Mongodb connection
    connection = MongoClient("mongodb://james:1234@mongo:27017")
    db = connection['ml']

    # Initial GridFS
    fs = gridfs.GridFS(db)

    # Read test image
    img_out1 = cv2.imread("test.jpg")

    print("type", type(img_out1))

    # Test case 1
    t = time.time()
    writeImgRedis1(r, "img1", img_out1)
    print("T1_WRITE", time.time() - t, "Redis bytes")

    t = time.time()
    img = readImgRedis1(r, "img1")
    print("T1_READ ", time.time() - t)
    cv2.imwrite("T1.jpg", img)

    # Test case 2
    t = time.time()
    writeImgRedis2(r, "img2", img_out1)
    print("T2_WRITE", time.time() - t, "Redis base64")

    t = time.time()
    img = readImgRedis2(r, "img2")
    print("T2_READ ", time.time() - t)
    cv2.imwrite("T2.jpg", img)

    # Test case 3
    t = time.time()
    file_id = writeImgMongo1(fs, img_out1)
    print("T3_WRITE", time.time() - t, "Mongodb GridFS BytesIO")

    t = time.time()
    img = readImgMongo1(fs, file_id)
    print("T3_READ ", time.time() - t)
    cv2.imwrite("T3.jpg", img)

    # Test case 4
    t = time.time()
    file_id = writeImgMongo2(fs, img_out1)
    print("T4_WRITE", time.time() - t, "Mongodb GridFS base64")

    t = time.time()
    img = readImgMongo2(fs, file_id)
    print("T4_READ ", time.time() - t)
    cv2.imwrite("T4.jpg", img)

    # Test case 5
    t = time.time()
    file_id = writeImgMongo3(db, img)
    print("T5_WRITE", time.time() - t, "Mongodb base64")

    t = time.time()
    img = readImgMongo3(db)
    print("T5_READ ", time.time() - t)
    cv2.imwrite("T5.jpg", img)

    # Test case 6
    t = time.time()
    file_id = writeImgMongo3(db, img)
    print("T6_WRITE", time.time() - t, "Mongodb bytes")

    t = time.time()
    img = readImgMongo3(db)
    print("T6_READ ", time.time() - t)
    cv2.imwrite("T6.jpg", img)

