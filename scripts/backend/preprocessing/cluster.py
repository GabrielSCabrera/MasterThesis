from numba import njit, prange
import numpy as np

from .. import utils
from .. import config

@njit(cache = True)
def jit_search_closest(frame, idx):
    dirs = np.zeros(6, dtype = np.uint8)
    return [idx]


@njit(cache = True)
def jit_extract_frame(frame, min_cluster_size, msg, tot_iter):
    '''
        Numba accelerated function to extract groups of ones from a 3-D binary
        numpy array
    '''
    groups = []
    count = 0
    perc = 0
    utils.jit_tools.jit_loading_bar_print(msg, perc)
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            count += 1
            new_perc = int(100*count/tot_iter)
            if new_perc > perc:
                perc = new_perc
                utils.jit_tools.jit_loading_bar_print(msg, perc)
            for k in range(frame.shape[2]):
                new_groups = jit_search_closest(frame, (i,j,k))
                if new_groups:
                    groups.append(new_groups)
    return 0

def extract_clusters(dataset, min_cluster_size = 1):
    '''
        min_cluster_size: int >= 1
    '''

    clusters = []

    fail_times = dataset.fail_times

    pad_width = ((1, 1), (1, 1), (1, 1))

    # Iterating through each time-step of given dataset
    for n, (frame, fail) in enumerate(zip(dataset, fail_times)):
        print(frame.size)
        exit()
        msg = f'\rFRAME [{n+1}/{len(dataset)}]'
        tot_iter = frame.size
        groups = jit_extract_frame(frame, min_cluster_size, msg, tot_iter)
        clusters.append({'fail':fail, 'groups':groups})
