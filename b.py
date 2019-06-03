import sklearn
from sklearn.cluster import KMeans
import cv2
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os
import pickle
import random 
import scipy
import sys

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

def gray(img):
    img = img.astype('uint8')
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def extract_features(image, vector_size=32):
    try:
        alg = cv2.xfeatures2d.SIFT_create()
        kps = alg.detect(image)
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        kps, dsc = alg.compute(image, kps)
        dsc = dsc.flatten()
        needed_size = (vector_size * 64 * 2)
        if dsc.size < needed_size:
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print(f'Error: {e}' )
        return None
    return dsc.reshape(1, -1)


with open("dsc_list.pickle", "rb") as f:
    print('loading dsc_list.pickle ...')
    descriptor_list = pickle.load(f)
    print('...')

descriptor_list = np.array(descriptor_list)  

with open("images.pickle", "rb") as f:
    print('loading images.pickle ...')
    images, images_names, _ = pickle.load(f)
    print('...')




def cos_cdist(images, input_dsc):
    dsc_list = np.array([image[2] for image in images])
    v = input_dsc.reshape(1, -1)
    dist = scipy.spatial.distance.cdist(dsc_list, v, 'cosine').reshape(-1)
    for idx, d in enumerate(dist):
        images[idx] = list(images[idx])
        images[idx][3] = d 
        images[idx] = tuple(images[idx])
    return images

n, x, y = descriptor_list.shape
descriptor_list = descriptor_list.reshape((n, x*y))

input_index = None

if (len(sys.argv) > 1):
    idx = int(sys.argv[1])
    data = images[idx]
else:
    data = random.choice(images)


with open("kmeans.pickle", "rb") as f:
    print('loading kmeans.pickle')
    kmeans = pickle.load(f)
    print('done')

print('extracting input image')
data_dsc = extract_features(data)
print('searching ...')

show(data, "input image", True)

rs = kmeans.predict(data_dsc)[0]

labels = kmeans.labels_

good_dict_images = []
for i, label in enumerate(labels):
    if label == rs:
        img = images[i]
        img_name = images_names[i]
        # show_wait(img, img_name)
        img_dsc = descriptor_list[i]
        dist = 0.0
        good_dict_images.append((img, img_name, img_dsc, dist))
print(rs)
print(len(good_dict_images))
dict_images = []


images_dist = cos_cdist(good_dict_images, data_dsc)

images_dist = sorted(images_dist, key=lambda x: x[3])


print('search result: ')
for img in images_dist[:10]:
    show_wait(img[0], f'{img[1]} - {img[3]}')



