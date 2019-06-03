import pickle
import cv2
import numpy as np

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

with open('images.pickle', 'rb') as f:
    images, images_names, init = pickle.load(f)

print(init)
dsc_list = []

for i, image in enumerate(images):
    print(f'{i} extracting {images_names[i]} features {" - xxxxxxxxx" if i % 2 == 0 else " - xx"}')
    dsc = extract_features(image)
    dsc_list.append(dsc)

with open('dsc_list.pickle', 'wb') as f:
    print('dumping dsc_list.pickle ....')
    pickle.dump(dsc_list, f)
    print('done')
