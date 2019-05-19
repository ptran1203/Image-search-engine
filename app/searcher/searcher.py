import cv2
import numpy as np
import os
from urllib.request import Request, urlopen
from math import sqrt
from json import dump, load


# Const
BASE_DIR = os.getcwd()
IMG_PATH = BASE_DIR + "/static/images/copydays_original/"
H = np.zeros((300,256,3))
BINS = np.arange(256).reshape(256,1)
COLOR = [ (255,0,0),(0,255,0),(0,0,255) ]

def histogram(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = img.mean(axis=2).flatten()
    hist = np.histogram(img, range(257))
    vector = []
    for h in hist:
        # convert numpy.int64 to int
        h = [int(x) for x in h]
        vector.extend(h)

    return vector


def cosine_angle(a, b):
    if sum(a) == 0:
        return 0
    return sum(
        [x*y for x, y in zip(a, b)]
        ) / (sqrt(
                sum([x**2 for x in a])
            ) * sqrt(
                sum([x**2 for x in b])))


def init():
    data = {}
    for file in os.listdir(IMG_PATH):
        path = IMG_PATH + file
        data[file] = histogram(cv2.imread(path))
    
    print(data['200100.jpg'])
    with open(BASE_DIR + '/cache/img.json', 'w') as f:
        dump(data, f, indent=4)

def search(query, data):
    data_tmp = {}
    for k, v in data.items():
        # print(k, v)
        # return 1
        data_tmp[k] = cosine_angle(query, v)

    return [x for x in sorted(data_tmp.items(), key=lambda kv: -kv[1])][:10]


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
    init()
    # data = get_data()
    # print(IMG_PATH)
    query = histogram(cv2.imread(IMG_PATH + '204500.jpg'))
    print(query)
    # print(search(query, data))


if __name__ == "__main__":
    main()

        
