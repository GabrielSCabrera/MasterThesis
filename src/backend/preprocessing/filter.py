import numpy as np

def remove_empty(X_train, X_test, y_train, y_test, N = 0):
    """
        Removes datapoints that consist solely (or mostly) of zeros
        N: minimum number of ones in training and testing datapoints
    """
    idx_del = np.sum(X_train, axis = (1,2,3))
    idx_del = np.where(idx_del > N)[0]
    np.delete(X_train, idx_del)
    np.delete(y_train, idx_del)

    idx_del = np.sum(X_train, axis = (1,2,3))
    idx_del = np.where(idx_del > N)[0]
    np.delete(X_test, idx_del)
    np.delete(y_test, idx_del)

    return X_train, X_test, y_train, y_test
