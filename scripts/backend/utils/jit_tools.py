from numba import njit
import numpy as np

@njit(cache = True)
def jit_loading_bar_print(string, perc):
    '''
        PURPOSE
        To print the percentage loaded while in numba's jit nopython mode

        PARAMETERS
        string      <str> to be printed before the percentage
        perc        <int> in range [0, 100]

        RETURNS
        Series of strings to be printed once this function is called
        Example usage:

            >>> jit_loading_bar_print('Loading Bar Message', 5)
              5% Loading Bar Message

            >>> jit_loading_bar_print('Loading Bar Message', 15)
             15% Loading Bar Message

            >>> jit_loading_bar_print('Loading Bar Message', 100)
            100% Loading Bar Message
    '''
    if perc == 0:
        digs = 1
    else:
        digs = int(np.log10(perc)+1)

    if digs == 1:
        whitespace = '   '
        right = '\033[1C'
    elif digs == 2:
        whitespace = '  '
        right = '\033[2C'
    elif digs == 3:
        whitespace = ' '
        right = '\033[3C'

    upline = '\033[1A\033[80C'
    save = '\033[s'
    load = '\033[u'
    startline = '\033[999D'
    clearline = '\033[0K'

    print(upline + startline + right + save + clearline + upline)
    print(perc)
    print(load + '%' + whitespace + string)
