## use for testing

from feature import (
    ImageCluster,
    ImageDescriptor
)
import cv2
base = "/home/ptran/git/Image-search-engine/app/"
imgpath = base + "static/datasets/airplane/airplane_0002.jpg"
# imgpath = base + "static/datasets/cat/cat_0496.jpg"

img = cv2.imread(imgpath)
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

EXTRACTOR = cv2.xfeatures2d.SIFT_create()
kps = EXTRACTOR.detect(gray)
kps = sorted(kps, key=lambda x: -x.response)[:32]
img=cv2.drawKeypoints(gray,kps,None)

cv2.imshow('fmask.jpg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# print(img.keypoint)