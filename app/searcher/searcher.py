import cv2
import numpy as np
import os
from urllib.request import Request, urlopen
from math import sqrt
from json import dump, load
import mahotas as mt
from matplotlib import pyplot as plt

# Const
BASE_DIR = os.getcwd() + "/app"
IMG_PATH = BASE_DIR + "/static/images/"
BINS = (12, 8, 3)

class ImageDescriptor:
    def __init__(self, path, isLocal=True):
        self.img = self._get_img(path, isLocal)

    def _get_img(self, path, isLocal):
        if isLocal:
            return cv2.imread(path)

        if ("http") in path:
            res = urlopen(Request(path, headers={'User-Agent': 'Mozilla/5.0'}))
            array = np.asarray(bytearray(res.read()), dtype=np.uint8)
            img = cv2.imdecode(array, -1)
            if img is not None:
                return img
        
        return cv2.imdecode(
        np.fromstring(
            path.read(), np.uint8
            ), cv2.IMREAD_UNCHANGED
        )


    def histogram(self, mask):
        hist = cv2.calcHist(
            [self.img], [0, 1, 2], mask, BINS, [0, 256, 0, 256, 0, 256] 
        )
        hist = cv2.normalize(hist, hist).flatten()

        return [float(x) for x in hist.tolist()]

    def color_feature(self):
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        h, w = self.img.shape[:2]
        topmask = np.zeros((h, w),np.uint8)
        botmask = np.zeros((h, w),np.uint8)
        cv2.rectangle(topmask, (0, 0), (h//2, w), 255, -1)
        cv2.rectangle(botmask, (h//2, 0), (h, w), 255, -1)
        features = self.histogram(topmask)
        features.extend(self.histogram(botmask))
        return features

    def plot_hist(self):
        plt.hist(self.histogram(None), normed=False, bins=256)
        # plt.hist(self.img, normed=False, bins=256)
        plt.ylabel('Probability')
        plt.show()

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
    def __init__(self, isCached=True):
        if not isCached:
            self.build()

        with open(BASE_DIR + '/cache/img.json', 'r') as f:
            self.data = load(f)

    @staticmethod
    def build():
        print("START building...")
        data = {}
        files = os.listdir(IMG_PATH)
        length = len(files)
        for i, file in enumerate(files):
            path = IMG_PATH + file
            data[file] = ImageDescriptor(path).color_feature()
            print("progress: %s/ %s" %(i + 1, len(files)))

        print("DONE!!")
        with open(BASE_DIR + '/cache/img.json', 'w') as f:
            dump(data, f, indent=4, sort_keys=True)

        print("DATA SAVED!")
            

def main():
    # build the data
    database = Database(False)

    # img1 = ImageDescriptor(cv2.imread(IMG_PATH + "200000.jpg"))
    # img2 = ImageDescriptor(cv2.imread(IMG_PATH + "215000.jpg"))
    # img1.plot_hist()
    # img2.plot_hist()
    # searcher = Searcher(img1.color_feature(), database.data).search()
    # print(searcher)


if __name__ == "__main__":
    main()

        
