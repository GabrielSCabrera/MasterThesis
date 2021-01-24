from termios import tcflush, TCIFLUSH
from datetime import datetime
from pathlib import Path
import subprocess
import time
import sys
import re
import os

import numpy as np

from .terminal import clear_line, reset_screen, cursor_up, get_key_press
from ..config.config import delden_relpath, matlab_files_abspath
from ..preprocessing import file_io
from .format import B, I
from . import terminal

def select(title:str, options):
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
            tcflush(sys.stdin, TCIFLUSH)
    selection = options[int(key)-1]
    print(f'\r> {I(selection)}')
    print('–'*40, end = '\n\n')
    return selection

def scroll_select(title:str, options):
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

def select_int(title:str, val_range):
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

def select_float(title:str, val_range):
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

def select_bool(title:str):
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
    if selection.lower() == 'y':
        return True
    elif selection.lower() == 'n':
        return False
    else:
        raise Exception('Unexpected Error')

def select_str(title:str):
    print(B(title))
    selection = input('> ')
    return selection

def select_int_list(title:str):

    print(B(title))
    print(f'Expects {I("space-separated")} integers\n')

    msg = clear_line() + cursor_up() + '\rInvalid input format'

    while True:
        print(f'\r> {clear_line()}', end = '')
        val = input()
        val = re.sub('[ ]+', ' ', val)
        if not re.match(r'^[\d ]+$', val):
            print(msg, end = '')
            time.sleep(2)
            continue
        try:
            val = val.split(' ')
            int_val = list(map(int, val))
        except:
            print(msg, end = '')
            time.sleep(2)
            continue
        else:
            break

    return int_val

def confirm_overwrite(filename, path, extension = None):
    files = file_io.list_files(path, extension)
    if filename in list(files.keys()):
        terminal.reset_screen()
        title = B('Overwrite File ') + I(f'{filename}') + '?'
        return select_bool(title)
    return True

def create_unique_name(prefix:str = None, suffix:str = None) -> str:
    '''
        Generate a filename using the current date and time
    '''
    if prefix is None:
        prefix = ''
    elif prefix[-1] != '_':
        prefix += '_'

    if suffix is None:
        suffix = ''
    elif suffix[0] != '_':
        suffix = '_' + suffix

    datetime_str = f'{datetime.now():%Y-%m-%d %H:%M:%S.%f}'
    filename = f'{prefix}{datetime_str}{suffix}'
    return filename

def run_matlab(script_name:str, variables:str = None, suppress:bool = True):
    '''
        Runs a MATLAB script with the given initial conditions.
    '''
    print(f'\033[1mAttempting to run MATLAB script:\033[m', end = ' ')
    print(f'\033[3m{script_name}\033[m')

    script_path = matlab_files_abspath / script_name
    script = (
        f"try, {variables} run(\'{script_path}\'), catch e, disp(e), exit(1),"
        f"end, exit(0)"
    )
    cmd = f'matlab -nodisplay -nosplash -nodesktop -r "{script}"'

    if suppress:
        cmd += ' > /dev/null'

    completed_process = os.system(cmd)

    if completed_process == 0:
        print('\033[1;32mSuccessfully\033[m\033[1m ran MATLAB script\033[m')
    else:
        print('\033[1;31mFailed\033[m\033[1m to run MATLAB script\033[m')

    return completed_process

def run_matlab_set(scripts:str, variables:str = None, suppress:bool = True):
    '''
        Runs several MATLAB scripts with the given sets of initial conditions.
    '''
    print(
        f'\033[1mAttempting to run multiple MATLAB scripts\033[m', flush = True
    )

    script_str = ''
    for script, var in zip(scripts, variables):
        script_path = matlab_files_abspath / script
        script_str += f"{var} run(\'{script_path}\');"

    catch_str = f"try, {script_str}, catch e, disp(e), exit(1), end, exit(0)"
    script_str = script_str[:-2]
    cmd = f'matlab -nodisplay -nosplash -nodesktop -r "{catch_str}"'

    if suppress:
        cmd += ' > /dev/null'

    completed_process = os.system(cmd)

    if completed_process == 0:
        msg = (
            f'\033[1;32mSuccessfully\033[m\033[1m ran MATLAB scripts in bulk:'
            f'\033[m\n'
        )
        for script in scripts:
            script_path = matlab_files_abspath / script
            msg += f'\n\t{script_path.name}'
        print(msg, flush = True)
    else:
        msg = (
            '\033[1;31mFailed\033[m\033[1m to run MATLAB scripts in bulk\033[m'
        )
        print(msg, flush = True)

    return completed_process
