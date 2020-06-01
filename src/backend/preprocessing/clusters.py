from multiprocessing import Pool
from time import time
import numba as nb
import numpy as np
import shutil
import os

from .. import config
from .. import utils

@nb.njit(cache = True)
def jit_make_groups(frame, min_cluster_size, msg1, msg2, comp_dirs):
    '''
        Numba accelerated function to extract groups of ones from a 3-D binary
        numpy array.  Uses the Hoshen–Kopelman algorithm:

        < https://en.wikipedia.org/wiki/Hoshen%E2%80%93Kopelman_algorithm >
    '''
    tot_iter = 2*frame.size
    count = 0
    perc = 0
    label = 0
    connected = [[2]]

    strings = utils.jit_tools.jit_loading_bar_print(msg1, perc)
    print(strings[0])
    print(perc)
    print(strings[1])

    # FIRST PASS (FINDING)

    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            for k in range(frame.shape[2]):
                count += 1
                new_perc = int(100*count/frame.size)
                if new_perc > perc:
                    perc = new_perc
                    strings = utils.jit_tools.jit_loading_bar_print(msg1, perc)
                    print(strings[0])
                    print(perc)
                    print(strings[1])
                if frame[i,j,k] == 1:
                    smallest_label = label
                    labels = []
                    for l in range(len(comp_dirs)):
                        new_idx = np.array([i,j,k], config.cluster_uint_type)
                        new_idx += comp_dirs[l]
                        if 0 <= new_idx[0] < frame.shape[0] and\
                           0 <= new_idx[1] < frame.shape[1] and\
                           0 <= new_idx[2] < frame.shape[2]:

                            val = frame[new_idx[0],new_idx[1],new_idx[2]]
                            if 1 < val:
                                labels.append(val)
                    if not labels:
                        frame[i,j,k] = label+2
                        label += 1
                        connected.append([label+2])
                    else:
                        smallest = min(labels)
                        frame[i,j,k] = smallest
                        for l in labels:
                            if l not in connected[smallest-2]:
                                connected[smallest-2].append(l)

    # SORTING GROUPS
    groups = np.zeros(len(connected), dtype = config.cluster_uint_type)
    for i in range(2, label+3):
        for c in connected:
            if i in c:
                low = min(c)
                if groups[low-2] > 1:
                    groups[i-2] = groups[low-2]
                else:
                    groups[i-2] = low
                break

    group_keys = np.array(list(set(groups)))
    group_map = {}

    for n,key in enumerate(group_keys):
        group_map[key] = n+1

    for i in range(len(groups)):
        groups[i] = group_map[groups[i]]

    count = 0
    perc = 0
    strings = utils.jit_tools.jit_loading_bar_print(msg2, perc)
    print(strings[0])
    print(perc)
    print(strings[1])

    # SECOND PASS (GROUPING)
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            for k in range(frame.shape[2]):
                count += 1
                new_perc = int(100*count/frame.size)
                if new_perc > perc:
                    perc = new_perc
                    strings = utils.jit_tools.jit_loading_bar_print(msg2, perc)
                    print(strings[0])
                    print(perc)
                    print(strings[1])
                if frame[i,j,k] > 0:
                    frame[i,j,k] = groups[frame[i,j,k]-2]

    maximum = np.max(frame)
    return frame, maximum

def filter_clusters(frame, maximum, min_cluster_size, msg):
    '''
        Removes clusters of size < min_cluster_size
    '''
    new_groups = np.zeros(maximum, dtype = config.cluster_uint_type)
    removed = np.zeros(maximum, dtype = config.cluster_uint_type)
    label = 1

    count = 0
    perc = 0
    msg3 = msg.format(3)
    strings = utils.jit_tools.jit_loading_bar_print(msg3, perc)
    print(strings[0])
    print(perc)
    print(strings[1])

    # Setting values to zero
    for n in range(maximum):
        new_groups[n] = label
        if np.sum(np.equal(frame, n+1)) < min_cluster_size:
            removed[n] = 1
            frame[frame == n+1] = 0
        else:
            label += 1
        count += 1
        new_perc = int(100*count/maximum)
        if new_perc > perc:
            perc = new_perc
            strings = utils.jit_tools.jit_loading_bar_print(msg3, perc)
            print(strings[0])
            print(perc)
            print(strings[1])

    count = 0
    perc = 0
    msg4 = msg.format(4)
    strings = utils.jit_tools.jit_loading_bar_print(msg4, perc)
    print(strings[0])
    print(perc)
    print(strings[1])

    # Redefining groups
    for n,i in enumerate(new_groups):
        if removed[n] == 0:
            frame[frame == n+1] = i
        count += 1
        new_perc = int(100*count/maximum)
        if new_perc > perc:
            perc = new_perc
            strings = utils.jit_tools.jit_loading_bar_print(msg4, perc)
            print(strings[0])
            print(perc)
            print(strings[1])

    return frame

def direct_to_file(path, idx, mac_fail, frame, maximum, msg):
    '''
        Parses through each element in 'frame' and saves points to their
        respective files.

        Replacement for np.where, which raises a MemoryError.
    '''
    files = []
    label = config.cluster_metadata_labels['T_macroscopic_failure']
    for i in range(maximum):
        cluster_path = path / config.cluster_dir_labels.format(idx+i)
        os.mkdir(cluster_path)
        files.append(open(cluster_path / config.cluster_data, 'w+'))
        with open(cluster_path / config.cluster_metadata, 'w+') as outfile:
            outfile.write(f'{label}={mac_fail}')

    count = 0
    perc = 0
    msg5 = msg.format(5)
    strings = utils.jit_tools.jit_loading_bar_print(msg5, perc)
    print(strings[0])
    print(perc)
    print(strings[1])

    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            for k in range(frame.shape[2]):
                if frame[i,j,k] != 0:
                    files[frame[i,j,k]-1].write(f'{i:d},{j:d},{k:d}\n')
                count += 1
                new_perc = int(100*count/frame.size)
                if new_perc > perc:
                    perc = new_perc
                    strings = utils.jit_tools.jit_loading_bar_print(msg5, perc)
                    print(strings[0])
                    print(perc)
                    print(strings[1])

    for f in files:
        f.close()

    return idx + maximum

def get_indices(frame, min_cluster_size, msg, comp_dirs, path, idx, mac_fail):
    msg1 = msg.format(1)
    msg2 = msg.format(2)
    frame, maximum = jit_make_groups(frame, min_cluster_size, msg1, msg2, comp_dirs)
    if maximum > 0:
        frame = filter_clusters(frame, maximum, min_cluster_size, msg)
        t2 = time()
        idx = direct_to_file(path, idx, mac_fail, frame, maximum, msg)
        t3 = time()
    return idx

def extract_clusters(dataset, savename, min_cluster_size = 5):
    '''
        min_cluster_size: int >= 1
    '''
    clusters = []
    fail_times = dataset.fail_times
    path = config.clusters_relpath / savename

    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    idx = 0

    x,y,z = np.meshgrid([-1,0,1], [-1,0,1], [-1,0,1])
    x = x.flatten(); y = y.flatten(); z = z.flatten()
    comp_dirs = np.array([x,y,z], dtype = config.cluster_uint_type).T
    comp_dirs = np.delete(comp_dirs, 13, axis = 0)

    # Iterating through each time-step of given dataset
    for n, (frame, mac_fail) in enumerate(zip(dataset, fail_times)):
        low, high = 510, 550
        frame = frame.copy()[low:high,low:high,low:high]
        msg = 'STEP [{:d}/5] ' + f'FRAME [{n+1}/{len(dataset)}]'
        frame_new = frame.copy()
        idx = get_indices(frame_new, min_cluster_size, msg, comp_dirs, path,
                          idx, mac_fail)
