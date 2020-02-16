import numpy as np
import config

def split_cols_idx(dataset, splits, seed = 1337, test_size = 0.25):
    """
        splits – approximate number of columns to create (>= 25)
    """
    np.random.seed(seed)
    dims = dataset.dims
    splits_root = max(5, int(np.sqrt(splits)))

    x_idx_max = (dims[0]//splits_root)*splits_root
    y_idx_max = (dims[0]//splits_root)*splits_root

    x_idx = np.linspace(0, x_idx_max, splits_root, dtype = np.int64)
    y_idx = np.linspace(0, y_idx_max, splits_root, dtype = np.int64)

    x_idx, y_idx = np.meshgrid(x_idx, y_idx)

    x_idx = np.ravel(x_idx)
    y_idx = np.ravel(y_idx)

    xy_idx = np.vstack([x_idx, y_idx]).T
    idx_low = xy_idx[:-1]
    idx_high = xy_idx[1:]

    idx = []
    for i,j in zip(idx_low, idx_high):
        idx.append([slice(i[0],j[0]), slice(i[1],j[1])])
    idx = np.array(idx)

    N_cols = idx.shape[0]
    N_test = int(N_cols*test_size)
    idx_test = np.random.choice(N_cols, N_test, replace = False)
    idx_train = np.arange(0, N_cols)
    idx_train = np.delete(idx_train, idx_test)
    np.random.shuffle(idx_train)

    return idx_train, idx_test

def yield_cols(dataset, idx_train, fail_times):
    N_samples = dataset.samples*idx_train.shape[0]
    
    print(N_samples, dataset.samples)
    print(fail_times)
    # for i in idx:
    #     yield(dataset)

if __name__ == "__main__":
    label = 'M8_1'
    dataset = config.bins[label]
    fail_times = config.bin_fail_times[label]
    idx_train, idx_test = split_cols_idx(dataset, 121)
    yield_cols(dataset, idx_train, fail_times)
