from pathlib import Path
import numpy as np
import argparse
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

    help_matlab = (
        'Runs a custom MATLAB script.'
    )

    help_install = (
        'Downloads data files and installs the pipenv.'
    )

    help_uninstall = (
        'Removes downloaded data files, experiments, and all processed files.'
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
        '--sync', action='store_true', help = help_sync
    )
    parser.add_argument(
        '--force-sync', action='store_true', help = help_force_sync
    )
    parser.add_argument(
        '--delden-combine', action='store_true', help = help_delden_combine
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
        script_relpath = './matlab/delden_compare.m',
        variables = (
            f"directory = \'{directory}\'; save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/compare_01' + '.png'
    backend.select.run_matlab(
        suppress = suppress,
        script_relpath = './matlab/delden_compare_01.m',
        variables = (
            f"directory = \'{directory}\'; save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/hist' + '.png'
    backend.select.run_matlab(
        suppress = suppress,
        script_relpath = './matlab/delden_hist.m',
        variables = (
            f"directory = \'{directory}\'; save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/hist_01' + '.png'
    backend.select.run_matlab(
        suppress = suppress,
        script_relpath = './matlab/delden_hist_01.m',
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
        script_relpath = './matlab/delden_chart_exps.m',
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
        script_relpath = './matlab/delden_chart_exps_best.m',
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
        script_relpath = './matlab/delden_chart_exps_worst.m',
        variables = (
            f"directory = \'{directory}\'; "
            f"save_name_1 = \'{save_name_1}\'; "
            f"save_name_2 = \'{save_name_2}\'; "
            f"save_name_3 = \'{save_name_3}\'; "
            f"save_name_4 = \'{save_name_4}\'; "
        )
    )

def save_plot_delvol(directory:str, path:Path = None, suppress:bool = True):
    '''
        Saves a variety of plots for the `compare` results of delvol.
    '''

    if path is None:
        path = backend.config.matlab_img_relpath
    path = path / directory
    path.mkdir(exist_ok = True)

    save_name = directory + '/compare' + '.png'
    backend.select.run_matlab(
        suppress = suppress,
        script_relpath = './matlab/delvol_compare.m',
        variables = (
            f"directory = \'{directory}\'; save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/compare_01' + '.png'
    backend.select.run_matlab(
        suppress = suppress,
        script_relpath = './matlab/delvol_compare_01.m',
        variables = (
            f"directory = \'{directory}\'; save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/hist' + '.png'
    backend.select.run_matlab(
        suppress = suppress,
        script_relpath = './matlab/delvol_hist.m',
        variables = (
            f"directory = \'{directory}\'; save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/hist_01' + '.png'
    backend.select.run_matlab(
        suppress = suppress,
        script_relpath = './matlab/delvol_hist_01.m',
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
        script_relpath = './matlab/delvol_chart_exps.m',
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
        script_relpath = './matlab/delvol_chart_exps_best.m',
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
        script_relpath = './matlab/delvol_chart_exps_worst.m',
        variables = (
            f"directory = \'{directory}\'; "
            f"save_name_1 = \'{save_name_1}\'; "
            f"save_name_2 = \'{save_name_2}\'; "
            f"save_name_3 = \'{save_name_3}\'; "
            f"save_name_4 = \'{save_name_4}\'; "
        )
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
        script_relpath = './matlab/delden_log_compare.m',
        variables = (
            f"directory_1 = \'{directory_1}\'; directory_2 = \'{directory_2}\';"
            f" save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/compare_01' + '.png'
    backend.select.run_matlab(
        script_relpath = './matlab/delden_log_compare_01.m',
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
        script_relpath = './matlab/delvol_compare.m',
        variables = (
            f"directory_1 = \'{directory_1}\'; directory_2 = \'{directory_2}\';"
            f" save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/compare_01' + '.png'
    backend.select.run_matlab(
        script_relpath = './matlab/delvol_compare_01.m',
        variables = (
            f"directory_1 = \'{directory_1}\'; directory_2 = \'{directory_2}\';"
            f" save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/log_compare' + '.png'
    backend.select.run_matlab(
        script_relpath = './matlab/delvol_log_compare.m',
        variables = (
            f"directory_1 = \'{directory_1}\'; directory_2 = \'{directory_2}\';"
            f" save_name = \'{save_name}\';"
        )
    )

    save_name = directory + '/log_compare_01' + '.png'
    backend.select.run_matlab(
        script_relpath = './matlab/delvol_log_compare_01.m',
        variables = (
            f"directory_1 = \'{directory_1}\'; directory_2 = \'{directory_2}\';"
            f" save_name = \'{save_name}\';"
        )
    )

def procedure_delvol_all():

    BucketManager.download('delvol_data')
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
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENT {i} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
        delvol.set_experiments(i)
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
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENT {i} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
        delvol.set_experiments(i)
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
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENTS {", ".join(i)} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
        delvol.set_experiments(*i)
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
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENTS {", ".join(i)} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delvol = DelVolDensity.DelVolDensity(save_dir = path, title = title)
        delvol.set_experiments(*i)
        delvol.grid_search(
            itermax = N_experiments, train_size = 0.75, log = True,
            **gridsearch_params
        )
        delvol.save(filename = '-'.join(i))

    parsers.combine_delvol_results(path)
    save_plot_delvol(directory)

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

def procedure_matlab():
    directories = [
        'combined_2020-10-06 07:39:50.711793',
        'combined_2020-10-06 03:09:27.034176',
    ]

    for directory in directories:
        save_name = directory + '_compare_01' + '.png'
        backend.select.run_matlab(
            script_relpath = './matlab/delden_compare_01.m',
            variables = (
                f"directory = \'{directory}\'; save_name = \'{save_name}\';"
            )
        )

        save_name = directory + '_hist_01' + '.png'
        backend.select.run_matlab(
            script_relpath = './matlab/delden_hist_01.m',
            variables = (
                f"directory = \'{directory}\'; save_name = \'{save_name}\';"
            )
        )

        save_name = directory + '_compare' + '.png'
        backend.select.run_matlab(
            script_relpath = './matlab/delden_compare.m',
            variables = (
                f"directory = \'{directory}\'; save_name = \'{save_name}\';"
            )
        )
        save_name = directory + '_hist' + '.png'
        backend.select.run_matlab(
            script_relpath = './matlab/delden_hist.m',
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

if args.test:
    save_plot_delvol('combined_2020-11-12 15:38:51.531613', suppress = False)
    save_plot_delvol('combined_2020-11-12 22:54:54.260169', suppress = False)

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

if args.delvol_all_log:
    procedure_delvol_all_log()

if args.delvol_groups:
    procedure_delvol_groups()

if args.delvol_groups_log:
    procedure_delvol_groups_log()

if args.sync:
    procedure_sync()

if args.force_sync:
    procedure_force_sync()

if args.delden_combine:
    procedure_delden_combine()

if args.matlab:
    procedure_matlab()

if args.install:
    procedure_install()

if args.uninstall:
    procedure_uninstall()
