import cv2
import os
import pickle
import json

def show(img, name):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyWindow(name)

def gray(img):
    if img is None:
        return img
    img = img.astype('uint8')
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def pickle_load(path):
    if not is_cached(path):
        print("""
        Invalid file path: %s
        """ % path)
        exit(0)

    with open(path, "rb") as f:
        return pickle.load(f)

def pickle_save(obj, path):
    with open(path, "wb") as f:
        return pickle.dump(obj,f)


def json_save(obj, path):
    with open(path, "w") as f:
        return json.dump(obj,f, indent=4)

def json_load(path):
    with open(path, "r") as f:
        return json.load(f)


def is_cached(path):
    if not os.path.isfile(path) or os.path.getsize(path) < 1:
        return False
    return True


def show_keypoint_img(path, num_of_keypoints=32):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    EXTRACTOR = cv2.xfeatures2d.SIFT_create()
    kps = EXTRACTOR.detect(gray)
    kps = sorted(kps, key=lambda x: -x.response)[:num_of_keypoints]
    img=cv2.drawKeypoints(gray,kps,None)
    cv2.imshow('keypoint.jpg', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()