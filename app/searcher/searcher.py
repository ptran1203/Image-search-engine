import cv2
import numpy as np
import os
import pickle
from urllib.request import Request, urlopen
from math import sqrt
from json import dump, load
from matplotlib import pyplot as plt
# from cluster import ImageDescriptor, ImageCluster


# Const
# /app
BASE_DIR = os.path.dirname(os.getcwd())
IMG_PATH = os.path.join(BASE_DIR, "static/images")
BINS = (12, 8, 3)

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

        with open(BASE_DIR + '/cache/img.pkl', 'rb') as f:
            self.data = pickle.load(f)

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
        with open(BASE_DIR + '/cache/img.pkl', 'wb') as f:
            pickle.dump(data, f)

        print("DATA SAVED!")

        
