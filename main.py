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

    parser.add_argument('--unit_tests', action='store_true', help = 'Runs all unit tests')
    parser.add_argument('--test', action='store_true', help = 'Runs the latest test script')
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
        elif tot_len + len(entry) + 3 >= max_len:
            tot_len = tab_len + len(entry) + 3
        else:
            tot_len += len(entry) + 3
    if tot_len + len(new_entry) >= max_len:
        globals()['status_entries'].append('<newline>')
    globals()['status_entries'].append(new_entry)

def display_status():
    tab_len = len('Prev. Selections:') + 7
    status = format.B('Prev. Selections:') + ' '*7
    for n,entry in enumerate(globals()['status_entries']):
        if entry == '<newline>':
            status += '\n' + ' '*tab_len
        elif n == len(globals()['status_entries'])-1:
            status += f'{format.I(entry)}'
        else:
            status += f'{format.I(entry)} > '
    return status + '\n'

"""MAIN SCRIPT"""

args = parse_args()

if args.unit_tests is True:
    tests.run_tests()

if args.split is True:

    terminal.reset_screen()

    choices = config.labels
    label = select.select('Choose a Dataset', choices)
    dataset = config.bins[label]
    dims = dataset.dims
    split_dataset = None

    update_status(label)

    while True:
        terminal.reset_screen()
        print(display_status())
        savename = select.select_str('Save As')
        if not savename.strip():
            continue
        if '.npz' not in savename:
            savename += '.npz'
        sel = select.confirm_overwrite(savename, config.split_bins_relpath,
                                       '.npz')
        if sel is True:
            break

    terminal.reset_screen()
    update_status(f'Save As \'{savename}\'')
    print(display_status())

    test_size = select.select_float('Test Size', [0.05, 0.9])

    terminal.reset_screen()
    update_status(f'Train {100*(1-test_size):g}% & Test {100*(test_size):g}%')
    print(display_status())

    selection = select.select('Splitting Options', ['2-D', '3-D'])

    terminal.reset_screen()
    update_status(selection)
    print(display_status())

    shuffle = not select.select_bool('Split by Region?')

    terminal.reset_screen()
    if shuffle is True:
        update_status('Random')
    else:
        update_status('Split')
    print(display_status())

    if selection == '2-D':

        options = ['Columns (Vertical)', 'Slices (Horizontal)']
        selection = select.select('2-D Shape Options', options)

        terminal.reset_screen()
        update_status(selection)
        print(display_status())

        if selection == options[0]:

            min_cols = 2
            min_size = min(min_cols/(dims[0]), 1)

            limit = select.select_float('Dataset Size', [min_size, 1])

            terminal.reset_screen()
            update_status(f'{limit*100:g}% of Data')
            print(display_status())

            max_cols = int(limit*dims[0]//4)
            N_cols = select.select_int('Select Number of Columns p/ 2-D Slice',
                                        [min_cols, max_cols])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_cols,
                        'mode'        :   'col',
                        'test_size'   :   test_size,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_2D.test_train_split(**params)

        elif selection == options[1]:

            min_slices = 2

            min_size = min(min_slices/(dims[2]), 1)

            limit = select.select_float('Dataset Size', [min_size, 1])

            terminal.reset_screen()
            update_status(f'{limit*100:g}% of Data')
            print(display_status())

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   None,
                        'mode'        :   'slice',
                        'test_size'   :   test_size,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_2D.test_train_split(**params)

    elif selection == '3-D':

        options = ['Columns (Vertical)', 'Slabs (Horizontal)', 'Cubes']
        selection = select.select('3-D Shape Options', options)

        terminal.reset_screen()
        update_status(selection)
        print(display_status())

        if selection == options[0]:

            min_cols = 4

            min_size = min(min_cols**2/(min(dims[:2])**2), 1)

            limit = select.select_float('Dataset Size', [min_size, 1])

            terminal.reset_screen()
            update_status(f'{limit*100:g}% of Data')
            print(display_status())

            max_cols = int(limit*dims[0]*dims[1]//4)
            N_cols = select.select_int('Select Approx. Number of Columns',
                                         [min_cols, max_cols])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_cols,
                        'mode'        :   'col',
                        'test_size'   :   test_size,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_3D.test_train_split(**params)

        elif selection == options[1]:

            min_slabs = 4

            min_size = min(min_slabs/dims[2], 1)

            limit = select.select_float('Dataset Size', [min_size, 1])

            terminal.reset_screen()
            update_status(f'{limit*100:g}% of Data')
            print(display_status())

            max_slabs = int(limit*dims[2]//2)
            N_slices = select.select_int('Select Approx. Number of Slabs',
                                            [min_slabs, max_slabs])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_slices,
                        'mode'        :   'slice',
                        'test_size'   :   test_size,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_3D.test_train_split(**params)

        elif selection == options[2]:

            min_cubes = 8

            min_size = min(min_cubes**2/(min(dims)**3), 1)

            limit = select.select_float('Dataset Size', [min_size, 1])

            terminal.reset_screen()
            update_status(f'{limit*100:g}% of Data')
            print(display_status())

            max_cubes = int(limit*min(dims)**3//8)
            N_cubes = select.select_int('Select Approx. Number of Cubes',
                                          [min_cubes, max_cubes])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_cubes,
                        'mode'        :   'cube',
                        'test_size'   :   test_size,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_3D.test_train_split(**params)

    if split_dataset is None:
        raise Exception('Unexpected Error')

    X_train, X_test, y_train, y_test = split_dataset
    print(format.B('Saving Segments'))
    file_io.save_split(savename, X_train, X_test, y_train, y_test)
    print(format.B('Saved to ') + format.I(f'{config.split_bins_relpath}{savename}.npz'))

if args.train_DNN is True:

    terminal.reset_screen()

    files = file_io.list_files(config.split_bins_relpath, '.npz')

    if not files:
        msg = (f'{format.B("No Split-Data Files to Load")}\n'
               f'Run script with flag {format.I("--split")} to split a dataset '
               f'into {format.I("training")} and {format.I("testing")} sets, '
               'and save the results.')
        print(msg)
        exit()

    split_file = select.scroll_select('Select a File for Training',
                                      list(files.keys()))

    update_status(f'Load \'{split_file}\'')

    while True:
        terminal.reset_screen()
        print(display_status())
        savename = select.select_str('Save Model As')
        if not savename.strip():
            continue
        if config.DNN_model_extension not in savename:
            savename += config.DNN_model_extension
        sel = select.confirm_overwrite(savename, config.DNN_models_relpath,
                                       config.DNN_model_extension)
        if sel is True:
            break

    terminal.reset_screen()
    update_status(f'Save As \'{savename}\'')
    print(display_status())

    print(format.B("Loading Split Data"))

    X_train, X_test, y_train, y_test =\
    file_io.load_split(label = split_file)

    print(format.B("Reshaping Data"))

    X_train, X_test, y_train, y_test =\
    reshape.reshape_1D(X_train, X_test, y_train, y_test)

    print(format.B("Resizing Data"))

    X_train, X_test, y_train, y_test =\
    convert.float64(X_train, X_test, y_train, y_test)

    layers = (512, 256, 128, 64)
    model = DNN.Model(hidden_layer_sizes = layers)

    model.fit(X_train, y_train)

    model.save(savename)

if args.test is True:

    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
             'q','r','s','t','u','v','w','x','y','z','æ','ø','å']

    opt = ["argparse",
           "scripts",
           "globals",
           "status_entries",
           "parse_args",
           "update_status",
           "display_status",
           "parse_args",
           "unit_tests",
           "split",
           "train_DNN",
           "test"]

    # sel = terminal.scroll_select('A Title About The List', opt)
    # print('Selection: ', sel)

    # files = file_io.list_files(config.DNN_models_relpath, config.DNN_model_extension)
    files = file_io.list_files(config.split_bins_relpath, '.npz')
    sel = select.scroll_select('Select a File', list(files.keys()))
    print(f'Selected {sel}: {files[sel]}')
