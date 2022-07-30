import redis
import time
import base64
import numpy as np
import cv2
import struct

def readImgRedis1(r, key):
   encoded = r.get(key)
   h, w = struct.unpack('>II',encoded[:8])
   img = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
   return img

if __name__ == '__main__':
    # Redis connection
    r = redis.Redis(host='redis', port=6379, db=0)

    pubsub = r.pubsub()
    pubsub.subscribe('img_proc')
    count = 0
    for item in pubsub.listen():
        t = time.time()
        # print (item)
        if (item["type"] == "message"):
            # encoded = r.get("img")
            # jpg_original = base64.b64decode(encoded)
            # jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            # img = cv2.imdecode(jpg_as_np, flags=1)
            img = readImgRedis1(r, "img")
            print("T7_SUB ", time.time() - t)
            cv2.imwrite("T7_SUB.jpg", img)
        else:
            print(item)
        count += 1
