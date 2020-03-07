import numpy as np
import time
import sys
import os

from .format import B, I

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
