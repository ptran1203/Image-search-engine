import cv2
import pickle

def show(img, name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 400, 400)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyWindow(name)

def gray(img):
    img = img.astype('uint8')
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def load(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def save(obj, path):
    with open(path, "wb") as f:
        return pickle.dump(obj,f)

