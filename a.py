import sklearn
from sklearn.cluster import KMeans
import cv2
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os
import pickle
import random 
import scipy

def show(img, name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 400, 400)
    cv2.imshow(name, img)

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
    descriptor_list = pickle.load(f)

descriptor_list = np.array(descriptor_list)  

with open("images.pickle", "rb") as f:
    images, images_names = pickle.load(f)

# for index, i in enumerate(images):
#     show(i, images_names[index])
#     cv2.waitKey(0)
#     cv2.destroyWindow(images_names[index])


def cos_cdist(dsc_list, input_dsc):
    dsc_list = [i[0].reshape(1, -1) for i in dsc_list]
    print(dsc_list[0].shape)
    v = input_dsc.reshape(1, -1)
    print(v.shape)
    return scipy.spatial.distance.cdist(dsc_list, v, 'cosine').reshape(-1)

kmeans = KMeans(n_clusters = 8)
n, x, y = descriptor_list.shape

descriptor_list = descriptor_list.reshape((n, x*y))
kmeans.fit(descriptor_list)

data = random.choice(images)

print('extracting input image')
data_dsc = extract_features(data)
print('searching ...')

# show(data, "input image")



rs = kmeans.predict(data_dsc)


print(rs)
labels = kmeans.labels_
print(labels)

good_images = []

for index, i in enumerate(labels):
    if i == rs[0]:
        good_images.append((descriptor_list[index] ,images[index], images_names[index]))
        
distances = cos_cdist(good_images, data_dsc)

print(distances)




