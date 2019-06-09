import cv2
import os
import pickle
import json

def show(img, name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 400, 400)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyWindow(name)

def gray(img):
    if img is None:
        return img
    img = img.astype('uint8')
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def load(path):
    if not os.path.isfile(path) or os.path.getsize(path) < 1:
        print("""
        Invalid file path: %s
        if you does not build data yet, run:
        python ./app/source/feature.py
        """ % path)

        exit(0)
    with open(path, "rb") as f:
        return pickle.load(f)

def save(obj, path):
    with open(path, "wb") as f:
        return pickle.dump(obj,f)


def json_save(obj, path):
    with open(path, "w") as f:
        return json.dump(obj,f, indent=4)

def json_load(path):
    with open(path, "r") as f:
        return json.load(f)