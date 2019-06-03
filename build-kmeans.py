import sklearn
from sklearn.cluster import KMeans
import cv2
import numpy as np
import os
import pickle
import random 
import scipy

with open("dsc_list.pickle", "rb") as f:
    print('loading dsc_list.pickle ...')
    descriptor_list = pickle.load(f)
    print('done')
f.close()
descriptor_list = np.array(descriptor_list)  

with open("images.pickle", "rb") as f:
    print('loading images.pickle ...')
    images, images_names, init = pickle.load(f)
    print('done')
f.close()

def show(img, name, for_input=False):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 400, 400)
    if for_input:
        cv2.moveWindow(name, 20,50)
    cv2.imshow(name, img)

def show_wait(img, name):
    show(img, name)
    cv2.waitKey(0)
    cv2.destroyWindow(name)

n, x, y = descriptor_list.shape
descriptor_list = descriptor_list.reshape((n, x*y))

centers = []

for i in init:
    show_wait(images[i], images_names[i])
    centers.append(descriptor_list[i])

centers = np.array(centers)

kmeans = KMeans(n_clusters=8, n_init=1, init=centers)

print('start training ...')
kmeans.fit(descriptor_list)
print('finished training.')

with open("kmeans.pickle", "wb") as f:
    print('dumping kmeans.pickle ....')
    pickle.dump(kmeans, f)
    print('done')