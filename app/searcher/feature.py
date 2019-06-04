import cv2
import os
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pickle as pickle
import json
BASE_DIR = os.path.dirname(os.getcwd())
EXTRACTOR = cv2.xfeatures2d.SURF_create()
IMG_DIR = os.path.join(BASE_DIR, "static/images")

def load(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def save(obj, path):
    with open(path, "wb") as f:
        return pickle.dump(obj,f)

class ImageDescriptor:
    def __init__(self, path):
        self.image = cv2.imread(path)
        # self.path = path
        self.keypoint, self.descriptor = self._features(EXTRACTOR)


    def _features(self, extractor):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        kps = extractor.detect(image)
        kps = sorted(kps, key=lambda x: -x.response)[:32]
        keypoints, descriptor = extractor.compute(image, kps)
        descriptor = descriptor.flatten()
        size = 32 * 64
        if descriptor.size < size:
            descriptor = np.concatenate([descriptor, np.zeros(size - descriptor.size)])
        return keypoints, descriptor


class ImageCluster:
    def __init__(self, images, n=8):
        self.images = images
        self.kmeans = KMeans(n_clusters=n)
        self.kmeans.fit(np.array(self._descriptor_list()))

    def _descriptor_list(self):
        return [descriptor for descriptor in self.images.values()]

    def predict(self, img_dsc):
        return self.kmeans.predict(
            img_dsc.reshape(1 , -1)
        )

    def clustered_images(self):
        res = {}
        for name, descriptor in self.images.items():
            if descriptor is not None:
                res[name] = self.predict(descriptor)
        return res

class Searcher:
    def __init__(self, query_v, data):
        self.query_vector = query_v
        self.data = data


    def _cosine(self, vectorb):
        vectora = self.query_vector
        dividend = sqrt(
                sum([x**2 for x in vectora])
            ) * sqrt(
                sum([x**2 for x in vectorb])
            )

        if sum(vectora) == 0 or dividend == 0:
            return 0

        return sum(
            [x*y for x, y in zip(vectora, vectorb)]
            ) / dividend

    def search(self, limit=10):
        data_tmp = {}
        print(len(self.data))
        for k, v in self.data.items():
            data_tmp[k] = self._cosine(v)
        
        return [x for x in sorted(data_tmp.items(),key=lambda kv: -kv[1]) if 0.6 < x[1]][:limit]

        # not in use
        sorted_by_fcolor = [x for x in sorted(
            data_tmp.items(),
            key=lambda kv: -kv[1]
            )][:10]

        data_ftexture = {key[0]: self.data[key[0]]['ftexture'] for key in sorted_by_fcolor}

        data_tmp = {}
        for k, v in data_ftexture.items():
            data_tmp[k] = self._cosine(v)
        
        return [x for x in sorted(data_tmp.items(),key=lambda kv: kv[1])][:limit]


class Database:
    def __init__(self, number_of_images=0,isCached=True):
        if not isCached:
            self.build(number_of_images)

        self.images = load(os.path.join(BASE_DIR, "cache/images.pkl"))

    @staticmethod
    def build(num=0):
        print("START building...")
        data = {}
        files = os.listdir(IMG_DIR)
        if num > 0:
            files = files[:num]
        length = len(files)
        for i, file in enumerate(files):
            path = os.path.join(IMG_DIR, file)
            data[file] = ImageDescriptor(path).descriptor
            # print("progress: %s/ %s" %(i + 1, len(files)))

        print("DONE!!")
        save(data, os.path.join(BASE_DIR, "cache/images.pkl"))

        print("DATA SAVED!")

        





database = Database()
cluster = ImageCluster(database.images)

print(cluster.clustered_images())