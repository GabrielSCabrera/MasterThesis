from pathlib import Path
from typing import List
import numpy as np
import argparse
import datetime
import readline
import time
import sys
import os
import re

print('\033[m')
from src import *

globals()['status_entries'] = []

def parse_args():

    argparse_desc = (
        'Runs various aspects of the rock fracture analysis depending on the '
        'sequence of included command-line arguments.'
    )
    help_split = (
        'Splits and saves the dataset into four arrays: X_train, X_test, '
        'y_train, y_test.'
    )
    help_train_DNN = (
        'Create and train a model based on a previously split and saved '
        'dataset.'
    )
    help_score_DNN = (
        'Load a previously saved model and split dataset and print the training'
        ' and testing accuracy.'
    )
    help_cluster = (
        'Load a previously saved model and split dataset and print the training'
        ' and testing accuracy.'
    )
    help_delden = (
        'Perform analyses on the given experiments using density data.'
    )
    help_delden_all = (
        'Perform analyses on the all experiments using density data.'
    )
    help_delden_all_log = (
        'Perform analyses on the all experiments using density data.  '
        'Begins by taking the logarithm of all values.'
    )
    help_delden_groups = (
        'Perform analyses on the all experiments using density data, combining '
        'experiments containing identical rock types.'
    )
    help_delden_groups_log = (
        'Perform analyses on the all experiments using density data, combining '
        'experiments containing identical rock types.  '
        'Begins by taking the logarithm of all values.'
    )
    help_delden_compare = (
        'Compares two different sets of calculations and plots their results.'
    )
    help_delvol_all = (
        'Perform analyses on the all experiments using delvol data.'
    )
    help_delvol_lite = (
        'Perform analyses on the all experiments using delvol data.  For test '
        'purposes only, does not yield useful data.'
    )
    help_delvol_all_log = (
        'Perform analyses on the all experiments using delvol data.  '
        'Begins by taking the logarithm of all values.'
    )
    help_delvol_groups = (
        'Perform analyses on the all experiments using delvol data, combining '
        'experiments containing identical rock types.'
    )
    help_delvol_groups_log = (
        'Perform analyses on the all experiments using delvol data, combining '
        'experiments containing identical rock types.  '
        'Begins by taking the logarithm of all values.'
    )
    help_delvol_plots = (
        'Select a previously run experiment and create the related figures.'
    )
    help_final_plots = (
        'Creates and saves all the final plots used in the thesis.'
    )
    help_delvol_logspace_plots = (
        'Select a previously run logspace experiment and create the related '
        'figures.'
    )
    help_delvol_linspace_plots = (
        'Select a previously run logspace experiment and create the related '
        'figures.'
    )
    help_delvol_data_prep = (
        'Creates plots that are universal to the delvol dataset, meaning plots '
        'that can be created with the data provided without the need to create '
        'or evaluate a model.'
    )
    help_sync = (
        'Synchronizes the local data with the complete dataset collection, but '
        'only if the local files are of a different size than those hosted '
        'online.'
    )
    help_force_sync = (
        'Synchronizes the local data with the complete dataset collection, even'
        ' if the local files are identical to those hosted online.'
    )
    help_delden_combine = (
        'Synchronizes the local data with the complete dataset collection.'
    )
    help_delvol_combine = (
        'Synchronizes the local data with the complete dataset collection.'
    )
    help_delvol_logspace = (
        'Runs delvol for a single sample, but for many N (number of models) '
        'in order to understand the trend for the std of R².'
    )
    help_delvol_linspace = (
        'Runs delvol for a single sample, but for many N (number of models) '
        'in order to understand the trend for the std of R².'
    )
    help_stress_strain = (
        'Plots the stress vs. the strain over time per-experiment.'
    )
    help_plot_ondemand = (
        'Plots the time to failure of a selected experiment relative to '
        'a selected column label.'
    )
    help_plots_all = (
        'Plots the time to failure of all experiment relative to all column'
        ' labels.'
    )
    help_matlab = (
        'Runs a custom MATLAB script.'
    )
    help_install = (
        'Downloads data files and installs the pipenv.'
    )
    help_uninstall = (
        'Removes downloaded data files, experiments, and all processed files.'
    )
    help_custom = (
        'Custom script, set this up on-demand.'
    )

    parser = argparse.ArgumentParser(description = argparse_desc)

    parser.add_argument(
        '--unit_tests', action='store_true', help = 'Runs all unit tests'
    )
    parser.add_argument(
        '--test', action='store_true', help = 'Runs the latest test script'
    )
    parser.add_argument(
        '--split', action='store_true', help = help_split
    )
    parser.add_argument(
        '--train_DNN', action='store_true', help = help_train_DNN
    )
    parser.add_argument(
        '--score_DNN', action='store_true', help = help_score_DNN
    )
    parser.add_argument(
        '--cluster', action='store_true', help = help_cluster
    )
    parser.add_argument(
        '--delden', action='store_true', help = help_delden
    )
    parser.add_argument(
        '--delden-all', action='store_true', help = help_delden_all
    )
    parser.add_argument(
        '--delden-all-log', action='store_true', help = help_delden_all_log
    )
    parser.add_argument(
        '--delden-groups', action='store_true', help = help_delden_groups
    )
    parser.add_argument(
        '--delden-groups-log', action='store_true',
        help = help_delden_groups_log
    )
    parser.add_argument(
        '--delden-compare', action='store_true',
        help = help_delden_compare
    )
    parser.add_argument(
        '--delvol-all', action='store_true', help = help_delvol_all
    )
    parser.add_argument(
        '--delvol-lite', action='store_true', help = help_delvol_lite
    )
    parser.add_argument(
        '--delvol-all-log', action='store_true', help = help_delvol_all_log
    )
    parser.add_argument(
        '--delvol-groups', action='store_true', help = help_delvol_groups
    )
    parser.add_argument(
        '--delvol-groups-log', action='store_true',
        help = help_delvol_groups_log
    )
    parser.add_argument(
        '--delvol-plots', action='store_true', help = help_delvol_plots
    )
    parser.add_argument(
        '--final-plots', action='store_true', help = help_final_plots
    )
    parser.add_argument(
        '--delvol-logspace-plots', action='store_true',
        help = help_delvol_logspace_plots
    )
    parser.add_argument(
        '--delvol-linspace-plots', action='store_true',
        help = help_delvol_linspace_plots
    )
    parser.add_argument(
        '--delvol-data-prep', action='store_true',
        help = help_delvol_data_prep
    )
    parser.add_argument(
        '--sync', action='store_true', help = help_sync
    )
    parser.add_argument(
        '--force-sync', action='store_true', help = help_force_sync
    )
    parser.add_argument(
        '--delden-combine', action='store_true', help = help_delden_combine
    )
    parser.add_argument(
        '--delvol-combine', action='store_true', help = help_delvol_combine
    )
    parser.add_argument(
        '--delvol-logspace', action='store_true', help = help_delvol_logspace
    )
    parser.add_argument(
        '--delvol-linspace', action='store_true', help = help_delvol_linspace
    )
    parser.add_argument(
        '--stress-strain', action='store_true', help = help_stress_strain
    )
    parser.add_argument(
        '--plot-ondemand', action='store_true', help = help_plot_ondemand
    )
    parser.add_argument(
        '--plots-all', action='store_true', help = help_plots_all
    )
    parser.add_argument(
        '--matlab', action='store_true', help = help_matlab
    )
    parser.add_argument(
        '--install', action='store_true', help = help_uninstall
    )
    parser.add_argument(
        '--uninstall', action='store_true', help = help_uninstall
    )
    parser.add_argument(
        '--custom', action='store_true', help = help_custom
    )

    return parser.parse_args()

def update_status(new_entry):
    tab_len = len('Prev. Selections:') + 7
    tot_len = tab_len
    max_len = 80
    for entry in globals()['status_entries']:
        if entry == '<newline>':
            continue
        elif tot_len + len(entry) + 3 >= max_len:
            tot_len = tab_len + len(entry) + 3
        else:
            tot_len += len(entry) + 3
    if tot_len + len(new_entry) >= max_len:
        globals()['status_entries'].append('<newline>')
    globals()['status_entries'].append(new_entry)

def display_status():
    tab_len = len('Prev. Selections:') + 7
    status = format.B('Prev. Selections:') + ' '*7
    for n,entry in enumerate(globals()['status_entries']):
        if entry == '<newline>':
            status += '\n' + ' '*tab_len
        elif n == len(globals()['status_entries'])-1:
            status += f'{format.I(entry)}'
        else:
            status += f'{format.I(entry)} > '
    return status + '\n'

"""FUNCTIONS"""

def cross_ref_delvol(directory:str, path:Path = None, suppress:bool = True):
    '''
        Cross references the delvol and delden data in order to
    '''

def save_plot_delden(directory:str, path:Path = None, suppress:bool = True):
    '''
        Saves a variety of plots for the `compare` results of delden.
    '''

    if path is None:
        path = backend.config.matlab_img_relpath
    path = path / directory
    path.mkdir(exist_ok = True)

    save_name = directory + '/compare' + '.png'
    backend.select.run_matlab(
        suppress = suppress,
        script_name = 'delden_compare.m',
        variables = (
            f"directory = \'{directory}\'; save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/compare_01' + '.png'
    backend.select.run_matlab(
        suppress = suppress,
        script_name = 'delden_compare_01.m',
        variables = (
            f"directory = \'{directory}\'; save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/hist' + '.png'
    backend.select.run_matlab(
        suppress = suppress,
        script_name = 'delden_hist.m',
        variables = (
            f"directory = \'{directory}\'; save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/hist_01' + '.png'
    backend.select.run_matlab(
        suppress = suppress,
        script_name = 'delden_hist_01.m',
        variables = (
            f"directory = \'{directory}\'; save_name = \'{save_name}\';"
        )
    )

    save_name_1 = directory + '/chart_exps' + '.png'
    save_name_2 = directory + '/chart_exps' + '.pdf'
    save_name_3 = directory + '/chart_exps_log' + '.png'
    save_name_4 = directory + '/chart_exps_log' + '.pdf'
    backend.select.run_matlab(
        suppress = suppress,
        script_name = 'delden_chart_exps.m',
        variables = (
            f"directory = \'{directory}\'; "
            f"save_name_1 = \'{save_name_1}\'; "
            f"save_name_2 = \'{save_name_2}\'; "
            f"save_name_3 = \'{save_name_3}\'; "
            f"save_name_4 = \'{save_name_4}\'; "
        )
    )

    save_name_1 = directory + '/chart_exps_best' + '.png'
    save_name_2 = directory + '/chart_exps_best' + '.pdf'
    save_name_3 = directory + '/chart_exps_best_log' + '.png'
    save_name_4 = directory + '/chart_exps_best_log' + '.pdf'
    backend.select.run_matlab(
        suppress = suppress,
        script_name = 'delden_chart_exps_best.m',
        variables = (
            f"directory = \'{directory}\'; "
            f"save_name_1 = \'{save_name_1}\'; "
            f"save_name_2 = \'{save_name_2}\'; "
            f"save_name_3 = \'{save_name_3}\'; "
            f"save_name_4 = \'{save_name_4}\'; "
        )
    )

    save_name_1 = directory + '/chart_exps_worst' + '.png'
    save_name_2 = directory + '/chart_exps_worst' + '.pdf'
    save_name_3 = directory + '/chart_exps_worst_log' + '.png'
    save_name_4 = directory + '/chart_exps_worst_log' + '.pdf'
    backend.select.run_matlab(
        suppress = suppress,
        script_name = 'delden_chart_exps_worst.m',
        variables = (
            f"directory = \'{directory}\'; "
            f"save_name_1 = \'{save_name_1}\'; "
            f"save_name_2 = \'{save_name_2}\'; "
            f"save_name_3 = \'{save_name_3}\'; "
            f"save_name_4 = \'{save_name_4}\'; "
        )
    )

def save_plot_delvol_conditional(directory:str, path:Path = None, suppress:bool = True):
    scripts = [
        'delvol_importances_good_sum_norm_all.m',
    ]

    variables = []

    #################################################################
    save_name = directory + '/importances_good_sum_norm_all.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\'; "
    )

    #################################################################

    if path is None:
        path = backend.config.matlab_img_relpath
    path = path / directory
    path.mkdir(exist_ok = True)

    result = backend.select.run_matlab_set(scripts, variables, suppress)

def save_plot_delvol(directory:str, path:Path = None, suppress:bool = True):
    '''
        Saves a variety of plots for the `compare` results of delvol.
    '''

    scripts = [
        'delvol_compare.m',
        'delvol_compare_01.m',
        'delvol_hist.m',
        'delvol_hist_01.m',
        'delvol_chart_exps.m',
        'delvol_chart_exps_best.m',
        'delvol_chart_exps_worst.m',
        'delvol_compare_sample_observed.m',
        'delvol_samples_exp.m',
        'delvol_samples_exp_01.m',
        'delvol_chart_exps_best_worst_compare.m',
        'delvol_importances.m',
        'delvol_importances_compare.m',
        'delvol_importances_mean.m',
        'delvol_importances_any.m',
        'delvol_importances_weak.m',
        'delvol_importances_good.m',
        'delvol_importances_good_norm.m',
        'delvol_importances_good_sum.m',
        'delvol_importances_good_sum_norm.m',
    ]

    variables = []

    #################################################################

    save_name = directory + '/compare' + '.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\';"
    )

    #################################################################
    save_name = directory + '/compare_01' + '.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\';"
    )

    #################################################################
    save_name = directory + '/hist' + '.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\';"
    )

    #################################################################
    save_name = directory + '/hist_01' + '.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\';"
    )

    #################################################################
    save_name_1 = directory + '/chart_exps' + '.png'
    save_name_2 = directory + '/chart_exps' + '.pdf'
    save_name_3 = directory + '/chart_exps_log' + '.png'
    save_name_4 = directory + '/chart_exps_log' + '.pdf'

    variables.append(
        f"directory = \'{directory}\'; "
        f"save_name_1 = \'{save_name_1}\'; "
        f"save_name_2 = \'{save_name_2}\'; "
        f"save_name_3 = \'{save_name_3}\'; "
        f"save_name_4 = \'{save_name_4}\'; "
    )

    #################################################################
    save_name_1 = directory + '/chart_exps_best' + '.png'
    save_name_2 = directory + '/chart_exps_best' + '.pdf'
    save_name_3 = directory + '/chart_exps_best_log' + '.png'
    save_name_4 = directory + '/chart_exps_best_log' + '.pdf'

    variables.append(
        f"directory = \'{directory}\'; "
        f"save_name_1 = \'{save_name_1}\'; "
        f"save_name_2 = \'{save_name_2}\'; "
        f"save_name_3 = \'{save_name_3}\'; "
        f"save_name_4 = \'{save_name_4}\'; "
    )

    #################################################################
    save_name_1 = directory + '/chart_exps_worst' + '.png'
    save_name_2 = directory + '/chart_exps_worst' + '.pdf'
    save_name_3 = directory + '/chart_exps_worst_log' + '.png'
    save_name_4 = directory + '/chart_exps_worst_log' + '.pdf'

    variables.append(
        f"directory = \'{directory}\'; "
        f"save_name_1 = \'{save_name_1}\'; "
        f"save_name_2 = \'{save_name_2}\'; "
        f"save_name_3 = \'{save_name_3}\'; "
        f"save_name_4 = \'{save_name_4}\'; "
    )

    #################################################################
    save_name_1 = directory + '/compare_sample_observed' + '.png'
    save_name_2 = directory + '/compare_sample_observed' + '.pdf'
    variables.append(
        f"directory = \'{directory}\'; "
        f"save_name_1 = \'{save_name_1}\'; "
        f"save_name_2 = \'{save_name_2}\'; "
    )

    #################################################################
    save_name = directory + '/samples_exp' + '.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\';"
    )

    #################################################################
    save_name = directory + '/samples_exp_01' + '.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\';"
    )

    #################################################################
    save_name_1 = directory + '/chart_exps_best_worst' + '.png'
    save_name_2 = directory + '/chart_exps_best_worst' + '.pdf'
    variables.append(
        f"directory = \'{directory}\'; "
        f"save_name_1 = \'{save_name_1}\'; "
        f"save_name_2 = \'{save_name_2}\'; "
    )

    #################################################################
    save_name = directory + '/importances_'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\';"
    )

    #################################################################
    save_name = directory + '/importances_compare.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\';"
    )

    #################################################################
    save_name = directory + '/importances_mean.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\'; "
    )

    #################################################################
    save_name = directory + '/importances_any.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\'; "
    )

    #################################################################
    save_name = directory + '/importances_weak.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\'; "
    )

    #################################################################
    save_name = directory + '/importances_good.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\'; "
    )

    #################################################################
    save_name = directory + '/importances_good_norm.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\'; "
    )

    #################################################################
    save_name = directory + '/importances_good_sum.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\'; "
    )

    #################################################################
    save_name = directory + '/importances_good_sum_norm.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\'; "
    )

    #################################################################

    if path is None:
        path = backend.config.matlab_img_relpath
    path = path / directory
    path.mkdir(exist_ok = True)

    result = backend.select.run_matlab_set(scripts, variables, suppress)

    if result != 0:
        msg = (
            '\n\033[1mReverting to Running Scripts Individually (Slow)\033[m\n'
        )
        print(msg, flush = True)
        for script, var in zip(scripts, variables):
            backend.select.run_matlab(
                suppress = suppress,
                script_name = script,
                variables = var
            )

def delvol_all_custom(N_experiments:int, training_labels:List[str]):

    BucketManager.download('delvol_data')
    terminal.reset_screen()

    exps = backend.groups.delvol_exps['all']

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    for label in training_labels:
        terminal.reset_screen()
        directory = label
        path = backend.config.delvol_relpath / directory
        path.mkdir(exist_ok = True)
        length = len(exps)
        for n,i in enumerate(exps):
            title = backend.utils.format.B(f'EXPERIMENT {i} ')
            title += backend.utils.format.I(f'({n+1}/{length})')
            delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
            delvol.set_experiments(i)
            delvol.set_training_label(label)
            delvol.grid_search(
                itermax = N_experiments, train_size = 0.75, **gridsearch_params
            )
            delvol.save(filename = i)

        parsers.combine_delvol_results(path)
        save_plot_delvol(directory)

def delvol_logspace_plot(directory:str, path:Path = None, suppress:bool = True):
    '''
        Creates plots showing the trend of the mean and std of R² for differing
        numbers of models.
    '''
    scripts = [
        'delvol_logspace_bars.m',
        'delvol_logspace_line.m',
    ]

    variables = []

    #################################################################
    save_name = directory + '/logspace_bars.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\'; "
    )
    #################################################################
    save_name_1 = directory + '/logspace_mean_lines.png'
    save_name_2 = directory + '/logspace_std_lines.png'
    variables.append(
        f"directory = \'{directory}\'; save_name_1 = \'{save_name_1}\'; "
        f"save_name_2 = \'{save_name_2}\'; "
    )
    #################################################################

    if path is None:
        path = backend.config.matlab_img_relpath
    path = path / directory
    path.mkdir(exist_ok = True)

    result = backend.select.run_matlab_set(scripts, variables, suppress)

    if result != 0:
        msg = (
            '\n\033[1mReverting to Running Scripts Individually (Slow)\033[m\n'
        )
        print(msg, flush = True)
        for script, var in zip(scripts, variables):
            backend.select.run_matlab(
                suppress = suppress,
                script_name = script,
                variables = var
            )

def delvol_linspace_plot(directory:str, path:Path = None, suppress:bool = True):
    '''
        Creates plots showing the trend of the mean and std of R² for differing
        numbers of models.
    '''
    scripts = [
        'delvol_linspace_bars.m',
        'delvol_linspace_line.m',
    ]

    variables = []

    #################################################################
    save_name = directory + '/linspace_bars.png'
    variables.append(
        f"directory = \'{directory}\'; save_name = \'{save_name}\'; "
    )
    #################################################################
    save_name_1 = directory + '/linspace_mean_lines.png'
    save_name_2 = directory + '/linspace_std_lines.png'
    variables.append(
        f"directory = \'{directory}\'; save_name_1 = \'{save_name_1}\'; "
        f"save_name_2 = \'{save_name_2}\'; "
    )
    #################################################################

    if path is None:
        path = backend.config.matlab_img_relpath
    path = path / directory
    path.mkdir(exist_ok = True)

    result = backend.select.run_matlab_set(scripts, variables, suppress)

    if result != 0:
        msg = (
            '\n\033[1mReverting to Running Scripts Individually (Slow)\033[m\n'
        )
        print(msg, flush = True)
        for script, var in zip(scripts, variables):
            backend.select.run_matlab(
                suppress = suppress,
                script_name = script,
                variables = var
            )

"""SCRIPT PROCEDURES"""

def procedure_split():

    terminal.reset_screen()

    choices = config.labels
    label = select.select('Choose a Dataset', choices)
    dataset = config.bins[label]
    dims = dataset.dims
    split_dataset = None

    update_status(label)

    while True:
        terminal.reset_screen()
        print(display_status())
        savename = select.select_str('Save As')
        if not savename.strip():
            continue
        if '.npz' not in savename:
            savename += '.npz'
        sel = select.confirm_overwrite(savename, config.split_bins_relpath,
                                       '.npz')
        if sel is True:
            break

    terminal.reset_screen()
    update_status(f'Save As \'{savename}\'')
    print(display_status())

    test_size = select.select_float('Test Size', [0.05, 0.9])

    terminal.reset_screen()
    update_status(f'Train {100*(1-test_size):g}% & Test {100*(test_size):g}%')
    print(display_status())

    selection = select.select('Splitting Options', ['2-D', '3-D'])

    terminal.reset_screen()
    update_status(selection)
    print(display_status())

    shuffle = not select.select_bool('Split by Region?')

    terminal.reset_screen()
    if shuffle is True:
        update_status('Random')
    else:
        update_status('Split')
    print(display_status())

    rem_zeros = select.select_bool('Remove Arrays Containing All Zeros?')
    if rem_zeros is True:
        update_status(f'Removing Zero-Arrays')
    else:
        update_status(f'Keeping Zero-Arrays')

    terminal.reset_screen()
    print(display_status())

    if selection == '2-D':

        options = ['Columns (Vertical)', 'Slices (Horizontal)']
        selection = select.select('2-D Shape Options', options)

        terminal.reset_screen()
        update_status(selection)
        print(display_status())

        if selection == options[0]:

            min_cols = 2
            min_size = min(min_cols/(dims[0]), 1)

            limit = select.select_float('Dataset Size', [min_size, 1])

            terminal.reset_screen()
            update_status(f'{limit*100:g}% of Data')
            print(display_status())

            max_cols = int(limit*dims[0]//4)
            N_cols = select.select_int('Select Number of Columns p/ 2-D Slice',
                                        [min_cols, max_cols])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_cols,
                        'mode'        :   'col',
                        'test_size'   :   test_size,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_2D.test_train_split(**params)

        elif selection == options[1]:

            min_slices = 2

            min_size = min(min_slices/(dims[2]), 1)

            limit = select.select_float('Dataset Size', [min_size, 1])

            terminal.reset_screen()
            update_status(f'{limit*100:g}% of Data')
            print(display_status())

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   None,
                        'mode'        :   'slice',
                        'test_size'   :   test_size,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_2D.test_train_split(**params)

    elif selection == '3-D':

        options = ['Columns (Vertical)', 'Slabs (Horizontal)', 'Cubes']
        selection = select.select('3-D Shape Options', options)

        terminal.reset_screen()
        update_status(selection)
        print(display_status())

        if selection == options[0]:

            min_cols = 4

            min_size = min(min_cols**2/(min(dims[:2])**2), 1)

            limit = select.select_float('Dataset Size', [min_size, 1])

            terminal.reset_screen()
            update_status(f'{limit*100:g}% of Data')
            print(display_status())

            max_cols = int(limit*dims[0]*dims[1]//4)
            N_cols = select.select_int('Select Approx. Number of Columns',
                                         [min_cols, max_cols])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_cols,
                        'mode'        :   'col',
                        'test_size'   :   test_size,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_3D.test_train_split(**params)

        elif selection == options[1]:

            min_slabs = 4

            min_size = min(min_slabs/dims[2], 1)

            limit = select.select_float('Dataset Size', [min_size, 1])

            terminal.reset_screen()
            update_status(f'{limit*100:g}% of Data')
            print(display_status())

            max_slabs = int(limit*dims[2]//2)
            N_slices = select.select_int('Select Approx. Number of Slabs',
                                            [min_slabs, max_slabs])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_slices,
                        'mode'        :   'slice',
                        'test_size'   :   test_size,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_3D.test_train_split(**params)

        elif selection == options[2]:

            min_cubes = 8

            min_size = min(min_cubes**2/(min(dims)**3), 1)

            limit = select.select_float('Dataset Size', [min_size, 1])

            terminal.reset_screen()
            update_status(f'{limit*100:g}% of Data')
            print(display_status())

            max_cubes = int(limit*min(dims)**3//8)
            N_cubes = select.select_int('Select Approx. Number of Cubes',
                                          [min_cubes, max_cubes])

            params = {
                        'dataset'     :   dataset,
                        'splits'      :   N_cubes,
                        'mode'        :   'cube',
                        'test_size'   :   test_size,
                        'limit'       :   limit,
                        'shuffle'     :   shuffle
                     }

            split_dataset = split_3D.test_train_split(**params)

    if split_dataset is None:
        raise Exception('Unexpected Error')

    X_train, X_test, y_train, y_test = split_dataset

    if rem_zeros is True:
        X_train, X_test, y_train, y_test =\
        filter.remove_empty(X_train, X_test, y_train, y_test)

    print(format.B('Saving Segments'))
    file_io.save_split(savename, X_train, X_test, y_train, y_test)
    print(format.B('Saved to ') + format.I(config.split_bins_relpath / savename))

def procedure_train_DNN():

    BucketManager.download('bins')
    backend.binfo.Binfo.load_data()

    terminal.reset_screen()

    files = file_io.list_files(config.split_bins_relpath, '.npz')

    if not files:
        msg = (f'{format.B("No Split-Data Files to Load")}\n'
               f'Run script with flag {format.I("--split")} to split a dataset '
               f'into {format.I("training")} and {format.I("testing")} sets, '
               'and save the results.')
        print(msg)
        exit()

    split_file = select.scroll_select('Select a File for Training',
                                      list(files.keys()))

    update_status(f'Load \'{split_file}\'')

    while True:
        terminal.reset_screen()
        print(display_status())
        savename = select.select_str('Save Model As')
        if not savename.strip():
            continue
        if config.DNN_model_extension not in savename:
            savename += config.DNN_model_extension
        sel = select.confirm_overwrite(savename, config.DNN_models_relpath,
                                       config.DNN_model_extension)
        if sel is True:
            break

    terminal.reset_screen()
    update_status(f'Save As \'{savename}\'')
    print(display_status())

    X_train, X_test, y_train, y_test =\
    file_io.load_split(label = split_file)

    X_train, X_test, y_train, y_test =\
    reshape.reshape_1D(X_train, X_test, y_train, y_test)

    layers = select.select_int_list('Select a Layer Configuration')

    terminal.reset_screen()
    update_status(f'Layer Config {layers}')
    print(display_status())

    model = DNN.Model(hidden_layer_sizes = tuple(layers), verbose = True)

    model.fit(X_train, y_train)

    model.save(savename)

    score_DNN(model, X_train, X_test, y_train, y_test)

def procedure_score_DNN():

    BucketManager.download('bins')
    backend.binfo.Binfo.load_data()
    terminal.reset_screen()

    files = file_io.list_files(config.split_bins_relpath, '.npz')

    if not files:
        msg = (f'{format.B("No Split-Data Files to Load")}\n'
               f'Run script with flag {format.I("--split")} to split a dataset '
               f'into {format.I("training")} and {format.I("testing")} sets, '
               'and save the results.')
        print(msg)
        exit()

    split_file = select.scroll_select('Select a File for Training',
                                      list(files.keys()))

    update_status(f'Load Split Data \'{split_file}\'')

    terminal.reset_screen()
    print(display_status())

    files = file_io.list_files(config.DNN_models_relpath, '.dnn')

    if not files:
        msg = (f'{format.B("No Model Files to Load")}\n'
               f'Run script with flag {format.I("--train_DNN")} to train a '
               f'model and save it to file.')
        print(msg)
        exit()

    model_file = select.scroll_select('Select a Model to Load',
                                      list(files.keys()))

    update_status(f'Load Model \'{model_file}\'')

    X_train, X_test, y_train, y_test =\
    file_io.load_split(label = split_file)

    X_train, X_test, y_train, y_test =\
    reshape.reshape_1D(X_train, X_test, y_train, y_test)

    terminal.reset_screen()
    print(display_status())

    model = DNN.load(model_file)
    score = score_DNN(model, X_train, X_test, y_train, y_test)

def score_DNN(model, X_train, X_test, y_train, y_test):

    terminal.reset_screen()
    print(display_status())

    print(format.B("Checking Accuracy"))

    train_score = str(model.score(X_train, y_train))
    test_score = str(model.score(X_test, y_test))

    print(f'Training Set Score: ' + format.I(train_score))
    print(f'Testing Set Score:  ' + format.I(test_score))

def procedure_cluster():

    terminal.reset_screen()
    BucketManager.download('bins')
    backend.binfo.Binfo.load_data()
    terminal.reset_screen()

    choices = config.labels
    label = select.select('Choose a Dataset', choices)
    dataset = config.bins[label]
    dims = dataset.dims
    split_dataset = None

    update_status(label)

    while True:
        terminal.reset_screen()
        print(display_status())
        savename = select.select_str('Save As')
        if not savename.strip():
            continue
        sel = select.confirm_overwrite(savename, config.clusters_relpath)
        if sel is True:
            break

    terminal.reset_screen()
    update_status(f'Save As \'{savename}\'')
    print(display_status())

    min_cluster_size = select.select_int('Minimum Cluster Size', [1, 1000])

    terminal.reset_screen()
    update_status(f'Min. Cluster Size {min_cluster_size}')
    print(display_status())

    print(format.B('Performing Extraction\n'))
    clusters.extract_clusters(dataset, savename, min_cluster_size)
    print(format.B('Saved to ') + format.I(config.clusters_relpath / savename))

def procedure_delden():

    BucketManager.download('density_data')
    terminal.reset_screen()

    title = 'How many experiments to run?'
    val_range = [0, 100]
    N_experiments = select.select_int(title, val_range)

    terminal.reset_screen()

    delden = DelDensity.DelDensity()
    delden.grid_search(itermax = 16)
    delden.save()

def procedure_delden_all():

    BucketManager.download('density_data')
    terminal.reset_screen()

    title = 'How many experiments to run?'
    val_range = [0, 100]
    N_experiments = select.select_int(title, val_range)
    exps = backend.groups.delden_exps['all']

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    terminal.reset_screen()

    directory = backend.utils.select.create_unique_name(prefix = 'combined')
    path = backend.config.delden_relpath / directory
    path.mkdir(exist_ok = True)
    length = len(exps)
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENT {i} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delden = DelDensity.DelDensity(save_dir = path, title = title)
        delden.set_experiments(i)
        delden.grid_search(
            itermax = N_experiments, train_size = 0.75,
            **gridsearch_params
        )
        delden.save(filename = i)

    parsers.combine_delden_results(path)
    save_plot_delden(directory)

def procedure_delden_all_log():

    BucketManager.download('density_data')
    terminal.reset_screen()

    title = 'How many experiments to run?'
    val_range = [0, 100]
    N_experiments = select.select_int(title, val_range)
    exps = backend.groups.delden_exps['all']

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    terminal.reset_screen()

    directory = backend.utils.select.create_unique_name(prefix = 'combined')
    path = backend.config.delden_relpath / directory
    path.mkdir(exist_ok = True)
    length = len(exps)
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENT {i} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delden = DelDensity.DelDensity(save_dir = path, title = title)
        delden.set_experiments(i)
        delden.grid_search(
            itermax = N_experiments, train_size = 0.75, log = True,
            **gridsearch_params
        )
        delden.save(filename = i)

    parsers.combine_delden_results(path)
    save_plot_delden(directory)

def procedure_delden_groups():

    BucketManager.download('density_data')
    terminal.reset_screen()

    title = 'How many experiments to run?'
    val_range = [0, 100]
    N_experiments = select.select_int(title, val_range)
    opts = backend.groups.delden_exps
    exps = [opts['WG'], opts['M8'], opts['MONZ']]

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    terminal.reset_screen()

    directory = backend.utils.select.create_unique_name(prefix = 'combined')
    path = backend.config.delden_relpath / directory
    path.mkdir(exist_ok = True)
    length = len(exps)
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENTS {", ".join(i)} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delden = DelDensity.DelDensity(save_dir = path, title = title)
        delden.set_experiments(*i)
        delden.grid_search(
            itermax = N_experiments, train_size = 0.75,
            **gridsearch_params
        )
        delden.save(filename = '-'.join(i))

    parsers.combine_delden_results(path)
    save_plot_delden(directory)

def procedure_delden_groups_log():

    BucketManager.download('density_data')
    terminal.reset_screen()

    title = 'How many experiments to run?'
    val_range = [0, 100]
    N_experiments = select.select_int(title, val_range)
    opts = backend.groups.delden_exps
    exps = [opts['WG'], opts['M8'], opts['MONZ']]

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    terminal.reset_screen()

    directory = backend.utils.select.create_unique_name(prefix = 'combined')
    path = backend.config.delden_relpath / directory
    path.mkdir(exist_ok = True)
    length = len(exps)
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENTS {", ".join(i)} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delden = DelDensity.DelDensity(save_dir = path, title = title)
        delden.set_experiments(*i)
        delden.grid_search(
            itermax = N_experiments, train_size = 0.75, log = True,
            **gridsearch_params
        )
        delden.save(filename = '-'.join(i))

    parsers.combine_delden_results(path)
    save_plot_delden(directory)

def procedure_delden_compare():

    terminal.reset_screen()
    directory_1 = 'All_2'
    directory_2 = 'All_Log_2'
    directory = f'compare_{directory_1}_{directory_2}'
    path = backend.config.matlab_img_relpath
    path = path / directory
    path.mkdir(exist_ok = True)

    save_name = directory + '/compare' + '.png'
    backend.select.run_matlab(
        script_name = 'delden_log_compare.m',
        variables = (
            f"directory_1 = \'{directory_1}\'; directory_2 = \'{directory_2}\';"
            f" save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/compare_01' + '.png'
    backend.select.run_matlab(
        script_name = 'delden_log_compare_01.m',
        variables = (
            f"directory_1 = \'{directory_1}\'; directory_2 = \'{directory_2}\';"
            f" save_name = \'{save_name}\';"
        )
    )

def procedure_delvol_compare():

    terminal.reset_screen()
    directory_1 = 'All_2'
    directory_2 = 'All_Log_2'
    directory = f'compare_{directory_1}_{directory_2}'
    path = backend.config.matlab_img_relpath
    path = path / directory
    path.mkdir(exist_ok = True)

    save_name = directory + '/compare' + '.png'
    backend.select.run_matlab(
        script_name = 'delvol_compare.m',
        variables = (
            f"directory_1 = \'{directory_1}\'; directory_2 = \'{directory_2}\';"
            f" save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/compare_01' + '.png'
    backend.select.run_matlab(
        script_name = 'delvol_compare_01.m',
        variables = (
            f"directory_1 = \'{directory_1}\'; directory_2 = \'{directory_2}\';"
            f" save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/log_compare' + '.png'
    backend.select.run_matlab(
        script_name = 'delvol_log_compare.m',
        variables = (
            f"directory_1 = \'{directory_1}\'; directory_2 = \'{directory_2}\';"
            f" save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/log_compare_01' + '.png'
    backend.select.run_matlab(
        script_name = 'delvol_log_compare_01.m',
        variables = (
            f"directory_1 = \'{directory_1}\'; directory_2 = \'{directory_2}\';"
            f" save_name = \'{save_name}\';"
        )
    )

def procedure_delvol_all():

    BucketManager.download('delvol_data')
    terminal.reset_screen()

    training_label = 'sig_d'
    # training_label = 'delvtot'
    title = 'How many experiments to run?'
    val_range = [0, 100]
    N_experiments = select.select_int(title, val_range)
    exps = backend.groups.delvol_exps['all']

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    terminal.reset_screen()

    directory = backend.utils.select.create_unique_name(prefix = 'combined')
    path = backend.config.delvol_relpath / directory
    path.mkdir(exist_ok = True)
    length = len(exps)
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENT {i} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
        delvol.set_experiments(i)
        delvol.set_training_label(training_label)
        delvol.grid_search(
            itermax = N_experiments, train_size = 0.75, **gridsearch_params
        )
        delvol.save(filename = i)

    parsers.combine_delvol_results(path)
    save_plot_delvol(directory)

def procedure_delvol_lite():

    BucketManager.download('delvol_data')
    terminal.reset_screen()

    N_experiments = 15
    exps = backend.groups.delvol_exps['all']

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.9],
        "alpha":            [0.001],
        "learning_rate":    [0.005],
        "n_estimators":     [10,],
        "max_depth":        [3, 5]
    }

    terminal.reset_screen()

    directory = 'lite_test'
    path = backend.config.delvol_relpath / directory
    path.mkdir(exist_ok = True)
    length = len(exps)
    training_label = 'delv50'
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENT {i} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
        delvol.set_experiments(i)
        delvol.set_training_label(training_label)
        delvol.grid_search(
            itermax = N_experiments, train_size = 0.75, **gridsearch_params
        )
        delvol.save(filename = i)

    parsers.combine_delvol_results(path)
    save_plot_delvol(directory)

def procedure_delvol_all_log():

    BucketManager.download('density_data')
    terminal.reset_screen()

    title = 'How many experiments to run?'
    val_range = [0, 100]
    N_experiments = select.select_int(title, val_range)
    exps = backend.groups.delvol_exps['all']

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    terminal.reset_screen()

    directory = backend.utils.select.create_unique_name(prefix = 'combined')
    path = backend.config.delvol_relpath / directory
    path.mkdir(exist_ok = True)
    length = len(exps)
    training_label = 'delv50'
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENT {i} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
        delvol.set_experiments(i)
        delvol.set_training_label(training_label)
        delvol.grid_search(
            itermax = N_experiments, train_size = 0.75, log = True,
            **gridsearch_params
        )
        delvol.save(filename = i)

    parsers.combine_delvol_results(path)
    save_plot_delvol(directory)

def procedure_delvol_groups():

    BucketManager.download('delvol_data')
    terminal.reset_screen()

    title = 'How many experiments to run?'
    val_range = [0, 100]
    N_experiments = select.select_int(title, val_range)
    opts = backend.groups.delvol_exps
    exps = [opts['WG'], opts['M8'], opts['MONZ']]

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    terminal.reset_screen()

    directory = backend.utils.select.create_unique_name(prefix = 'combined')
    path = backend.config.delvol_relpath / directory
    path.mkdir(exist_ok = True)
    length = len(exps)
    training_label = 'delv50'
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENTS {", ".join(i)} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
        delvol.set_experiments(*i)
        delvol.set_training_label(training_label)
        delvol.grid_search(
            itermax = N_experiments, train_size = 0.75,
            **gridsearch_params
        )
        delvol.save(filename = '-'.join(i))

    parsers.combine_delvol_results(path)
    save_plot_delvol(directory)

def procedure_delvol_groups_log():

    BucketManager.download('density_data')
    terminal.reset_screen()

    title = 'How many experiments to run?'
    val_range = [0, 100]
    N_experiments = select.select_int(title, val_range)
    opts = backend.groups.delvol_exps
    exps = [opts['WG'], opts['M8'], opts['MONZ']]

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    terminal.reset_screen()

    directory = backend.utils.select.create_unique_name(prefix = 'combined')
    path = backend.config.delvol_relpath / directory
    path.mkdir(exist_ok = True)
    length = len(exps)
    training_label = 'delvtot'
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENTS {", ".join(i)} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
        delvol.set_experiments(*i)
        delvol.set_training_label(training_label)
        delvol.grid_search(
            itermax = N_experiments, train_size = 0.75, log = True,
            **gridsearch_params
        )
        delvol.save(filename = '-'.join(i))

    parsers.combine_delvol_results(path)
    save_plot_delvol(directory)

def procedure_delvol_plots():
    title = (
        f'Select a Set of Results.'
    )
    path = backend.config.delvol_relpath
    options = [str(i.name) for i in path.glob('*')]
    selection = select.scroll_select(title, options)
    terminal.reset_screen()
    # save_plot_delvol(selection, suppress = False)
    save_plot_delvol_conditional(selection, suppress = False)

def procedure_final_plots():
    '''
        Expects the existence of multiple directories!
    '''

    scripts = [
        'delvol_compare.m',
        'delvol_compare.m',
        'delvol_compare_01.m',
        'delvol_compare_01.m',
        'delvol_importances_good_norm.m',
        'delvol_importances_good_norm.m',
        'delvol_importances_good_norm.m',
        'delvol_importances_good_sum_norm_all.m',
        'delvol_importances_good_sum_norm_all.m',
        'delvol_stress_strain_all.m',
        'delvol_linspace_bars.m',
        'delvol_linspace_bars.m',
        'delvol_plot_prepped_avg.m',
        'delvol_plot_prepped_avg.m',
        'delvol_plot_prepped_avg.m',
        'delvol_plot_prepped_avg.m',
        'delvol_plot_prepped_avg.m',
        'delvol_plot_prepped_avg_means.m',
        'delvol_plot_prepped_avg_means.m',
        'delvol_plot_prepped_avg_means.m',
        'delvol_plot_prepped_avg_means.m',
        'delvol_plot_prepped_avg_means.m',
    ]

    variables = []

    directory = 'final_plots'
    suppress = False

    #################################################################
    save_name = directory + '/compare_delvtot' + '.png'
    variables.append(
        f"directory = 'delvtot_all'; save_name = \'{save_name}\';"
    )
    #################################################################
    save_name = directory + '/compare_sigd' + '.png'
    variables.append(
        f"directory = 'sigd_all'; save_name = \'{save_name}\';"
    )
    #################################################################
    save_name = directory + '/compare_delvtot_01' + '.png'
    variables.append(
        f"directory = 'delvtot_all'; save_name = \'{save_name}\';"
    )
    #################################################################
    save_name = directory + '/compare_sigd_01' + '.png'
    variables.append(
        f"directory = 'sigd_all'; save_name = \'{save_name}\';"
    )
    #################################################################
    # save_name = directory + '/importances_delvtot_'
    # variables.append(
    #     f"directory = 'delvtot_all'; save_name = \'{save_name}\';"
    # )
    # #################################################################
    # save_name = directory + '/importances_sigd_'
    # variables.append(
    #     f"directory = 'sigd_all'; save_name = \'{save_name}\';"
    # )
    #################################################################
    save_name = directory + '/importances_good_norm_marble.png'
    variables.append(
        f"directory = 'delvtot_marble'; save_name = \'{save_name}\'; "
    )
    #################################################################
    save_name = directory + '/importances_good_norm_monzanite.png'
    variables.append(
        f"directory = 'delvtot_monzonite'; save_name = \'{save_name}\'; "
    )
    #################################################################
    save_name = directory + '/importances_good_norm_granite.png'
    variables.append(
        f"directory = 'delvtot_granite'; save_name = \'{save_name}\'; "
    )
    #################################################################
    save_name = directory + '/importances_good_sum_norm_all_delvtot.png'
    variables.append(
        f"directory = 'delvtot_all'; save_name = \'{save_name}\'; "
    )
    #################################################################
    save_name = directory + '/importances_good_sum_norm_all_sigd.png'
    variables.append(
        f"directory = 'sigd_all'; save_name = \'{save_name}\'; "
    )
    #################################################################
    # files_list = [
    #     'times_M8_1.mat',
    #     'times_M8_2.mat',
    #     'times_MONZ3.mat',
    #     'times_MONZ4.mat',
    #     'times_MONZ5.mat',
    #     'times_WG01.mat',
    #     'times_WG02.mat',
    #     'times_WG04.mat',
    # ]
    # exps = [
    #     'M8_1',
    #     'M8_2',
    #     'MONZ3',
    #     'MONZ4',
    #     'MONZ5',
    #     'WG01',
    #     'WG02',
    #     'WG04',
    # ]
    #
    # for i,j in zip(files_list, exps):
    #     save_name = directory + f'/{j}_stress_strain.png'
    #     variables.append(
    #         f"filename = '{i}'; save_name = \'{save_name}\';"
    #     )
    #################################################################
    save_name = directory + f'/stress_strain_all.png'
    variables.append(
        f"save_name = \'{save_name}\';"
    )
    #################################################################
    save_name = directory + '/linspace_bars_MONZ3.png'
    variables.append(
        f"directory = 'linspace_MONZ3_delvtot'; save_name = \'{save_name}\'; "
    )
    #################################################################
    save_name = directory + '/linspace_bars_WG01.png'
    variables.append(
        f"directory = 'linspace_WG01_delvtot'; save_name = \'{save_name}\'; "
    )
    #################################################################


    #################################################################
    save_name = directory + '/WG01_vol_50.png'
    variables.append(
        f"filename = 'WG01_vol_50_avg.csv'; save_name = \'{save_name}\'; "
        f"label = '50ᵗʰ Percentile of Individual Fracture Volume';"
    )
    #################################################################
    save_name = directory + '/WG01_ani_50.png'
    variables.append(
        f"filename = 'WG01_ani_50_avg.csv'; save_name = \'{save_name}\'; "
        f"label = '50ᵗʰ Percentile of Shape Anisotropy';"
    )
    #################################################################
    save_name = directory + '/WG01_l1_50.png'
    variables.append(
        f"filename = 'WG01_l1_50_avg.csv'; save_name = \'{save_name}\'; "
        f"label = '50ᵗʰ Percentile Min. Eigenvalue, Fracture Aperture';"
    )
    #################################################################
    save_name = directory + '/WG01_l3_50.png'
    variables.append(
        f"filename = 'WG01_l3_50_avg.csv'; save_name = \'{save_name}\'; "
        f"label = '50ᵗʰ Percentile Max. Eigenvalue, Fracture Aperture';"
    )
    #################################################################
    save_name = directory + '/WG01_th1_50.png'
    variables.append(
        f"filename = 'WG01_th1_50_avg.csv'; save_name = \'{save_name}\'; "
        f"label = '50ᵗʰ Percentile Orientiation of Min. Eigenvector';"
    )
    #################################################################


    #################################################################
    save_name = directory + '/WG01_vol_50_mean.png'
    variables.append(
        f"filename = 'WG01_vol_50_avg.csv'; save_name = \'{save_name}\'; "
        f"label = '50ᵗʰ Percentile of Individual Fracture Volume';"
    )
    #################################################################
    save_name = directory + '/WG01_ani_50_mean.png'
    variables.append(
        f"filename = 'WG01_ani_50_avg.csv'; save_name = \'{save_name}\'; "
        f"label = '50ᵗʰ Percentile of Shape Anisotropy';"
    )
    #################################################################
    save_name = directory + '/WG01_l1_50_mean.png'
    variables.append(
        f"filename = 'WG01_l1_50_avg.csv'; save_name = \'{save_name}\'; "
        f"label = '50ᵗʰ Percentile Min. Eigenvalue, Fracture Aperture';"
    )
    #################################################################
    save_name = directory + '/WG01_l3_50_mean.png'
    variables.append(
        f"filename = 'WG01_l3_50_avg.csv'; save_name = \'{save_name}\'; "
        f"label = '50ᵗʰ Percentile Max. Eigenvalue, Fracture Aperture';"
    )
    #################################################################
    save_name = directory + '/WG01_th1_50_mean.png'
    variables.append(
        f"filename = 'WG01_th1_50_avg.csv'; save_name = \'{save_name}\'; "
        f"label = '50ᵗʰ Percentile Orientiation of Min. Eigenvector';"
    )
    #################################################################
    path = backend.config.matlab_img_relpath
    path = path / directory
    path.mkdir(exist_ok = True)

    result = backend.select.run_matlab_set(scripts, variables, suppress)

    if result != 0:
        msg = (
            '\n\033[1mReverting to Running Scripts Individually (Slow)\033[m\n'
        )
        print(msg, flush = True)
        for script, var in zip(scripts, variables):
            backend.select.run_matlab(
                suppress = suppress,
                script_name = script,
                variables = var
            )

def procedure_delvol_logspace_plots():
    title = (
        f'Select a Set of Results.'
    )
    path = backend.config.delvol_relpath
    options = sorted([str(i.name) for i in path.glob('*')])
    selection = select.scroll_select(title, options)
    terminal.reset_screen()
    delvol_logspace_plot(selection, suppress = True)

def procedure_delvol_linspace_plots():
    title = (
        f'Select a Set of Results.'
    )
    path = backend.config.delvol_relpath
    options = sorted([str(i.name) for i in path.glob('*')])
    selection = select.scroll_select(title, options)
    terminal.reset_screen()
    delvol_linspace_plot(selection, suppress = True)

def procedure_delvol_data_prep():

    from scipy import io

    files = [
        'times_M8_1.mat',
        'times_M8_2.mat',
        'times_MONZ3.mat',
        'times_MONZ4.mat',
        'times_MONZ5.mat',
        'times_WG01.mat',
        'times_WG02.mat',
        'times_WG04.mat',
    ]

    new_files = [
        'times_M8_1.npy',
        'times_M8_2.npy',
        'times_MONZ3.npy',
        'times_MONZ4.npy',
        'times_MONZ5.npy',
        'times_WG01.npy',
        'times_WG02.npy',
        'times_WG04.npy',
    ]

    for file1, file2 in zip(files, new_files):
        path1 = config.stress_strain_relpath / file1
        path2 = config.stress_strain_npy_relpath / file2
        loaded = io.loadmat(path1)

        np.save(path2, loaded['times_real'])

    delvol_path = config.delvol_data_relpath
    stress_strain_path = config.stress_strain_npy_relpath

    delvol_files = list(delvol_path.glob('*.txt'))
    stress_strain_files = list(stress_strain_path.glob('*.npy'))

    delvol_data = []
    stress_strain_data = []

    delvol_columns = [
        'delvtot', 'delv50', 'time', 'sig_d', 'x', 'y', 'z', 'dmin_min',
        'dmin_25', 'dmin_50', 'dmin_75', 'dmin_max', 'th1_min', 'th1_25',
        'th1_50', 'th1_75', 'th1_max', 'th3_min', 'th3_25', 'th3_50', 'th3_75',
        'th3_max', 'l1_min', 'l1_25', 'l1_50', 'l1_75', 'l1_max', 'l3_min',
        'l3_25', 'l3_50', 'l3_75', 'l3_max', 'ani_min', 'ani_25', 'ani_50',
        'ani_75', 'ani_max', 'vol_min', 'vol_25', 'vol_50', 'vol_75', 'vol_max',
        'dc_25', 'dc_50', 'dc_75', 'dc_max', 'tot_vol', 'rand'
    ]

    stress_strain_columns = ['time', 'eps', 'distf', 'sig_d']

    delvol_columns = {i:j for j,i in enumerate(delvol_columns)}
    stress_strain_columns = {i:j for j,i in enumerate(stress_strain_columns)}

    for i in delvol_files:
        with open(i, 'r') as infile:
            lines = infile.readlines()[1:]
        for n, line in enumerate(lines):
            lines[n] = [float(i) for i in line.split(' ')[:-1]]
        delvol_data.append(np.array(lines, dtype = np.float64))

    for i in stress_strain_files:
        lines = np.load(i)
        stress_strain_data.append(np.array(lines, dtype = np.float64))

    # Creating a map from sig_d (time to failure) to eps (axial strain)
    stress_strain_map = {}
    idx1 = stress_strain_columns['sig_d']
    idx2 = stress_strain_columns['eps']
    for doc, name in zip(stress_strain_data, stress_strain_files):
        row = {}
        for j in range(doc.shape[0]):
            sig_d_val = doc[j,idx1]
            eps_val = doc[j,idx2]
            if sig_d_val not in row.keys():
                row[sig_d_val] = eps_val
            elif row[sig_d_val] != eps_val:
                msg = (
                    f'Inconsistency found: {row[sig_d_val]} != {eps_val}'
                )
                print(msg)
        pat = r'times_([A-Z0-9_]+).npy'
        key = re.sub(pat, r'\1', name.name)
        stress_strain_map[key] = row

    # Dividing the delvol into subvolumes by sig_d
    delvol_all = {}
    for doc, name in zip(delvol_data, delvol_files):
        subv = {}
        for row in doc:
            sig_d = row[delvol_columns['sig_d']]
            if sig_d not in subv.keys():
                subv[sig_d] = [row]
            else:
                subv[sig_d].append(row)
        pat = r'([A-Z0-9_]+)_3D_delvol_a3000_subv300.txt'
        key = re.sub(pat, r'\1', name.name)
        delvol_all[key] = subv

    delvol_final = {}
    stress_strain_final = {}
    for key in delvol_all.keys():
        dv_keys = np.array(list(delvol_all[key].keys()), dtype = float)
        ss_keys = np.array(list(stress_strain_map[key].keys()), dtype = float)
        ss_keys = {i:j for i,j in zip(np.round(ss_keys, 3), ss_keys)}
        delvol_final[key] = {}
        stress_strain_final[key] = {}

        for i in dv_keys:
            if i in ss_keys:
                delvol_final[key][i] = delvol_all[key][i]
                stress_strain_final[key][i] = stress_strain_map[key][ss_keys[i]]

    # Making arrays of sig_d to eps
    sig_d = {}
    eps = {}
    for key in delvol_final:
        sig_d_vals = sorted(list(delvol_final[key].keys()))
        sig_d[key] = []
        eps[key] = []
        for i in sig_d_vals:
            sig_d[key].append(i)
            eps[key].append(stress_strain_final[key][i])

    for label, idx in delvol_columns.items():
        for key1 in delvol_final:
            pairs = []
            for key2 in delvol_final[key1]:
                rows = delvol_final[key1][key2]
                for row in rows:
                    pairs.append((key2, row[idx]))
            filename = f'{key1}_{label}.csv'
            csv_out = '\n'.join(f'{i[0]},{i[1]}' for i in pairs)
            path = config.fmt_data_relpath / filename
            with open(path, 'w+') as outfile:
                outfile.write(csv_out)

    for label, idx in delvol_columns.items():
        for key1 in delvol_final:
            triplets = []
            for key2 in delvol_final[key1]:
                rows = delvol_final[key1][key2]
                vals = []
                for row in rows:
                    vals.append(row[idx])
                triplets.append((key2, np.mean(vals), np.std(vals)))

            filename = f'{key1}_{label}_avg.csv'
            csv_out = '\n'.join(f'{i[0]},{i[1]},{i[2]}' for i in triplets)
            path = config.fmt_data_relpath / filename
            with open(path, 'w+') as outfile:
                outfile.write(csv_out)

    for key in delvol_final:
        pairs = []
        for i,j in zip(sig_d[key], eps[key]):
            pairs.append((i, j))
        filename = f'{key}_eps.csv'
        csv_out = '\n'.join(f'{i[0]},{i[1]}' for i in pairs)
        path = config.fmt_data_relpath / filename
        with open(path, 'w+') as outfile:
            outfile.write(csv_out)

def procedure_sync():

    BucketManager.sync()

def procedure_force_sync():
    BucketManager.sync(force = True)

def procedure_delden_combine():

    terminal.reset_screen()
    directory = config.delden_relpath

    filename_pat = (
        r'combined\_(\d{4})\-(\d{2})\-(\d{2}) (\d{2})\:(\d{2})\:(\d{2})\.(\d{6})'
    )
    filename_repl = (
        r'\1/\2/\3 \4:\5:\6.\7'
    )

    files = []
    for f in directory.glob('*'):
        if len(re.findall(filename_pat, f.name)) != 0:
            files.append(f.name)

    N = len(files)
    if N == 0:
        msg = (
            f'\n\nNo combined delden experiments found.  Run `python main.py '
            f'--delden-all` to create a set of experiment output files in '
            f'`~/Documents/MasterThesis/results/delden/`.\n'
        )
        raise FileNotFoundError(msg)
    elif N == 1:
        selection = select.select_bool(f'Select Experiment `{files[0]}`?')
        if not selection:
            print('Terminating.')
            exit()
        else:
            selection = files[0]
    else:
        selection = select.scroll_select(
            f'Select an Experiment – {N} option(s)', files
        )

    path = directory / selection

    terminal.reset_screen()
    print(format.B('Selected Experiment: ') + format.I(selection))
    parsers.combine_delden_results(selection)

def procedure_delvol_combine():

    terminal.reset_screen()
    directory = config.delvol_relpath

    filename_pat = (
        r'linspace\_(\d{4})\-(\d{2})\-(\d{2}) (\d{2})\:(\d{2})\:(\d{2})\.(\d{6})'
    )
    filename_repl = (
        r'\1/\2/\3 \4:\5:\6.\7'
    )

    files = []
    for f in directory.glob('*'):
        # if len(re.findall(filename_pat, f.name)) != 0:
        files.append(f.name)

    N = len(files)
    if N == 0:
        msg = (
            f'\n\nNo linspace delvol experiments found.  Run '
            f'`python main.py --delvol-linspace` to create a set of experiment '
            f'output files in `~/Documents/MasterThesis/results/delvol/`.\n'
        )
        raise FileNotFoundError(msg)
    elif N == 1:
        selection = select.select_bool(f'Select Experiment `{files[0]}`?')
        if not selection:
            print('Terminating.')
            exit()
        else:
            selection = files[0]
    else:
        selection = select.scroll_select(
            f'Select an Experiment – {N} option(s)', files
        )

    path = directory / selection

    terminal.reset_screen()
    print(format.B('Selected Experiment: ') + format.I(selection))
    parsers.combine_linspace_results(selection)

def procedure_delvol_logspace():

    BucketManager.download('delvol_data')
    terminal.reset_screen()

    experiment = 'MONZ4'
    N_experiments = np.ceil(np.logspace(1, 2.2, 30)).astype(np.int64)
    exps = backend.groups.delvol_exps['all']

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    terminal.reset_screen()

    directory = backend.utils.select.create_unique_name(prefix = 'logspace')
    path = backend.config.delvol_relpath / directory
    path.mkdir(exist_ok = True)
    length = len(N_experiments)
    training_label = 'delv50'
    for n,i in enumerate(N_experiments):
        title = backend.utils.format.B(f'EXPERIMENT FOR N={i:d} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
        delvol.set_experiments(experiment)
        delvol.set_training_label(training_label)
        delvol.grid_search(
            itermax = i, train_size = 0.75, **gridsearch_params
        )
        delvol.save(filename = f'{experiment}_N{i:d}')

    with open(path / config.delvol_x_data_logspace, 'w+') as outfile:
        outfile.write(','.join(str(i) for i in N_experiments))

    parsers.combine_logspace_results(directory)
    delvol_logspace_plot(directory)

def procedure_delvol_linspace():

    BucketManager.download('delvol_data')
    terminal.reset_screen()

    experiment = 'MONZ4'
    N_experiments = np.ceil(np.linspace(5, 150, 30)).astype(np.int64)
    exps = backend.groups.delvol_exps['all']

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    terminal.reset_screen()

    directory = backend.utils.select.create_unique_name(prefix = 'linspace')
    path = backend.config.delvol_relpath / directory
    path.mkdir(exist_ok = True)
    length = len(N_experiments)
    training_label = 'delv50'
    for n,i in enumerate(N_experiments):
        title = backend.utils.format.B(f'EXPERIMENT FOR N={i:d} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
        delvol.set_experiments(experiment)
        delvol.set_training_label(training_label)
        delvol.grid_search(
            itermax = i, train_size = 0.75, **gridsearch_params
        )
        delvol.save(filename = f'{experiment}_N{i:d}')

    with open(path / config.delvol_x_data_linspace, 'w+') as outfile:
        outfile.write(','.join(str(i) for i in N_experiments))

    parsers.combine_linspace_results(directory)
    delvol_linspace_plot(directory)

def procedure_stress_strain():

    import matplotlib.pyplot as plt
    paths = config.stress_strain_npy_relpath.glob('*.npy')

    for path in paths:
        if 'WG04' in path.name:
            data = np.load(path)
            eps = data[:,1]         # Axial Strain
            sigds = data[:,2]       # Time to Failure
            distf = data[:,3]       # Normalized Stress & Distance to Failure

            plt.grid()
            plt.plot(sigds, eps)
            plt.xlabel('Differential Stress [MPa]')
            plt.ylabel('Axial Strain [Dimensionless]')
            plt.xlim(np.min(sigds), np.max(sigds))
            plt.show()

def procedure_plot_ondemand():

    directory = 'Plots On-Demand'

    exps = ['M8_1', 'M8_2', 'MONZ3', 'MONZ4', 'MONZ5', 'WG01', 'WG02', 'WG04']

    labels = {
        'delvtot'   : 'Change in Total Volume',
        'delv50'    : 'Change in 50ᵗʰ Percentile Volume',
        'time'      : 'Time',
        # 'sig_d'     : 'Differential Stress [MPa]',
        'sig_d'     : 'Time to Failure [Dimensionless]',
        'x'         : 'Position (x)',
        'y'         : 'Position (y)',
        'z'         : 'Position (z)',
        'dmin_min'  : 'Minimum of Minimum Distance Between Fracture Centroids',
        'dmin_25'   : '25ᵗʰ Percentile Minimum Distance Between Fracture Centroids',
        'dmin_50'   : '50ᵗʰ Percentile Minimum Distance Between Fracture Centroids',
        'dmin_75'   : '75ᵗʰ Percentile Minimum Distance Between Fracture Centroids',
        'dmin_max'  : 'Maximum of Minimum Distance Between Fracture Centroids',
        'th1_min'   : 'Minimum Orientiation of Min. Eigenvector',
        'th1_25'    : '25ᵗʰ Percentile Orientiation of Min. Eigenvector',
        'th1_50'    : '50ᵗʰ Percentile Orientiation of Min. Eigenvector',
        'th1_75'    : '75ᵗʰ Percentile Orientiation of Min. Eigenvector',
        'th1_max'   : 'Maximum Orientiation of Min. Eigenvector',
        'th3_min'   : 'Minimum Orientation of Max. Eigenvector',
        'th3_25'    : '25ᵗʰ Percentile Orientation of Max. Eigenvector',
        'th3_50'    : '50ᵗʰ Percentile Orientation of Max. Eigenvector',
        'th3_75'    : '75ᵗʰ Percentile Orientation of Max. Eigenvector',
        'th3_max'   : 'Maximum Orientation of Max. Eigenvector',
        'l1_min'    : 'Minimum of Min. Eigenvalue, Fracture Aperture',
        'l1_25'     : '25ᵗʰ Percentile Min. Eigenvalue, Fracture Aperture',
        'l1_50'     : '50ᵗʰ Percentile Min. Eigenvalue, Fracture Aperture',
        'l1_75'     : '75ᵗʰ Percentile Min. Eigenvalue, Fracture Aperture',
        'l1_max'    : 'Maximum of Min. Eigenvalue, Fracture Aperture',
        'l3_min'    : 'Minimum of Max. Eigenvalue, Fracture Aperture',
        'l3_25'     : '25ᵗʰ Percentile Max. Eigenvalue, Fracture Aperture',
        'l3_50'     : '50ᵗʰ Percentile Max. Eigenvalue, Fracture Aperture',
        'l3_75'     : '75ᵗʰ Percentile Max. Eigenvalue, Fracture Aperture',
        'l3_max'    : 'Maximum of Max. Eigenvalue, Fracture Aperture',
        'ani_min'   : 'Minimum of Shape Anisotropy',
        'ani_25'    : '25ᵗʰ Percentile Shape Anisotropy',
        'ani_50'    : '50ᵗʰ Percentile Shape Anisotropy',
        'ani_75'    : '75ᵗʰ Percentile Shape Anisotropy',
        'ani_max'   : 'Maximum of Shape Anisotropy',
        'vol_min'   : 'Minimum of Individual Fracture Volume',
        'vol_25'    : '25ᵗʰ Percentile Individual Fracture Volume',
        'vol_50'    : '50ᵗʰ Percentile Individual Fracture Volume',
        'vol_75'    : '75ᵗʰ Percentile Individual Fracture Volume',
        'vol_max'   : 'Maximum of Individual Fracture Volume',
        'dc_25'     : 'Minimum of Distance Between Centroids',
        'dc_50'     : '25ᵗʰ Percentile Distance Between Centroids',
        'dc_75'     : '50ᵗʰ Percentile Distance Between Centroids',
        'dc_max'    : '75ᵗʰ Percentile Distance Between Centroids',
        'tot_vol'   : 'Fracture Volume',
        'rand'      : 'Randomly Generated Values',
        'eps'       : 'Axial Strain [Dimensionless]',
    }


    no_outliers = backend.utils.select.select_bool('Remove Outliers?')
    if no_outliers:
        script = 'delvol_plot_prepped_no_outliers.m'
    else:
        script = 'delvol_plot_prepped.m'

    experiment = None
    while experiment not in exps:
        experiment = input('Please enter a valid experiment label.\n> ')
        if experiment not in exps:
            print('Invalid! Try Again.')

    label = None
    while label not in labels.keys():
        label = input('Please enter a valid column label.\n> ')
        if label not in labels.keys():
            print('Invalid! Try Again.')
    ylabel = labels[label]

    print()

    filename = f'{experiment}_{label}'
    path = backend.config.matlab_img_relpath
    path = path / directory
    path.mkdir(exist_ok = True)

    if no_outliers:
        save_name = directory + f'/{filename}_no_outliers.png'
    else:
        save_name = directory + f'/{filename}.png'

    variables = (
        f"filename = \'{filename}.csv\'; save_name = \'{str(save_name)}\'; "
        f"label = \'{ylabel}\';"
    )

    backend.select.run_matlab(
        suppress = True,
        script_name = script,
        variables = variables
    )

def procedure_plots_all():

    directory = 'Plots All'

    exps = ['M8_1', 'M8_2', 'MONZ3', 'MONZ4', 'MONZ5', 'WG01', 'WG02', 'WG04']

    labels = {
        'delvtot'   : 'Change in Total Volume',
        'delv50'    : 'Change in 50ᵗʰ Percentile Volume',
        'time'      : 'Time',
        # 'sig_d'     : 'Differential Stress [MPa]',
        'sig_d'     : 'Time to Failure [Dimensionless]',
        'x'         : 'Position (x)',
        'y'         : 'Position (y)',
        'z'         : 'Position (z)',
        'dmin_min'  : 'Minimum of Minimum Distance Between Fracture Centroids',
        'dmin_25'   : '25ᵗʰ Percentile Minimum Distance Between Fracture Centroids',
        'dmin_50'   : '50ᵗʰ Percentile Minimum Distance Between Fracture Centroids',
        'dmin_75'   : '75ᵗʰ Percentile Minimum Distance Between Fracture Centroids',
        'dmin_max'  : 'Maximum of Minimum Distance Between Fracture Centroids',
        'th1_min'   : 'Minimum Orientiation of Min. Eigenvector',
        'th1_25'    : '25ᵗʰ Percentile Orientiation of Min. Eigenvector',
        'th1_50'    : '50ᵗʰ Percentile Orientiation of Min. Eigenvector',
        'th1_75'    : '75ᵗʰ Percentile Orientiation of Min. Eigenvector',
        'th1_max'   : 'Maximum Orientiation of Min. Eigenvector',
        'th3_min'   : 'Minimum Orientation of Max. Eigenvector',
        'th3_25'    : '25ᵗʰ Percentile Orientation of Max. Eigenvector',
        'th3_50'    : '50ᵗʰ Percentile Orientation of Max. Eigenvector',
        'th3_75'    : '75ᵗʰ Percentile Orientation of Max. Eigenvector',
        'th3_max'   : 'Maximum Orientation of Max. Eigenvector',
        'l1_min'    : 'Minimum of Min. Eigenvalue, Fracture Aperture',
        'l1_25'     : '25ᵗʰ Percentile Min. Eigenvalue of Fracture Aperture',
        'l1_50'     : '50ᵗʰ Percentile Min. Eigenvalue of Fracture Aperture',
        'l1_75'     : '75ᵗʰ Percentile Min. Eigenvalue of Fracture Aperture',
        'l1_max'    : 'Maximum of Min. Eigenvalue, Fracture Aperture',
        'l3_min'    : 'Minimum of Max. Eigenvalue, Fracture Aperture',
        'l3_25'     : '25ᵗʰ Percentile Max. Eigenvalue of Fracture Aperture',
        'l3_50'     : '50ᵗʰ Percentile Max. Eigenvalue of Fracture Aperture',
        'l3_75'     : '75ᵗʰ Percentile Max. Eigenvalue of Fracture Aperture',
        'l3_max'    : 'Maximum of Max. Eigenvalue, Fracture Aperture',
        'ani_min'   : 'Minimum of Shape Anisotropy',
        'ani_25'    : '25ᵗʰ Percentile Shape Anisotropy',
        'ani_50'    : '50ᵗʰ Percentile Shape Anisotropy',
        'ani_75'    : '75ᵗʰ Percentile Shape Anisotropy',
        'ani_max'   : 'Maximum of Shape Anisotropy',
        'vol_min'   : 'Minimum of Individual Fracture Volume',
        'vol_25'    : '25ᵗʰ Percentile Individual Fracture Volume',
        'vol_50'    : '50ᵗʰ Percentile Individual Fracture Volume',
        'vol_75'    : '75ᵗʰ Percentile Individual Fracture Volume',
        'vol_max'   : 'Maximum of Individual Fracture Volume',
        'dc_25'     : 'Minimum of Distance Between Centroids',
        'dc_50'     : '25ᵗʰ Percentile Distance Between Centroids',
        'dc_75'     : '50ᵗʰ Percentile Distance Between Centroids',
        'dc_max'    : '75ᵗʰ Percentile Distance Between Centroids',
        'tot_vol'   : 'Fracture Volume',
        'rand'      : 'Randomly Generated Values',
        # 'eps'       : 'Axial Strain [Dimensionless]',
    }

    no_outliers = backend.utils.select.select_bool('Remove Outliers?')
    averaged = backend.utils.select.select_bool('Take Averages?')
    print()

    if no_outliers:
        script = 'delvol_plot_prepped_no_outliers'
    else:
        script = 'delvol_plot_prepped'

    if averaged:
        script += '_avg'
    script += '.m'

    scripts = []
    variables = []

    for experiment in exps:
        for label in labels:

            filename = f'{experiment}_{label}'
            path = backend.config.matlab_img_relpath
            path = path / directory
            path.mkdir(exist_ok = True)

            if averaged:
                filename += '_avg'

            if no_outliers:
                save_name = directory + f'/{filename}_no_outliers'
            else:
                save_name = directory + f'/{filename}'

            if averaged:
                save_name += '_avg'

            save_name += '.png'

            row = (
                f"filename = \'{filename}.csv\'; save_name = \'{str(save_name)}\'; "
                f"label = \'{labels[label]}\';"
            )

            scripts.append(script)
            variables.append(row)

    backend.select.run_matlab_set(
        suppress = True, scripts = scripts, variables = variables
    )

def procedure_matlab():
    directories = [
        'combined_2020-10-06 07:39:50.711793',
        'combined_2020-10-06 03:09:27.034176',
    ]

    for directory in directories:
        save_name = directory + '_compare_01' + '.png'
        backend.select.run_matlab(
            script_name = 'delden_compare_01.m',
            variables = (
                f"directory = \'{directory}\'; save_name = \'{save_name}\';"
            )
        )

        save_name = directory + '_hist_01' + '.png'
        backend.select.run_matlab(
            script_name = 'delden_hist_01.m',
            variables = (
                f"directory = \'{directory}\'; save_name = \'{save_name}\';"
            )
        )

        save_name = directory + '_compare' + '.png'
        backend.select.run_matlab(
            script_name = 'delden_compare.m',
            variables = (
                f"directory = \'{directory}\'; save_name = \'{save_name}\';"
            )
        )
        save_name = directory + '_hist' + '.png'
        backend.select.run_matlab(
            script_name = 'delden_hist.m',
            variables = (
                f"directory = \'{directory}\'; save_name = \'{save_name}\';"
            )
        )

def procedure_install():
    backend.install.install()

def procedure_uninstall():
    backend.install.uninstall()

"""MAIN SCRIPT"""

args = parse_args()

if args.unit_tests:
    tests.run_tests()

if args.split:
    BucketManager.download('bins')
    backend.binfo.Binfo.load_data()
    preset = defaults.split_defaults
    config_info = format.config_info(preset)
    msg = f'{config_info}\nUse default configuration?'
    if select.select_bool(msg):
        X_train, X_test, y_train, y_test = split_2D.test_train_split(**preset)
        X_train, X_test, y_train, y_test =\
        filter.remove_empty(X_train, X_test, y_train, y_test)
        savename = 'default'
        print(format.B('Saving Segments'))
        file_io.save_split(savename, X_train, X_test, y_train, y_test)
        print(format.B('Saved to ') + format.I(f'{config.split_bins_relpath}{savename}'))
    else:
        procedure_split()

if args.train_DNN:
    BucketManager.download('bins')
    procedure_train_DNN()

if args.score_DNN:
    procedure_score_DNN()

if args.custom:

    BucketManager.download('delvol_data')
    terminal.reset_screen()

    experiments = ['MONZ3']
    training_labels = ['delvtot', 'sig_d']
    N_repeats = 1
    N_experiments = np.ceil(np.linspace(5, 100, 24)).astype(np.int64)
    exps = backend.groups.delvol_exps['all']

    gridsearch_params = {
        "colsample_bytree": [0.3, 0.5, 0.7, 0.9],
        "alpha":            [0, 0.001, 0.01, 0.1],
        "learning_rate":    [0.005, 0.01, 0.05, 0.1, 0.5],
        "n_estimators":     [10, 25, 50, 100, 150],
        "max_depth":        [1, 3, 5, 7, 9, 11]
    }

    length = len(N_experiments)*N_repeats
    length *= len(training_labels)*len(experiments)

    factors = [
        len(N_experiments), len(N_experiments)*N_repeats,
        len(N_experiments)*N_repeats*len(training_labels)
    ]

    for N1, experiment in enumerate(experiments):
        for N2, training_label in enumerate(training_labels):
            for N3 in range(N_repeats):
                try:
                    terminal.reset_screen()

                    directory = backend.utils.select.create_unique_name(
                        prefix = 'linspace'
                    )

                    path = backend.config.delvol_relpath / directory
                    path.mkdir(exist_ok = True)
                    for n,i in enumerate(N_experiments):
                        curr = n + N1*factors[0] + N2*factors[1] + N3*factors[2]
                        title = backend.utils.format.B(f'EXPERIMENT FOR N={i:d} ')
                        title += backend.utils.format.I(f'({curr}/{length})')
                        title += f'\tEXP:{experiment}\t TARGET:{training_label}'
                        delvol = DelVolDensity.DelVolDensity(
                            save_dir = path, title = title
                        )
                        delvol.set_experiments(experiment)
                        delvol.set_training_label(training_label)
                        delvol.grid_search(
                            itermax = i, train_size = 0.75, **gridsearch_params
                        )
                        delvol.save(filename = f'{experiment}_N{i:d}')

                    with open(path / config.delvol_x_data_linspace, 'w+') as outfile:
                        outfile.write(','.join(str(i) for i in N_experiments))

                    parsers.combine_linspace_results(directory)
                    delvol_linspace_plot(directory)

                except Exception as e:

                    with open(Path.home() / 'Documents/error_log.txt', 'a+') as outfile:
                        T = datetime.datetime.now()
                        msg = (
                            f'Error in iteration {n} of exp {experiment} at {T}:\n'
                            f'\t{e}\nDescription:\t{title}\n\n'
                        )
                        outfile.write(msg)

if args.delvol_linspace:
    procedure_delvol_linspace()

if args.delvol_logspace:
    procedure_delvol_logspace()

if args.test:

    # directory = 'delvtot'
    # script = 'delvol_importances_mean.m'
    # save_name = directory + '/importances_mean.png'
    # var = f"directory = \'{directory}\'; save_name = \'{save_name}\'; "
    # backend.select.run_matlab(
    #     suppress = False,
    #     script_name = script,
    #     variables = var
    # )

    # from scipy import io
    #
    # exps = [
    #     'M8_1',
    #     'M8_2',
    #     'MONZ3',
    #     'MONZ4',
    #     'MONZ5',
    #     'WG01',
    #     'WG02',
    #     'WG04',
    # ]
    #
    # files = [
    #     'times_M8_1.mat',
    #     'times_M8_2.mat',
    #     'times_MONZ3.mat',
    #     'times_MONZ4.mat',
    #     'times_MONZ5.mat',
    #     'times_WG01.mat',
    #     'times_WG02.mat',
    #     'times_WG04.mat',
    # ]
    #
    # new_files = [
    #     'times_M8_1.npy',
    #     'times_M8_2.npy',
    #     'times_MONZ3.npy',
    #     'times_MONZ4.npy',
    #     'times_MONZ5.npy',
    #     'times_WG01.npy',
    #     'times_WG02.npy',
    #     'times_WG04.npy',
    # ]
    #
    # script = 'delvol_stress_strain.m'
    # vars = []
    # scripts = []
    #
    # for file1, file2, exp in zip(files, new_files, exps):
    #
    #     save_name = f'{exp}_stress_strain.png'
    #
    #     var = (
    #         f'filename = \'{file1}\'; save_name = \'{save_name}\';'
    #     )
    #
    #     vars.append(var)
    #     scripts.append(script)
    #
    #     path1 = config.stress_strain_relpath / file1
    #     path2 = config.stress_strain_npy_relpath / file2
    #     loaded = io.loadmat(path1)
    #
    #     np.save(path2, loaded['times_real'])
    #
    # backend.select.run_matlab_set(
    #     suppress = False,
    #     scripts = scripts,
    #     variables = vars
    # )

    selections = [
        'delvtot_marble',   'delvtot_monzonite',    'delvtot_granite',
        'sigd_marble',      'sigd_monzonite',       'sigd_granite',
        'delvtot_all', 'sigd_all',
    ]

    for selection in selections:
        save_plot_delvol(selection, suppress = False)
        if selection in ['delvtot_all', 'sigd_all']:
            save_plot_delvol_conditional(selection, suppress = False)

if args.cluster:
    procedure_cluster()

if args.delden:
    procedure_delden()

if args.delden_all:
    procedure_delden_all()

if args.delden_all_log:
    procedure_delden_all_log()

if args.delden_groups:
    procedure_delden_groups()

if args.delden_groups_log:
    procedure_delden_groups_log()

if args.delden_compare:
    procedure_delden_compare()

if args.delvol_all:
    procedure_delvol_all()

if args.delvol_lite:
    procedure_delvol_lite()

if args.delvol_all_log:
    procedure_delvol_all_log()

if args.delvol_groups:
    procedure_delvol_groups()

if args.delvol_groups_log:
    procedure_delvol_groups_log()

if args.delvol_plots:
    procedure_delvol_plots()

if args.final_plots:
    procedure_final_plots()

if args.delvol_logspace_plots:
    procedure_delvol_logspace_plots()

if args.delvol_linspace_plots:
    procedure_delvol_linspace_plots()

if args.delvol_data_prep:
    procedure_delvol_data_prep()

if args.plot_ondemand:
    procedure_plot_ondemand()

if args.plots_all:
    procedure_plots_all()

if args.sync:
    procedure_sync()

if args.force_sync:
    procedure_force_sync()

if args.delden_combine:
    procedure_delden_combine()

if args.delvol_combine:
    procedure_delvol_combine()

if args.stress_strain:
    procedure_stress_strain()

if args.matlab:
    procedure_matlab()

if args.install:
    procedure_install()

if args.uninstall:
    procedure_uninstall()
