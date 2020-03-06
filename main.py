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

    parser = argparse.ArgumentParser(description = argparse_desc)

    parser.add_argument('--test', action='store_true', help = 'Runs all tests')
    parser.add_argument('--split', action='store_true', help = help_split)

    return parser.parse_args()

def B(string):
    '''Bold String Formatter'''
    return f'\033[1m{string}\033[m'

def I(string):
    '''Italic String Formatter'''
    return f'\033[3m{string}\033[m'

def clear_line():
    return '\033[0K'

def reset_screen():
    print('\033[2J\033[H', end = '\r')

def cursor_up():
    return '\033[1A'

def getKeyPress():
    os.system("stty raw -echo")
    key = sys.stdin.read(1)
    os.system("stty -raw echo")
    return key

def select(title, options):
    print(B(title), end = '\n\n')
    for n, option in enumerate(options):
        print(B(f"{n+1})") + '\t' + I(option))
    print('\n' + B("Q)") + '\t' + I('Quit'))
    print(f'\n{B("Select one of the above")}')
    valid = np.arange(1, len(options)+1).astype(str)
    while True:
        print(f'\r>{clear_line()}', end = '')
        key = getKeyPress()
        if key in valid:
            break
        elif str(key).lower() == 'q':
            print('\r> User Exit')
            exit()
        else:
            print('\rInvalid Selection!', end = '')
            time.sleep(1.5)
    selection = options[int(key)-1]
    print(f'\r> {I(selection)}')
    print('–'*40, end = '\n\n')
    return selection

def select_int(title, val_range):
    '''
        val_range: list of two ints, with val_range[0] < val_range[1]
    '''
    if val_range is None:
        print(B(title))
    else:
        low = val_range[0]
        high = val_range[1]
        valid = f' [{low:g}, {high:g}]'
        print(B(title + ':') + valid)
    while True:
        print(f'\r> {clear_line()}', end = '')
        val = input()
        try:
            val = int(val)
        except:
            print(clear_line() + cursor_up(), end = '')
            if val_range is None:
                print(f'\rInput must be an integer', end = '')
            else:
                print(f'\rInput must be an integer in:{valid}', end = '')
            time.sleep(2)
        else:
            if val_range is None:
                break
            elif not low <= val <= high:
                print(clear_line() + cursor_up(), end = '')
                print(f'\rInput must be an integer in:{valid}', end = '')
                time.sleep(2)
            else:
                break
    return int(val)

def select_float(title, val_range):
    '''
        val_range: list of two floats, with val_range[0] < val_range[1]
    '''
    if val_range is None:
        print(B(title))
    else:
        low = val_range[0]
        high = val_range[1]
        valid = f' [{low:g}, {high:g}]'
        print(B(title + ':') + valid)
    while True:
        print(f'\r> {clear_line()}', end = '')
        val = input()
        try:
            val = float(val)
        except:
            print(clear_line() + cursor_up(), end = '')
            if val_range is None:
                print(f'\rInput must be a number', end = '')
            else:
                print(f'\rInput must be a number in:{valid}', end = '')
            time.sleep(2)
        else:
            if val_range is None:
                break
            elif not low <= val <= high:
                print(clear_line() + cursor_up(), end = '')
                print(f'\rInput must be a number in:{valid}', end = '')
                time.sleep(2)
            else:
                break
    return float(val)

def select_bool(title):
    print(B(title) + I(" [Y/n]"))

    while True:
        print(f'\r>{clear_line()}', end = '')
        key = str(getKeyPress())
        if key.lower() == 'q':
            print('\r> User Exit')
            exit()
        elif key.lower() in ['y','n']:
            selection = key
            break
        else:
            print('\rInvalid Selection!', end = '')
            time.sleep(1.5)
    print(f'\r> {I(selection)}')
    print('–'*40, end = '\n\n')
    if selection.lower() == 'y':
        return True
    elif selection.lower() == 'n':
        return False
    else:
        raise Exception('Unexpected Error')

def select_str(title):
    print(B(title))
    selection = input('> ')
    return selection

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
    status = B('Prev. Selections:') + ' '*7
    for entry in globals()['status_entries']:
        if entry == '<newline>':
            status += '\n' + ' '*tab_len
        else:
            status += f'{I(entry)} > '
    status = status[:-3]
    print(status, end = '\n\n')

"""MAIN SCRIPT"""

args = parse_args()

if args.test is True:
    tests.run_tests()

if args.split is True:

    reset_screen()

    choices = config.labels
    label = select('Choose a Dataset', choices)
    dataset = config.bins[label]
    dims = dataset.dims
    split_dataset = None

    reset_screen()
    update_status(label)
    display_status()

    savename = select_str('Save As')

    reset_screen()
    update_status('Save As ' + savename + '.npz')
    display_status()

    selection = select('Splitting Options', ['2-D', '3-D'])

    reset_screen()
    update_status(selection)
    display_status()

    shuffle = not select_bool('Split by Region?')

    reset_screen()
    if shuffle is True:
        update_status('Random')
    else:
        update_status('Split')
    display_status()

    limit = select_float('Dataset Size', [1E-3, 1])

    reset_screen()
    update_status(f'{limit*100:g}% of Data')
    display_status()

    if selection == '2-D':

        options = ['Columns (Vertical)', 'Slices (Horizontal)']
        selection = select('2-D Shape Options', options)

        reset_screen()
        update_status(selection)
        display_status()

        if selection == options[0]:
            N_cols = select_int('Select Number of Columns p/ 2-D Slice',
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
        selection = select('3-D Shape Options', options)

        reset_screen()
        update_status(selection)
        display_status()

        if selection == options[0]:
            N_cols = select_int('Select Approx. Number of Columns',
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
            N_slices = select_int('Select Approx. Number of Slabs',
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
            N_cubes = select_int('Select Approx. Number of Cubes',
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
