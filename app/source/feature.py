import cv2
import os
import numpy as np
import json
import re
import scipy
from urllib.request import urlopen, Request
from math import sqrt
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

# TODO: avoid importError when use helper in index.py
try:
    from helper import (
        gray, show, pickle_load, pickle_save, json_load, json_save,
        is_cached
    )
except ImportError:
    from source.helper import (
        gray, show, pickle_load, pickle_save, json_load, json_save,
        is_cached
    )


BASE_DIR = os.path.join(os.getcwd(), "app")
EXTRACTOR = cv2.xfeatures2d.SIFT_create()
IMG_DIR = os.path.join(BASE_DIR, "static/datasets")
NUM_OF_IMGS = {
    "airplane" : 727,
    "car": 968,
    "cat": 885,
    "dog": 702,
    "flower": 843,
    "fruit": 1000,
    "motobike": 788,
    "person": 986,
}

# paths map for save, load data
PATHS = {
    "images": os.path.join(BASE_DIR, "cache/images.pkl"),
    "model": os.path.join(BASE_DIR, "cache/model.pkl"),
    "feature_vectors": os.path.join(BASE_DIR, "cache/feature_vectors.pkl"),
    "clustered": os.path.join(BASE_DIR, "cache/clustered.pkl"),    
}

class ImageDescriptor:
    def __init__(self, path, is_train_image=True):
        self.is_train_image = is_train_image
        self.image = self._getimg(path)
        self.keypoint, self.descriptors = self._features(EXTRACTOR)

    @staticmethod
    def _file_name(path, rex):
        return re.search(rex, path).group()

    @staticmethod
    def _getimg(path):
        if "http" in path or "data:image" in path:
            res = urlopen(Request(path, headers={'User-Agent': 'Mozilla/5.0'}))
            array = np.asarray(bytearray(res.read()), dtype=np.uint8)
            img = cv2.imdecode(array, -1)
            if img is not None:
                return img
        return cv2.imread(path)

    def _features(self, extractor):
        dimensions = 64
        image = gray(self.image)
        kps = extractor.detect(image)
        kps = sorted(kps, key=lambda x: -x.response)[:dimensions]
        keypoints, descriptors = extractor.compute(image, kps)
        if descriptors is None:
            descriptors = np.zeros(0)

        return keypoints, descriptors


class ImageCluster:
    def __init__(self, images, n=8):
        self.images = images
        self.kmeans = KMeans(n_clusters=n)
        self.kmeans.fit(np.array(self._descriptor_list()))

    def _descriptor_list(self):
        res = []
        for img_dsc in self.images.values():
            for dsc in img_dsc:
                res.append(dsc)

        return res

    def histogram(self, img_dsc):
        if type(img_dsc).__module__ != np.__name__:
            img_dsc = img_dsc.descriptors
        his = np.zeros(len(self.kmeans.cluster_centers_))
        prediction = self.kmeans.predict(img_dsc)
        # print(prediction)
        for pre in prediction:
            his[pre] += 1
        return his

    def create_histograms(self):
        res = {}
        for img, dsc in self.images.items():
            res[img] = self.histogram(dsc)

        return res        


class Database:
    def __init__(self, number_of_images=0):
        if not is_cached(PATHS['images']):
            self.build(number_of_images)

        self.images = pickle_load(PATHS['images'])

    @staticmethod
    def build(num=0):
        data = {}
        sub_dirs = [i for i in os.listdir(IMG_DIR) if i.endswith('DS_Store') == False]
        if num > 0:
            sub_dirs = sub_dirs[:num]
        for sdir in sub_dirs:
            subpaths = os.path.join(IMG_DIR, sdir)
            for file in os.listdir(subpaths):
                if (file.endswith('DS_Store')):
                    continue
                path = os.path.join(subpaths, file)
                data[file] = ImageDescriptor(path).descriptors
        pickle_save(data, PATHS['images'])

class Searcher:
    def __init__(self, cluster_object):
        self.cluster = cluster_object

    @staticmethod
    def _cosine(vectora, vectorb):
        return scipy.spatial.distance.cdist(
            # euclidean or cosine
            vectora.reshape(1, -1), vectorb.reshape(1, -1), 'cosine'
        )

    @staticmethod
    def _cache(obj, classname):
        saveobj = [_[0] for _ in obj[:NUM_OF_IMGS[classname]]]
        json_save(saveobj,
                os.path.join(BASE_DIR,
                "cache/result/"+classname+".json"))


    def search(self, imgpath, limit=10):
        img_dsc = ImageDescriptor(imgpath, True)
        if img_dsc.image is None:
            return None
        fea_vector = self.cluster.histogram(img_dsc)
        images = self.cluster.images
        feature_vectors = pickle_load(PATHS["feature_vectors"])
        cos_dict = {}

        rex = re.compile(r'_[0-9]+.[a-z]+')
        for name, fea_vec in feature_vectors.items():
            path = os.path.join("/static/datasets/", re.sub(rex,'', name),name)
            cos_dict[name] = (
                self._cosine(fea_vector, fea_vec),
                path
            )

        res = sorted(cos_dict.items(), key=lambda x: x[1][0])

        self._cache(res, 'dog')
        return res[:limit]

# load cluster model
def loadmodel():
    return pickle_load(PATHS["model"])


if __name__ == "__main__":
    from feature import *
    from time import time
    print("START building...")
    start = time()
    db = Database()
    end = time()
    print("Data has been generated in %s seconds" % (end - start))
    cluster = None
    if not is_cached(PATHS["model"]):
        start = time()
        cluster = ImageCluster(db.images, 200)
        end = time()
        print("Kmeans has been trained in %s seconds" % (end - start))
        print("saving data....")
        pickle_save(cluster, PATHS["model"])
    else:
        cluster = pickle_load(PATHS["model"])
    pickle_save(cluster.create_histograms(),PATHS["feature_vectors"])
    print("DONE!")

    