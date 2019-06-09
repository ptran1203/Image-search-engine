import numpy as np
from sklearn.metrics import precision_recall_fscore_support
import matplotlib.pyplot as plt
from feature import BASE_DIR, NUM_OF_IMGS
import os
from helper import json_load

def name(file_name):
    names = [
        'airplane', 'car', 'cat', 'dog', 'flower',
        'fruit', 'motorbike', 'person'
    ]
    for name in names:
        if name in file_name:
            return name
    return False

def cal(y_true, y_pre):
    return {
        "all": precision_recall_fscore_support(
                    y_true, y_pre, average=None
                ),
        "avg": precision_recall_fscore_support(
                    y_true, y_pre, average="micro"
                )
    }

def get_pre(classname):
    path = os.path.join(BASE_DIR,
                "cache/result/"+classname+".json")
    data = json_load(path)
    return [name(x) for x in data]


if __name__ == "__main__":
    y_true = np.array(['dog']*NUM_OF_IMGS['dog'])
    y_pre = np.array(get_pre('dog'))
    print(list(y_pre).count('dog'))
    res = cal(y_true, y_pre)
    precision, recall, x, y = res['all']

    # print(list(recall))
    avg = res['avg']
    print(avg)
    ## draw chart
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('PR chart')

    plt.plot(sorted(recall, reverse=True),
            sorted(precision))

    # plt.plot(
    #     recall, precision
    # )

    plt.savefig(os.path.join(BASE_DIR,
                'static/images/PRchart.png'))