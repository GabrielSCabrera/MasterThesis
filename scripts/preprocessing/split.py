import numpy as np
import config

def split_cols_idx(dataset, splits, test_size = 0.25):
    """
        splits – approximate number of columns to create (>= 25)
    """
    dims = dataset.dims
    splits_root = max(5, int(np.sqrt(splits)))

    x_idx_max = (dims[0]//splits_root)*splits_root
    y_idx_max = (dims[1]//splits_root)*splits_root

    x_idx = np.linspace(0, x_idx_max, splits_root, dtype = np.int64)
    y_idx = np.linspace(0, y_idx_max, splits_root, dtype = np.int64)

    x_idx_low = x_idx[:-1]
    y_idx_low = y_idx[:-1]

    x_idx_high = x_idx[1:]
    y_idx_high = y_idx[1:]

    y_idx = np.array([slice(i,j) for i,j in zip(y_idx_low, y_idx_high)])
    x_idx = np.array([slice(i,j) for i,j in zip(x_idx_low, x_idx_high)])

    x_idx, y_idx = np.meshgrid(x_idx, y_idx)

    x_idx = np.ravel(x_idx)
    y_idx = np.ravel(y_idx)
    z_idx = np.array([slice(0, dims[2])]*len(x_idx))

    idx = [[i,j,k] for i,j,k in zip(x_idx, y_idx, z_idx)]
    idx = np.array(idx)

    N_cols = idx.shape[0]
    N_test = int(N_cols*test_size)
    idx_test = np.random.choice(N_cols, N_test, replace = False)
    idx_train = np.arange(0, N_cols)
    idx_train = np.delete(idx_train, idx_test)
    np.random.shuffle(idx_train)

    return idx[idx_train], idx[idx_test]

def split_cubes_idx(dataset, splits, test_size = 0.25):
    """
        splits – approximate number of cubes to create (>= 125)
    """
    dims = dataset.dims
    splits_root = max(5, int(np.cbrt(splits)))

    x_idx_max = (dims[0]//splits_root)*splits_root
    y_idx_max = (dims[1]//splits_root)*splits_root
    z_idx_max = (dims[2]//splits_root)*splits_root

    x_idx = np.linspace(0, x_idx_max, splits_root, dtype = np.int64)
    y_idx = np.linspace(0, y_idx_max, splits_root, dtype = np.int64)
    z_idx = np.linspace(0, z_idx_max, splits_root, dtype = np.int64)

    x_idx_low = x_idx[:-1]
    y_idx_low = y_idx[:-1]
    z_idx_low = z_idx[:-1]

    x_idx_high = x_idx[1:]
    y_idx_high = y_idx[1:]
    z_idx_high = z_idx[1:]

    x_idx = np.array([slice(i,j) for i,j in zip(x_idx_low, x_idx_high)])
    y_idx = np.array([slice(i,j) for i,j in zip(y_idx_low, y_idx_high)])
    z_idx = np.array([slice(i,j) for i,j in zip(z_idx_low, z_idx_high)])

    x_idx, y_idx, z_idx = np.meshgrid(x_idx, y_idx, z_idx)

    x_idx = np.ravel(x_idx)
    y_idx = np.ravel(y_idx)
    z_idx = np.ravel(z_idx)

    idx = [[i,j,k] for i,j,k in zip(x_idx, y_idx, z_idx)]
    idx = np.array(idx)

    N_cols = idx.shape[0]
    N_test = int(N_cols*test_size)
    idx_test = np.random.choice(N_cols, N_test, replace = False)
    idx_train = np.arange(0, N_cols)
    idx_train = np.delete(idx_train, idx_test)
    np.random.shuffle(idx_train)

    return idx[idx_train], idx[idx_test]

def split_slices_idx(dataset, splits, test_size = 0.25):
    """
        splits – approximate number of slices to create (>= 25)
    """
    dims = dataset.dims

    z_idx = np.linspace(0, dims[2], splits, dtype = np.int64)

    z_idx_low = z_idx[:-1]
    z_idx_high = z_idx[1:]

    z_idx = np.array([slice(i,j) for i,j in zip(z_idx_low, z_idx_high)])

    x_idx = np.array([slice(0, dims[0])]*len(z_idx))
    y_idx = np.array([slice(0, dims[1])]*len(z_idx))

    idx = [[i,j,k] for i,j,k in zip(x_idx, y_idx, z_idx)]
    idx = np.array(idx)

    N_cols = idx.shape[0]
    N_test = int(N_cols*test_size)
    idx_test = np.random.choice(N_cols, N_test, replace = False)
    idx_train = np.arange(0, N_cols)
    idx_train = np.delete(idx_train, idx_test)
    np.random.shuffle(idx_train)

    return idx[idx_train], idx[idx_test]

def test_train_split(dataset, fail_times, splits, mode, test_size = 0.25):
    if mode == 'col':
        dummy1, dummy2 = split_cols_idx(dataset, splits, test_size)
    elif mode == 'slice':
        dummy1, dummy2 = split_slices_idx(dataset, splits, test_size)
    elif mode == 'cube':
        dummy1, dummy2 = split_cubes_idx(dataset, splits, test_size)

    step_iter = len(dummy1) + len(dummy2)
    tot_iter = len(dataset)*step_iter

    X_train = []
    X_test = []

    y_train = []
    y_test = []

    perc = 0
    for m, sample in enumerate(dataset):

        if m >= 3:
            break

        if mode == 'col':
            indices_train, indices_test = \
            split_cols_idx(dataset, splits, test_size)
        elif mode == 'slice':
            indices_train, indices_test = \
            split_slices_idx(dataset, splits, test_size)
        elif mode == 'cube':
            indices_train, indices_test = \
            split_cubes_idx(dataset, splits, test_size)

        for n, idx_train in enumerate(indices_train):

            X_train.append(sample[idx_train[0], idx_train[1], idx_train[1]])
            y_train.append(fail_times[m])

            # LOADING BAR
            new_perc = int(100*(m*step_iter + n)/tot_iter)
            if new_perc > perc:
                perc = new_perc
                print(f'\rLoading Segments {perc:3d}%', end = '')

        for n, idx_test in enumerate(indices_test):

            X_test.append(sample[idx_test[0], idx_test[1]])
            y_test.append(fail_times[m])

            # LOADING BAR
            new_perc = int(100*(m*step_iter + n + len(indices_train))/tot_iter)
            if new_perc > perc:
                perc = new_perc
                print(f'\rLoading Segments {perc:3d}%', end = '')

    # LOADING BAR
    print(f'\rLoading Segments {100:3d}%')

    X_train = np.array(X_train, dtype = np.uint8)
    y_train = np.array(y_train, dtype = np.uint8)

    X_test = np.array(X_test, dtype = np.uint8)
    y_test = np.array(y_test, dtype = np.uint8)

    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    label = 'M8_1'
    splits = 200
    dataset = config.bins[label]
    fail_times = config.bin_fail_times[label]
    X_train, X_test, y_train, y_test = \
    test_train_split(dataset, fail_times, splits, mode = 'cube')
