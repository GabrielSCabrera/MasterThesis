from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

from src.backend.config import config

def argparser(**kwargs):
    '''
        Prepares saving and loading variables in a standardized way.
    '''
    if 'directory' not in kwargs.keys():
        raise ValueError('Missing argument `directory`!')
    else:
        directory = kwargs['directory']

    if 'savename' not in kwargs.keys():
        savename = directory
    else:
        savename = kwargs['savename']

    if 'datapath' not in kwargs.keys():
        datapath = config.delvol_relpath
    else:
        datapath = kwargs['datapath']

    if 'savepath' not in kwargs.keys():
        savepath = config.matlab_img_relpath
    else:
        savepath = kwargs['savepath']

    load = datapath / directory
    save = savepath / savename

    return load, save

def load_combined(load_path:Path):
    '''
        Loads combined data and returns it as a dict of dicts.

        Structure:

            {
                'EXP1' : {
                    y_train         :   List[np.ndarray],
                    y_test          :   List[np.ndarray],
                    y_train_pred    :   List[np.ndarray],
                    y_test_pred     :   List[np.ndarray],
                    scores          :   np.ndarray,
                    final           :   np.ndarray,
                },
                'EXP2' : {
                    y_train         :   List[np.ndarray],
                    y_test          :   List[np.ndarray],
                    y_train_pred    :   List[np.ndarray],
                    y_test_pred     :   List[np.ndarray],
                    scores          :   np.ndarray,
                    final           :   np.ndarray,
                },
                ...
            }
    '''
    dirs = load_path.glob('*')
    all_data = {}

    files = ['y_train', 'y_test', 'y_train_pred', 'y_test_pred']
    ext = '.csv'

    for d in dirs:
        if d.is_dir():
            new_dict = {}
            for f in files:

                data = []
                with open(load_path / d / (f + ext) , 'r') as infile:
                    for line in infile:
                        data.append(np.array(
                            line.strip().split(','), dtype = np.float64
                        ))
                new_dict[f] = data

            new_dict['scores'] = np.loadtxt(
                load_path / d / 'scores.csv', delimiter = ','
            )
            all_data[d.name] = new_dict

    with open(load_path / 'scores.csv', 'r') as infile:
        for line in infile:
            line = line.split(',')
            key = line[0]
            value = np.array(line[1:], dtype = np.float64)
            all_data[key]['final'] = value

    return all_data

def histogram(combined_data, ylim:Tuple[float] = None, text = None):
    '''
        Creates a dotted histogram from a set of combined results comparing
        their R²-values.
    '''
    x_vals = []
    x_labels = []
    x_vals_unique = []
    y_vals_test = []
    y_vals_train = []
    for n, (k, v) in enumerate(combined_data.items()):
        x_labels.append(k)
        x_vals_unique.append(n)
        for score in v['scores']:
            y_vals_train.append(score[0])
            y_vals_test.append(score[1])
            x_vals.append(n)

    x_vals = np.array(x_vals)
    x_vals_unique = np.array(x_vals_unique)
    y_vals_train = np.array(y_vals_train)
    y_vals_test = np.array(y_vals_test)
    x_labels = np.array(x_labels)

    idx = np.argsort(x_labels)
    x_labels = x_labels[idx]
    idx_map = {i:j for i,j in zip(idx, x_vals_unique)}

    x_vals_final = []
    for i in x_vals:
        x_vals_final.append(idx_map[i])

    plt.figure(figsize = (12.8, 9.6))
    plt.plot(x_vals_final, y_vals_train, 'C0x', label = 'Training Set')
    plt.plot(x_vals_final, y_vals_test, 'r^', label = 'Testing Set')
    plt.xticks(x_vals_unique, x_labels)

    if ylim is not None:
        plt.ylim(ylim)

    title = '$R^2$ Scores for Several Models from Multiple Experiments'

    if text is not None:
        title += text

    plt.title(title)
    plt.xlabel('Experiment Label')
    plt.ylabel('$R^2$ Score')
    plt.legend(loc = 4, bbox_to_anchor=(1, 1, 0, 0))
    plt.grid()
    plt.show()
    plt.close()

def errorbars(combined_data, ylim:Tuple[float] = None, text = None):
    '''
        Creates a dotted histogram from a set of combined results comparing
        their R²-values.
    '''
    x_vals = []
    x_labels = []
    mean_R2 = []
    std_R2 = []

    mean_idx = 1
    std_idx = 5

    for n, (k, v) in enumerate(combined_data.items()):
        x_labels.append(k)
        x_vals.append(n)
        mean_R2.append(v['final'][mean_idx])
        std_R2.append(v['final'][std_idx])

    x_vals = np.array(x_vals)
    x_labels = np.array(x_labels)
    mean_R2 = np.array(mean_R2)
    std_R2 = np.array(std_R2)

    idx = np.argsort(x_labels)
    x_labels = x_labels[idx]
    idx_map = {i:j for i,j in zip(idx, x_vals)}

    x_vals_final = []
    for i in x_vals:
        x_vals_final.append(idx_map[i])

    plt.figure(figsize = (12.8, 9.6))

    plt.errorbar(
        x = x_vals_final, y = mean_R2, yerr = std_R2, fmt = 'rs', capsize = 10,
        ecolor = 'C0', mfc = 'w'
    )

    plt.xticks(x_vals, x_labels)
    if ylim is not None:
        plt.ylim(ylim)

    title = 'Mean $R^2$ Scores (and Error) for Multiple Experiments'

    if text is not None:
        title += text

    plt.title(title)
    plt.xlabel('Experiment Label')
    plt.ylabel('Mean $R^2$ Score')
    plt.grid()
    plt.show()
    plt.close()

def chart_exp_pred(combined_data):
    '''
        Creates a chart that compares the expected vs. predicted results in a
        set of combined results.
    '''
    for n, (k1, v1) in enumerate(combined_data.items()):
        pass
