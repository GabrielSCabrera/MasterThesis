import numpy as np
from .. import config

def save_split(label, X_train, X_test, y_train, y_test):
    path = config.split_bins_relpath + label
    np.savez_compressed(path, X_train = X_train, X_test = X_test,
                              y_train = y_train, y_test = y_test)

def load_split(label):
    path = config.split_bins_relpath + label
    if '.npz' not in path:
        path += '.npz'
    data = np.load(path)
    return data['X_train'], data['X_test'], data['y_train'], data['y_test']
