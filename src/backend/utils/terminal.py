import numpy as np
import termios
import time
import sys
import tty
import os

from .format import B, I
from ..config import fields

def clear_line():
    return '\033[0K'

def reset_screen():
    print('\033[2J\033[H', end = '\r')

def cursor_up():
    return '\033[1A'

def get_key_press():
    last = ['']*7
    output = ''
    active = True
    dt_max = 1E-1
    t0 = time.time()
    digits = ['0','1','2','3','4','5','6','7','8','9']
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
             'q','r','s','t','u','v','w','x','y','z','æ','ø','å',]
    os.system("stty raw -echo")
    while active:
        ch = sys.stdin.read(1)
        t1 = time.time()
        if t1 - t0 > dt_max:
            last = ['']*7
        else:
            last[0:-1] = last[1:]
        last[-1] = ch
        last_str = ''.join(last)
        for key, value in zip(fields.ANSI_keys, fields.ANSI_values):
            if key in last_str:
                if (key in digits or key in alpha) and last_str != key:
                    continue
                else:
                    output = value
                    active = False
                    break
        t0 = t1
    os.system("stty -raw echo")
    return output
