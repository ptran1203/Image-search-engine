import cv2
import numpy as np
from math import sqrt
from os import listdir
from json import dump, load

# Const
img1 = cv2.imread('images/108103_sm.jpg')
img2 = cv2.imread('images/118501_sm.jpg')
img3 = cv2.imread('images/107300_sm.jpg')


IMG_PATH = "images/copydays_original/"
H = np.zeros((300,256,3))
BINS = np.arange(256).reshape(256,1)
COLOR = [ (255,0,0),(0,255,0),(0,0,255) ]

def histogram(img):
   for ch, col in enumerate(COLOR):
    hist_item = cv2.calcHist([img],[ch],None,[256],[0,255])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist_item=np.int32(np.around(hist_item))

    # pts = np.column_stack((BINS,hist_item))
    # cv2.polylines(H,[pts],False,col) 
    # h=np.flipud(H)
    # cv2.imshow('colorhist',h)
    # if cv2.waitKey(0) == ord('q'):
    #     print ("quit")
    return hist_item.flatten().tolist()


def cosine_angle(a, b):
    return sum(
        [x*y for x, y in zip(a, b)]
        ) / (sqrt(
                sum([x**2 for x in a])
            ) * sqrt(
                sum([x**2 for x in b])))


def init():
    data = {}
    for file in listdir(IMG_PATH):
        path = IMG_PATH + file
        data[file.replace('.jpg', '')] = histogram(cv2.imread(path))
    
    # cache data
    with open('cache/img.json', 'w') as f:
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

    with open('cache/img.json', 'r') as f:
        return load(f)

    


def main():
    # init()
    data = get_data()
    query = histogram(cv2.imread(IMG_PATH + '204500.jpg'))
    print(search(query, data))


if __name__ == "__main__":
    main()

        
