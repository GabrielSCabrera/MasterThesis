from typing import Dict
import re

def B(string:str) -> str:
    '''
        Bold String Formatter
    '''
    return f'\033[1m{string}\033[m'

def I(string:str) -> str:
    '''
        Italic String Formatter
    '''
    return f'\033[3m{string}\033[m'

def config_info(defaults:Dict[str,str]) -> str:
    max_len = max(map(len, defaults.keys())) + 1
    max_len += len(B(''))
    title = 'DEFAULTS'
    centered = max_len + max(map(len, map(str, defaults.values())))
    out = f'\n{title:^{centered}s}'
    for key,value in defaults.items():
        key = re.sub(r'_', ' ', key)
        key = key.capitalize()
        out += f'\n{B(key):>{max_len}s}\t{I(value)}'
    out += '\n'
    return out

def clean_str(string:str) -> str:
    '''
        Removes all ANSI escape sequences from given string.
    '''
    pat = r'(\033\[)[0-?]*[ -\/]*[@-~]'
    return re.sub(pat, '', string)
