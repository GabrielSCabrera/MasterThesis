from .terminal import clear_line, reset_screen, cursor_up, get_key_press
from ..preprocessing import file_io
from .format import B, I
from . import terminal
import numpy as np
import time

def select(title, options):
    print(B(title), end = '\n\n')
    for n, option in enumerate(options):
        print(B(f"{n+1})") + '\t' + I(option))
    print('\n' + B("Q)") + '\t' + I('Quit'))
    print(f'\n{B("Select one of the above")}')
    valid = np.arange(1, len(options)+1).astype(str)
    while True:
        print(f'\r>{clear_line()}', end = '')
        key = get_key_press()
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

def scroll_select(title, options):
    max_len = min(len(options), 9)
    opt_enum = [i+1 for i in range(len(options))]

    while True:

        reset_screen()

        print(B(title))
        print(f'\n   Scroll With Arrow-Keys {B("UP")} and {B("DOWN")}')
        print(f'   Select with {B("ENTER")}')
        print(f'   {B("Q")} to {B("QUIT")}', end = '\n\n')
        print('┌─┐')
        print('│▲│')

        for n, option in enumerate(options[0:max_len]):
            num = '│ │' +  B(f'{opt_enum[n]:>5d}  ')
            if n == max_len//2:
                print(num + ' \033[48;7m<' + I(option) + '\033[48;7m>\033[m')
                selection = option
            else:
                print(num + '  ' + option)

        print('│▼│')
        print('└─┘')

        key = get_key_press()
        if key == 'Down':
            options[0:-1], options[-1] = options[1:], options[0]
            opt_enum[0:-1], opt_enum[-1] = opt_enum[1:], opt_enum[0]
        elif key == 'Up':
            options[1:], options[0] = options[0:-1], options[-1]
            opt_enum[1:], opt_enum[0] = opt_enum[0:-1], opt_enum[-1]
        elif key == 'Enter':
            return selection
        elif key == 'q':
            exit()

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
    print(B(title) + I(" [Y/n](q)"))

    while True:
        print(f'\r>{clear_line()}', end = '')
        key = str(get_key_press())
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

def confirm_overwrite(filename, path, extension = None):
    files = file_io.list_files(path, extension)
    if filename in list(files.keys()):
        terminal.reset_screen()
        title = B('Overwrite File ') + I(f'{filename}') + '?'
        return select_bool(title)
    return True
