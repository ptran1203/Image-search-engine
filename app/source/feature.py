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
    from helper import gray, show, load, save
except ImportError:
    from source.helper import gray, show, load, save


BASE_DIR = os.path.join(os.getcwd(), "app")
EXTRACTOR = cv2.xfeatures2d.SURF_create()
IMG_DIR = os.path.join(BASE_DIR, "static/datasets")

class ImageDescriptor:
    def __init__(self, path):
        self.image = self._getimg(path)
        # self.path = path
        self.keypoint, self.descriptor = self._features(EXTRACTOR)

    @staticmethod
    def _getimg(path):
        if "http" in path:
            res = urlopen(Request(path, headers={'User-Agent': 'Mozilla/5.0'}))
            array = np.asarray(bytearray(res.read()), dtype=np.uint8)
            img = cv2.imdecode(array, -1)
            if img is not None:
                print(type(img))
                return img

        return cv2.imread(path)

    def _features(self, extractor):
        image = gray(self.image)
        kps = extractor.detect(image)
        kps = sorted(kps, key=lambda x: -x.response)[:32]
        keypoints, descriptor = extractor.compute(image, kps)
        if descriptor is None:
            descriptor = np.zeros(0)
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
        if type(img_dsc).__module__ != np.__name__:
            img_dsc = img_dsc.descriptor
        res = self.kmeans.predict(
            img_dsc.reshape(1 , -1)
        )
        return res

    def clustered_images(self):
        res = {}
        for name, descriptor in self.images.items():
            if descriptor is not None:
                key = self.predict(descriptor)[0] or None
                if key:
                    if key not in res:
                        res[key] = []
                    res[key].append(name)
        return res


class Database:
    def __init__(self, number_of_images=0,cached=True):
        if not cached:
            self.build(number_of_images)

        self.images = load(os.path.join(BASE_DIR, "cache/images.pkl"))

    @staticmethod
    def build(num=0):
        print("START building...")
        data = {}
        sub_dirs = os.listdir(IMG_DIR)
        if num > 0:
            sub_dirs = sub_dirs[:num]
        length = len(sub_dirs)
        for sdir in sub_dirs:
            subpaths = os.path.join(IMG_DIR, sdir)
            for file in os.listdir(subpaths):
                path = os.path.join(subpaths, file)
                data[file] = ImageDescriptor(path).descriptor
                # print("progress: %s/ %s" %(i + 1, len(sub_dirs)))

        print("DONE!!")
        save(data, os.path.join(BASE_DIR, "cache/images.pkl"))

        print("DATA SAVED!")

class Searcher:
    def __init__(self, cluster_object):
        self.cluster = cluster_object

    @staticmethod
    def _cosine(vectora, vectorb):
        return scipy.spatial.distance.cdist(
            # euclidean or cosine
            vectora.reshape(1, -1), vectorb.reshape(1, -1), 'cosine'
        )

    def search(self, imgpath, limit=10):
        img_dsc = ImageDescriptor(imgpath)
        if img_dsc.image is None:
            return None
        img_pre = self.cluster.predict(img_dsc)
        images = self.cluster.images
        matched_imgs = load(
            os.path.join(BASE_DIR, "cache/clustered.pkl")
        )
        cos_dict = {}
        rex = re.compile(r'_[0-9]+.[a-z]+')
        for name in matched_imgs[img_pre[0]]:
            path = os.path.join("/static/datasets/", re.sub(rex,'', name),name)
            cos_dict[name] = (
                self._cosine(img_dsc.descriptor,
                        images[name]),
                path
            )

        res = sorted(cos_dict.items(), key=lambda x: -x[1][0])[:10]
        return res[:limit]

# load cluster model
def loadmodel():
    return load(os.path.join(BASE_DIR, "cache/model.pkl"))


if __name__ == "__main__":
    from feature import *
    # import time
    # cluster = loadmodel()    
    # searcher = Searcher(cluster)
    # imgpath = os.path.join(IMG_DIR, "person", "person_0000.jpg")
    # start = time.time()
    # res = searcher.search(imgpath)
    # end = time.time()
    # print(res)
    # rebuild-all
    db = Database(0, False)
    cluster = ImageCluster(db.images, 32)
    #cache
    save(cluster.clustered_images(),
        os.path.join(BASE_DIR, "cache/clustered.pkl"))
    save(cluster, os.path.join(BASE_DIR, "cache/model.pkl"))