import numpy as np
import argparse
import time
import sys
import os

from scripts import *

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
            time.sleep(1)
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
        print(f'\r>{clear_line()}', end = '')
        val = input()
        try:
            val = int(val)
        except:
            print(clear_line() + cursor_up(), end = '')
            if val_range is None:
                print(f'\rInput must be an integer', end = '')
            else:
                print(f'\rInput must be an integer in:{valid}', end = '')
            time.sleep(1.5)
        else:
            if val_range is None:
                break
            elif not low <= val <= high:
                print(clear_line() + cursor_up(), end = '')
                print(f'\rInput must be an integer in:{valid}', end = '')
                time.sleep(1.5)
            else:
                break
    return val

"""MAIN SCRIPT"""

args = parse_args()

if args.test is True:
    tests.run_tests()

if args.split is True:

    choices = config.labels
    label = select('Choose a Dataset', choices)
    dataset = config.bins[label]
    dims = dataset.dims

    selection = select('Splitting Options', ['2-D', '3-D'])

    if selection == '2-D':

        options = ['Columns (Vertical)', 'Slices (Horizontal)']
        selection = select('2-D Shape Options', options)

        if selection == 'Columns (Vertical)':
            N_cols = select_int('Select Number of Columns p/ 2-D Slice',
                                [5, dims[0]//5])

        elif selection == 'Slices (Horizontal)':
            pass

    elif selection == '3-D':

        options = ['Columns (Vertical)', 'Slabs (Horizontal)', 'Cubes']
        selection = select('3-D Shape Options', options)

        if selection == 'Columns (Vertical)':
            N_cols = select_int('Select Approx. Number of Columns',
                                [25, dims[0]//5])

        elif selection == 'Slabs (Horizontal)':
            N_cols = select_int('Select Approx. Number of Slabs',
                                [5, dims[2]//5])

        elif selection == 'Cubes':
            N_cols = select_int('Select Approx. Number of Cubes',
                                [125, np.prod(dims)//1000])
