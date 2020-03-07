import numpy as np

def as_type(X_train, X_test, y_train, y_test, new_type):
    X_train = X_train.astype(new_type)
    X_test = X_test.astype(new_type)
    y_train = y_train.astype(new_type)
    y_test = y_test.astype(new_type)

    return X_train, X_test, y_train, y_test

def float32(X_train, X_test, y_train, y_test):
    X_train = X_train.astype(np.float32)
    X_test = X_test.astype(np.float32)
    y_train = y_train.astype(np.float32)
    y_test = y_test.astype(np.float32)

    return X_train, X_test, y_train, y_test

def float64(X_train, X_test, y_train, y_test):
    X_train = X_train.astype(np.float64)
    X_test = X_test.astype(np.float64)
    y_train = y_train.astype(np.float64)
    y_test = y_test.astype(np.float64)

    return X_train, X_test, y_train, y_test

def uint8(X_train, X_test, y_train, y_test):
    X_train = X_train.astype(np.uint8)
    X_test = X_test.astype(np.uint8)
    y_train = y_train.astype(np.uint8)
    y_test = y_test.astype(np.uint8)

    return X_train, X_test, y_train, y_test
