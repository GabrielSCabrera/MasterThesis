import numba as nb
import numpy as np

from .. import utils
from .. import config

@nb.njit(cache = True)
def jit_make_groups(frame, min_cluster_size, msg, comp_dirs):
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

    strings = utils.jit_tools.jit_loading_bar_print(msg, perc)
    print(strings[0])
    print(perc)
    print(strings[1])

    # FIRST PASS (FINDING)

    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            for k in range(frame.shape[2]):
                count += 1
                new_perc = int(100*count/tot_iter)
                if new_perc > perc:
                    perc = new_perc
                    strings = utils.jit_tools.jit_loading_bar_print(msg, perc)
                    print(strings[0])
                    print(perc)
                    print(strings[1])
                if frame[i,j,k] == 1:
                    smallest_label = label
                    labels = []
                    for l in range(len(comp_dirs)):
                        new_idx = np.array([i,j,k])
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
    groups = np.zeros(len(connected), dtype = np.int64)
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

    # SECOND PASS (GROUPING)
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            for k in range(frame.shape[2]):
                count += 1
                new_perc = int(100*count/tot_iter)
                if new_perc > perc:
                    perc = new_perc
                    strings = utils.jit_tools.jit_loading_bar_print(msg, perc)
                    print(strings[0])
                    print(perc)
                    print(strings[1])
                if frame[i,j,k] > 0:
                    frame[i,j,k] = groups[frame[i,j,k]-2]

    return frame

def filter_clusters(frame, min_cluster_size):
    '''
        Removes clusters of size < min_cluster_size
    '''
    maximum = np.max(frame)
    new_groups = np.zeros(maximum, dtype = np.int64)
    removed = np.zeros(maximum, dtype = np.uint8)
    label = 1
    # Setting values to zero
    for n in range(maximum):
        new_groups[n] = label
        if np.sum(np.equal(frame, n+1)) < min_cluster_size:
            removed[n] = 1
            frame[frame == n+1] = 0
        else:
            label += 1

    # Redefining groups
    for n,i in enumerate(new_groups):
        if removed[n] == 0:
            frame[frame == n+1] = i
    return frame

def get_indices(frame, min_cluster_size, msg, comp_dirs, savename):
    frame = jit_make_groups(frame, min_cluster_size, msg, comp_dirs)
    frame = filter_clusters(frame, min_cluster_size)
    maximum = np.max(frame)
    groups = []
    for i in range(maximum):
        groups.append(np.array(np.where(frame == i)).T)
    return groups

def extract_clusters(dataset, min_cluster_size = 5, savename):
    '''
        min_cluster_size: int >= 1
    '''

    clusters = []
    fail_times = dataset.fail_times
    # os.mkdir(config.clusters_relpath)

    x,y,z = np.meshgrid([-1,0,1], [-1,0,1], [-1,0,1])
    x = x.flatten(); y = y.flatten(); z = z.flatten();
    comp_dirs = np.array([x,y,z]).T
    comp_dirs = np.delete(comp_dirs, 13, axis = 0)

    # Iterating through each time-step of given dataset
    for n, (frame, fail) in enumerate(zip(dataset, fail_times)):
        #TODO Save arrays to file in each iteration instead of keeping in RAM
        low, high = 500, 600
        frame = frame.copy()[low:high,low:high,low:high]
        msg = f'FRAME [{n+1}/{len(dataset)}]'
        groups = get_indices(frame, min_cluster_size, msg, comp_dirs)
        clusters.append({'fail':fail, 'groups':groups})

    print(clusters)
