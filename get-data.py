
import pickle
from os import listdir
import cv2

dir_ = './app/static/datasets'
subfolders = ['airplane', 'car', 'cat', 'dog', 'flower', 'fruit', 'motorbike', 'person']

images = []
images_names = []
init_indices = []
stt = 1
for i, sf in enumerate(subfolders):
    init_indices.append(stt)
    subfolder_dir = f'{dir_}/{sf}'
    print(f'fetching {subfolder_dir} --------------')
    for j, f in enumerate(listdir(subfolder_dir)):
        print(f'{stt} - reading {f} ------------x ------')
        img = cv2.imread(f'{subfolder_dir}/{f}')
        images.append(img)
        images_names.append(f)
        stt+=1

with open('images.pickle', 'wb') as f:
    print('dumping images.pickle ... ')
    pickle.dump((images, images_names, init_indices), f)


print('finish.')

