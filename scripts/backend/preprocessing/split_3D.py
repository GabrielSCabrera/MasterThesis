import numpy as np

from ..utils import format

def split_cols_idx(dataset, splits, test_size = 0.25, limit = 1, shuffle = True):
    """
        splits – approximate number of columns to create
    """
    dims = dataset.dims
    splits_root = int(np.sqrt(splits/limit))
    step = max(int(np.cbrt(1/limit)), 1)

    x_idx_max = (dims[0]//splits_root+1)*splits_root
    y_idx_max = (dims[1]//splits_root+1)*splits_root

    x_idx = np.arange(0, x_idx_max, splits_root, dtype = np.int64)
    y_idx = np.arange(0, y_idx_max, splits_root, dtype = np.int64)

    x_idx = np.array([slice(i,j,step) for i,j in zip(x_idx[:-1], x_idx[1:])])
    y_idx = np.array([slice(i,j,step) for i,j in zip(y_idx[:-1], y_idx[1:])])

    x_idx, y_idx = np.meshgrid(x_idx, y_idx)

    x_idx = np.ravel(x_idx)
    y_idx = np.ravel(y_idx)
    z_idx = np.array([slice(None)]*len(x_idx))

    idx = [[i,j,k] for i,j,k in zip(x_idx, y_idx, z_idx)]
    idx = np.array(idx)

    N_cols = idx.shape[0]
    N_test = max(int(N_cols*test_size), 1)

    if shuffle:
        idx_test = np.random.choice(N_cols, N_test, replace = False)
    else:
        idx_test = np.random.choice(N_test, N_test, replace = False)

    idx_train = np.arange(0, N_cols)
    idx_train = np.delete(idx_train, idx_test)
    np.random.shuffle(idx_train)

    train_lim = int(limit*len(idx_train))
    test_lim = int(limit*len(idx_test))
    return idx[idx_train[:train_lim]], idx[idx_test[:test_lim]]

def split_cubes_idx(dataset, splits, test_size = 0.25, limit = 1, shuffle = True):
    """
        splits – approximate number of cubes to create
    """
    dims = dataset.dims
    splits_root = int(np.cbrt(splits/limit))
    step = max(int(np.cbrt(1/limit)), 1)

    x_idx_max = (dims[0]//splits_root+1)*splits_root
    y_idx_max = (dims[1]//splits_root+1)*splits_root
    z_idx_max = (dims[2]//splits_root+1)*splits_root

    x_idx = np.arange(0, x_idx_max, splits_root, dtype = np.int64)
    y_idx = np.arange(0, y_idx_max, splits_root, dtype = np.int64)
    z_idx = np.arange(0, z_idx_max, splits_root, dtype = np.int64)

    x_idx = np.array([slice(i,j,step) for i,j in zip(x_idx[:-1], x_idx[1:])])
    y_idx = np.array([slice(i,j,step) for i,j in zip(y_idx[:-1], y_idx[1:])])
    z_idx = np.array([slice(i,j,step) for i,j in zip(z_idx[:-1], z_idx[1:])])

    x_idx, y_idx, z_idx = np.meshgrid(x_idx, y_idx, z_idx)

    x_idx = np.ravel(x_idx)
    y_idx = np.ravel(y_idx)
    z_idx = np.ravel(z_idx)

    idx = [[i,j,k] for i,j,k in zip(x_idx, y_idx, z_idx)]
    idx = np.array(idx)

    N_cubes = idx.shape[0]
    N_test = max(int(N_cubes*test_size), 1)

    if shuffle:
        idx_test = np.random.choice(N_cubes, N_test, replace = False)
    else:
        idx_test = np.random.choice(N_test, N_test, replace = False)

    idx_train = np.arange(0, N_cubes)
    idx_train = np.delete(idx_train, idx_test)
    np.random.shuffle(idx_train)

    return idx[idx_train], idx[idx_test]

def split_slices_idx(dataset, splits, test_size = 0.25, limit = 1, shuffle = True):
    """
        splits – approximate number of slices to create (>= 25)
    """
    dims = dataset.dims
    z_idx_max = (dims[2]//(splits/limit)+1)*splits
    step = max(int(1/limit), 1)

    z_idx = np.arange(0, z_idx_max, splits, dtype = np.int64)

    z_idx = np.array([slice(i,j,step) for i,j in zip(z_idx[:-1], z_idx[1:])])

    x_idx = np.array([slice(0,dims[0])]*len(z_idx))
    y_idx = np.array([slice(0,dims[1])]*len(z_idx))

    idx = [[i,j,k] for i,j,k in zip(x_idx, y_idx, z_idx)]
    idx = np.array(idx)

    N_slices = idx.shape[0]
    N_test = max(int(N_slices*test_size), 1)

    if shuffle:
        idx_test = np.random.choice(N_slices, N_test, replace = False)
    else:
        idx_test = np.random.choice(N_test, N_test, replace = False)

    idx_train = np.arange(0, N_slices)
    idx_train = np.delete(idx_train, idx_test)
    np.random.shuffle(idx_train)

    train_lim = int(limit*len(idx_train))
    test_lim = int(limit*len(idx_test))
    return idx[idx_train[:train_lim]], idx[idx_test[:test_lim]]

def test_train_split(dataset, splits, mode, test_size = 0.25, limit = 1, shuffle = True):

    X_train = None
    y_train = None

    X_test = None
    y_test = None

    fail_times = dataset.fail_times

    perc = 0
    for m, sample in enumerate(dataset):

        if mode == 'col':
            indices_train, indices_test = \
            split_cols_idx(dataset, splits, test_size, limit, shuffle)
        elif mode == 'slice':
            indices_train, indices_test = \
            split_slices_idx(dataset, splits, test_size, limit, shuffle)
        elif mode == 'cube':
            indices_train, indices_test = \
            split_cubes_idx(dataset, splits, test_size, limit, shuffle)

        if X_train is None:

            shape1 = len(indices_train)*len(dataset)
            idx_train = indices_train[0]
            shape2 = sample[idx_train[0], idx_train[1], idx_train[2]].shape

            X_train = np.zeros((shape1, shape2[0], shape2[1], shape2[2]), dtype = np.uint8)
            y_train = np.zeros((shape1), dtype = np.uint8)

            shape1 = len(indices_test)*len(dataset)
            idx_test = indices_test[0]
            shape2 = sample[idx_test[0], idx_test[1], idx_test[2]].shape

            X_test = np.zeros((shape1, shape2[0], shape2[1], shape2[2]), dtype = np.uint8)
            y_test = np.zeros((shape1), dtype = np.uint8)

            step_iter = len(indices_train) + len(indices_test)
            tot_iter = len(dataset)*step_iter
            idx_iter = 0

        for n, idx_train in enumerate(indices_train):

            X_train[idx_iter] = sample[idx_train[0], idx_train[1], idx_train[2]]
            y_train[idx_iter] = fail_times[m]

            # LOADING BAR
            new_perc = int(100*(m*step_iter + n)/tot_iter)
            if new_perc > perc:
                perc = new_perc
                print(format.B('\rLoading Segments ') + format.I(f'{perc:3d}%'), end = '')

        for n, idx_test in enumerate(indices_test):

            X_test[idx_iter] = sample[idx_test[0], idx_test[1], idx_test[2]]
            y_test[idx_iter] = fail_times[m]

            # LOADING BAR
            new_perc = int(100*(m*step_iter + n + len(indices_train))/tot_iter)
            if new_perc > perc:
                perc = new_perc
                print(format.B('\rLoading Segments ') + format.I(f'{perc:3d}%'), end = '')

        idx_iter += 1

    # LOADING BAR
    print(format.B('\rLoading Segments ') + format.I(f'{100:3d}%'))

    return X_train, X_test, y_train, y_test
