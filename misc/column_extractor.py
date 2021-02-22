from pathlib import Path
from typing import Dict
import re

import matplotlib.pyplot as plt
import numpy as np

def get_col(path:Path, label:str):
    with open(path, 'r') as infile:
        header = infile.readline().split(' ')
        data = infile.readlines()

    idx = None
    for n,i in enumerate(header):
        if i.lower() == label.lower():
            idx = n

    assert idx is not None, f'No column `{label}` found!'

    data = np.array([i.split(' ') for i in data])
    column = data[:,idx].astype(np.float64)
    return column

def ID_file(filename:str):
    exps = ['M8_1', 'M8_2', 'MONZ3', 'MONZ4', 'MONZ5', 'WG01', 'WG02', 'WG04']
    for i in exps:
        if i.lower() in filename.name.lower():
            return i
    raise NameError(f'Unable to ID file `{filename}`')

def all_docs(path:Path, label:str):
    data = {}
    for i in path.glob('*_d9.txt'):
        key = ID_file(i)
        data[key] = get_col(i, label)
    return data

def format_output(data:Dict[str, np.ndarray], label:str, fmt_spec:str = '.4f'):
    template = (
        '\\begin{{table}}[h]\n'
        '\t\\centering\n'
        '\t\\begin{{tabular}}{{c}}\n'
        '\t\t{} \\\\\n\t\t\\hline\n{}\n'
        '\t\\end{{tabular}}\n'
        '\t\\caption{{Caption}}\n'
        '\t\\label{{tab:sig_d_{}}}\n'
        '\\end{{table}}\n'
    )
    tables = []
    for k,v in data.items():
        rows = '\n'.join([f'\t\t{i} \\\\' for i in v])
        tables.append(template.format(label, rows, k))

    return tables

def plot_output(data:Dict[str, np.ndarray]):

    for k,v in data.items():
        plt.plot(range(v.shape[0]), v, label = k)

    plt.xlabel('Increments (Time Independent)')
    plt.ylabel('Differental Stress [MPa]')
    plt.grid()
    plt.legend()
    plt.show()

def plot_output_types(data:Dict[str, np.ndarray]):
    exps = ['M8_1', 'M8_2', 'MONZ3', 'MONZ4', 'MONZ5', 'WG01', 'WG02', 'WG04']
    shows = [1, 4, 7]

    for n,k in enumerate(exps):
        v = data[k]
        plt.plot(range(v.shape[0]), v, label = k)
        if n in shows:
            plt.xlabel('Increments (Time Independent)')
            plt.ylabel('Differental Stress [MPa]')
            plt.grid()
            plt.legend()
            plt.show()

if __name__ == '__main__':

    path = Path.home() / 'Documents' / 'MasterThesis' / 'data' / 'density_data'
    data = all_docs(path, 'sigd')
    tables = format_output(data, 'Differential Stress [MPa]')

    # plot_output(data)
    plot_output_types(data)

    # for i in tables:
    #     print(i)
