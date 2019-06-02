
import pickle
from os import listdir
import cv2

dir_ = './app/static/datasets'
subfolders = ['airplane', 'car', 'cat', 'dog', 'flower', 'fruit', 'motorbike', 'person']

images = []
images_names = []
for sf in subfolders:
    subfolder_dir = f'{dir_}/{sf}'
    print(f'fetching {subfolder_dir}')
    for f in listdir(subfolder_dir)[:50]:
        print(f'reading {f}')
        img = cv2.imread(f'{subfolder_dir}/{f}')
        images.append(img)
        images_names.append(f)

with open('images.pickle', 'wb') as f:
    print('dumping images.pickle ... ')
    pickle.dump((images, images_names), f)

print('finish.')

