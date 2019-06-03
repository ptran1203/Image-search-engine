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
    print('loading dsc_list.pickle ...')
    descriptor_list = pickle.load(f)
    print('...')

descriptor_list = np.array(descriptor_list)  

with open("images.pickle", "rb") as f:
    print('loading images.pickle ...')
    images, images_names = pickle.load(f)
    print('...')




def cos_cdist(images, input_dsc):
    dsc_list = [i[0] for i in images]
    v = input_dsc.reshape(1, -1)
    dist = scipy.spatial.distance.cdist(dsc_list, v, 'cosine').reshape(-1)
    for idx, i in enumerate(dist):
        images[idx] = list(images[idx])
        images[idx][3] = i
        images[idx] = tuple(images[idx])
    return images

n, x, y = descriptor_list.shape
descriptor_list = descriptor_list.reshape((n, x*y))

n = len(images)
centers = []

for i in range(0, n, int(n/8)):
    print(images_names[i])
    centers.append(descriptor_list[i])
centers = np.array(centers)

kmeans = KMeans(n_clusters = 8, init=centers, n_init=1)

kmeans.fit(descriptor_list)

data = random.choice(images)

print('extracting input image')
data_dsc = extract_features(data)
print('searching ...')

show(data, "input image")



rs = kmeans.predict(data_dsc)


print(rs)
labels = kmeans.labels_
print(labels)

good_images = []

for index, i in enumerate(labels):
    if i == rs[0]:
        # show(images[index], images_names[index])
        # cv2.waitKey(0)
        # cv2.destroyWindow(images_names[index])
        good_images.append((descriptor_list[index] ,images[index], images_names[index], -1))

print(len(good_images))      
images_dist = cos_cdist(good_images, data_dsc)
images_dist = sorted(images_dist, key=lambda x: x[3])
# for index, i in enumerate(images):
#     show(i, images_names[index])
#     cv2.waitKey(0)
#     cv2.destroyWindow(images_names[index])
for img in images_dist[:5]:
    show(img[1], f'{img[2]} - {img[3]}')
    cv2.waitKey(0)
    cv2.destroyWindow(f'{img[2]} - {img[3]}')



