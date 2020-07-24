import numpy as np

def reshape_1D(X_train, X_test, y_train, y_test):

    new_shapes = {}

    new_shapes['X_train'] = (X_train.shape[0], np.prod(X_train.shape[1:]))
    new_shapes['X_test'] = (X_test.shape[0], np.prod(X_test.shape[1:]))
    new_shapes['y_train'] = (y_train.shape[0],)
    new_shapes['y_test'] = (y_test.shape[0],)

    X_train = X_train.reshape(new_shapes['X_train'])
    X_test = X_test.reshape(new_shapes['X_test'])
    y_train = y_train.reshape(new_shapes['y_train'])
    y_test = y_test.reshape(new_shapes['y_test'])

    return X_train, X_test, y_train, y_test
