import cv2
import numpy as np
import os
from urllib.request import Request, urlopen
from math import sqrt
from json import dump, load


# Const
BASE_DIR = os.getcwd()
IMG_PATH = BASE_DIR + "/static/images/copydays_original/"
BINS = (12, 8, 3)

def histogram(img, mask):
    hist = cv2.calcHist(
        [img], [0, 1, 2], mask, BINS, [0,256,0,256,0,256]
    )
    hist = cv2.normalize(hist, hist).flatten()
    return [float(x) for x in hist.tolist()]


def fvector(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, w = img.shape[:2]
    topmask = np.zeros((h, w),np.uint8)
    botmask = np.zeros((h, w),np.uint8)
    cv2.rectangle(topmask, (0, 0), (h//2, w), 255, -1)
    cv2.rectangle(botmask, (h//2, 0), (h, w), 255, -1)
    fvector = histogram(img, topmask)
    print(len(fvector))
    fvector.extend(histogram(img, botmask))
    print(len(fvector))
    return fvector


def cosine_angle(a, b):
    dividend = (sqrt(
                sum([x**2 for x in a])
            ) * sqrt(
                sum([x**2 for x in b])
            ))

    if sum(a) == 0 or dividend == 0:
        return 0

    return sum(
        [x*y for x, y in zip(a, b)]
        ) / dividend


def init():
    data = {}
    for file in os.listdir(IMG_PATH):
        path = IMG_PATH + file
        data[file] = fvector(cv2.imread(path))
    
    with open(BASE_DIR + '/cache/img.json', 'w') as f:
        dump(data, f, indent=4)

def search(query, data, limit=10):
    data_tmp = {}
    for k, v in data.items():
        data_tmp[k] = cosine_angle(query, v)

    return [x for x in sorted(data_tmp.items(),key=lambda kv: -kv[1])][:limit]


def get_data(isCached=True):
    if not isCached:
        init()

    with open(BASE_DIR + '/cache/img.json', 'r') as f:
        return load(f)

def get_img_from_url(url):
    res = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
    array = np.asarray(bytearray(res.read()), dtype=np.uint8)
    img = cv2.imdecode(array, -1)
    return img

def get_img(name):
    return cv2.imread(IMG_PATH + name)

def main():
    # init()
    # trial
    data = get_data()
    query = fvector(cv2.imread(IMG_PATH + '204500.jpg'))
    print(search(query, data))


if __name__ == "__main__":
    main()

        
