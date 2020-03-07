import numpy as np
import argparse
import time
import sys
import os

from scripts import *

globals()['status_entries'] = []

def parse_args():

    argparse_desc = ('Runs various aspects of the rock fracture analysis '
                     'depending on the sequence of included command-line '
                     'arguments.')

    help_split = ('Splits and saves the dataset into four arrays: X_train, '
                  'X_test, y_train, y_test.')

    help_train_DNN = ('Create and train a model based on a previously split and '
                  'saved dataset.')

    parser = argparse.ArgumentParser(description = argparse_desc)

    parser.add_argument('--test', action='store_true', help = 'Runs all tests')
    parser.add_argument('--split', action='store_true', help = help_split)
    parser.add_argument('--train_DNN', action='store_true', help = help_train_DNN)

    return parser.parse_args()

def update_status(new_entry):
    tab_len = len('Prev. Selections:') + 7
    tot_len = tab_len
    max_len = 80
    for entry in globals()['status_entries']:
        if entry == '<newline>':
            continue
        elif tot_len + len(entry) >= max_len:
            tot_len = tab_len + len(entry) + 3
        else:
            tot_len += len(entry) + 3
    if tot_len + len(new_entry) >= max_len:
        globals()['status_entries'].append('<newline>')
    globals()['status_entries'].append(new_entry)

def display_status():
    tab_len = len('Prev. Selections:') + 7
    status = format.B('Prev. Selections:') + ' '*7
    for entry in globals()['status_entries']:
        if entry == '<newline>':
            status += '\n' + ' '*tab_len
        else:
            status += f'{format.I(entry)} > '
    status = status[:-3]
    print(status, end = '\n\n')

"""MAIN SCRIPT"""

args = parse_args()

if args.test is True:
    tests.run_tests()

if args.split is True:

    terminal.reset_screen()

    choices = config.labels
    label = terminal.select('Choose a Dataset', choices)
    dataset = config.bins[label]
    dims = dataset.dims
    split_dataset = None

    terminal.reset_screen()
    update_status(label)
    display_status()

    savename = terminal.select_str('Save As')

    terminal.reset_screen()
    update_status('Save As ' + savename + '.npz')
    display_status()

    selection = terminal.select('Splitting Options', ['2-D', '3-D'])

    terminal.reset_screen()
    update_status(selection)
    display_status()

    shuffle = not terminal.select_bool('Split by Region?')

    terminal.reset_screen()
    if shuffle is True:
        update_status('Random')
    else:
        update_status('Split')
    display_status()

    limit = terminal.select_float('Dataset Size', [1E-3, 1])

    terminal.reset_screen()
    update_status(f'{limit*100:g}% of Data')
    display_status()

    if selection == '2-D':

        options = ['Columns (Vertical)', 'Slices (Horizontal)']
        selection = terminal.select('2-D Shape Options', options)

        terminal.reset_screen()
        update_status(selection)
        display_status()

        if selection == options[0]:
            N_cols = terminal.select_int('Select Number of Columns p/ 2-D Slice',
                                [5, dims[0]//5])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_cols,
                        'mode'        :   'col',
                        'test_size'   :   0.25,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_2D.test_train_split(**params)

        elif selection == options[1]:

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   None,
                        'mode'        :   'slice',
                        'test_size'   :   0.25,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_2D.test_train_split(**params)

    elif selection == '3-D':

        options = ['Columns (Vertical)', 'Slabs (Horizontal)', 'Cubes']
        selection = terminal.select('3-D Shape Options', options)

        terminal.reset_screen()
        update_status(selection)
        display_status()

        if selection == options[0]:
            N_cols = terminal.select_int('Select Approx. Number of Columns',
                                [25, dims[0]//5])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_cols,
                        'mode'        :   'col',
                        'test_size'   :   0.25,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_3D.test_train_split(**params)

        elif selection == options[1]:
            N_slices = terminal.select_int('Select Approx. Number of Slabs',
                                [5, dims[2]//5])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_slices,
                        'mode'        :   'slice',
                        'test_size'   :   0.25,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_3D.test_train_split(**params)

        elif selection == options[2]:
            N_cubes = terminal.select_int('Select Approx. Number of Cubes',
                                [125, np.prod(dims)//1000])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_cubes,
                        'mode'        :   'cube',
                        'test_size'   :   0.25,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_3D.test_train_split(**params)

    if split_dataset is None:
        raise Exception('Unexpected Error')

    X_train, X_test, y_train, y_test = split_dataset
    print(B('Saving Segments'))
    file_io.save_split(savename, X_train, X_test, y_train, y_test)
    print(B('Saved to ') + I(f'{config.split_bins_relpath}{savename}.npz'))

if args.train_DNN is True:

    label = 'small_dataset'

    layers = (512, 256, 128, 64)
    model = DNN.Model(hidden_layer_sizes = layers, verbose = True)

    X_train, X_test, y_train, y_test =\
    file_io.load_split(label = label)

    X_train, X_test, y_train, y_test =\
    reshape.reshape_1D(X_train, X_test, y_train, y_test)

    X_train, X_test, y_train, y_test =\
    convert.float64(X_train, X_test, y_train, y_test)

    model.fit(X_train, y_train)

    model.save(label)
