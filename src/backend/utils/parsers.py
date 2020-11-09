from typing import Union, Any, Dict
from pathlib import Path
import numpy as np
import inspect
import sys

from ..config import config

def kwarg_parser(fields, kwargs) -> Dict[Union[str, int], Any]:

    # Getting the name of the object from which this was called
    obj_name = inspect.getmodule(sys._getframe(1)).__name__
    obj_name = obj_name.split('.')[-1].capitalize()

    if kwargs == {}:
        return fields.copy()

    for key, value in kwargs.items():

        key = key.lower()

        if key not in fields.keys():
            msg = (f'\n\nAttempt to set invalid parameter \'{key}\'')
            raise SyntaxError(msg)

        elif not isinstance(value, type(fields[key])):
            msg = (f'\n\nParameter \'{key}\'> expects a(n) {type(fields[key])}'
                   f', but was given a(n) \'{type(value)}\' instead.')
            raise ValueError(msg)

    for key, value in fields.items():
        if key not in kwargs.keys():
            kwargs[key] = value

    return kwargs

def format_bytes(b:int) -> str:
    '''
        Given a value in bytes, will convert it to whatever order of magnitude
        needed for compactness (e.g. b=1024 should return `1 KB`)

        Inspired by https://stackoverflow.com/a/52379087
    '''
    step = 1024
    for prefix in ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'):
        if b < step:
            return f'{b:.0f}{prefix}'
        b /= step
    return f'{b}B'

def combine_deldensity_results(experiment:str, directory:Path = None) -> None:
    '''
        Takes results from a set of deldensity experiments saved in a folder of
        format `/combined_YYYY-MM-DD HH:MM:SS.XXXXXX`, which are by default
        saved to `~/Documents/MasterThesis/results/delden`.
    '''
    if directory is None:
        directory = config.delden_relpath

    path = directory / experiment
    temp = list(path.glob('*'))
    experiments = []
    for i in temp:
        if i.is_dir():
            experiments.append(i)

    N_experiments = len(experiments)

    avg_R2_train = np.zeros(N_experiments, dtype = np.float64)
    avg_R2_test = np.zeros(N_experiments, dtype = np.float64)
    avg_rmse_train = np.zeros(N_experiments, dtype = np.float64)
    avg_rmse_test = np.zeros(N_experiments, dtype = np.float64)

    std_R2_train = np.zeros(N_experiments, dtype = np.float64)
    std_R2_test = np.zeros(N_experiments, dtype = np.float64)
    std_rmse_train = np.zeros(N_experiments, dtype = np.float64)
    std_rmse_test = np.zeros(N_experiments, dtype = np.float64)

    for n,i in enumerate(experiments):

        R2_train = []
        R2_test = []
        rmse_train = []
        rmse_test = []
        with open(i / 'scores.csv', 'r') as infile:
            for line in infile:
                scores = list(map(float, line.split(',')))
                R2_train.append(scores[0])
                R2_test.append(scores[1])
                rmse_train.append(scores[2])
                rmse_test.append(scores[3])

        avg_R2_train[n] = np.mean(R2_train)
        avg_R2_test[n] = np.mean(R2_test)
        avg_rmse_train[n] = np.mean(rmse_train)
        avg_rmse_test[n] = np.mean(rmse_test)

        std_R2_train[n] = np.std(R2_train)
        std_R2_test[n] = np.std(R2_test)
        std_rmse_train[n] = np.std(rmse_train)
        std_rmse_test[n] = np.std(rmse_test)

    scores = np.zeros((N_experiments, 8))
    for i in range(N_experiments):
        scores[i] = np.array([
            avg_R2_train[i], avg_R2_test[i], avg_rmse_train[i],
            avg_rmse_test[i], std_R2_train[i], std_R2_test[i],
            std_rmse_train[i], std_rmse_test[i]
        ])

    filename = 'scores.csv'
    out = ''
    for n,row in enumerate(scores):
        out += f'{experiments[n].name},'
        for i in row:
            out += f'{i:f},'
        out = out[:-1] + '\n'
    out = out[:-1]
    with open(path / filename, 'w+') as outfile:
        outfile.write(out)

def combine_delvol_results(experiment:str, directory:Path = None) -> None:
    '''
        Takes results from a set of delvol experiments saved in a folder of
        format `/combined_YYYY-MM-DD HH:MM:SS.XXXXXX`, which are by default
        saved to `~/Documents/MasterThesis/results/delvol`.
    '''
    if directory is None:
        directory = config.delvol_relpath

    path = directory / experiment
    temp = list(path.glob('*'))
    experiments = []
    for i in temp:
        if i.is_dir():
            experiments.append(i)

    N_experiments = len(experiments)

    avg_R2_train = np.zeros(N_experiments, dtype = np.float64)
    avg_R2_test = np.zeros(N_experiments, dtype = np.float64)
    avg_rmse_train = np.zeros(N_experiments, dtype = np.float64)
    avg_rmse_test = np.zeros(N_experiments, dtype = np.float64)

    std_R2_train = np.zeros(N_experiments, dtype = np.float64)
    std_R2_test = np.zeros(N_experiments, dtype = np.float64)
    std_rmse_train = np.zeros(N_experiments, dtype = np.float64)
    std_rmse_test = np.zeros(N_experiments, dtype = np.float64)

    for n,i in enumerate(experiments):

        R2_train = []
        R2_test = []
        rmse_train = []
        rmse_test = []
        with open(i / 'scores.csv', 'r') as infile:
            for line in infile:
                scores = list(map(float, line.split(',')))
                R2_train.append(scores[0])
                R2_test.append(scores[1])
                rmse_train.append(scores[2])
                rmse_test.append(scores[3])

        avg_R2_train[n] = np.mean(R2_train)
        avg_R2_test[n] = np.mean(R2_test)
        avg_rmse_train[n] = np.mean(rmse_train)
        avg_rmse_test[n] = np.mean(rmse_test)

        std_R2_train[n] = np.std(R2_train)
        std_R2_test[n] = np.std(R2_test)
        std_rmse_train[n] = np.std(rmse_train)
        std_rmse_test[n] = np.std(rmse_test)

    scores = np.zeros((N_experiments, 8))
    for i in range(N_experiments):
        scores[i] = np.array([
            avg_R2_train[i], avg_R2_test[i], avg_rmse_train[i],
            avg_rmse_test[i], std_R2_train[i], std_R2_test[i],
            std_rmse_train[i], std_rmse_test[i]
        ])

    filename = 'scores.csv'
    out = ''
    for n,row in enumerate(scores):
        out += f'{experiments[n].name},'
        for i in row:
            out += f'{i:f},'
        out = out[:-1] + '\n'
    out = out[:-1]
    with open(path / filename, 'w+') as outfile:
        outfile.write(out)
