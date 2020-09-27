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
        '--sync', action='store_true', help = help_sync
    )
    parser.add_argument(
        '--force-sync', action='store_true', help = help_force_sync
    )
    parser.add_argument(
        '--delden-combine', action='store_true', help = help_delden_combine
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
    # exps = ['WG04',]

    gridsearch_params = {
        "colsample_bytree": [0.6, 0.7, 0.8, 0.9, 1.0],
        "alpha":            [0, 1, 2, 3],
        "learning_rate":    [0.01, 0.5, 0.1, 0.2],
        "n_estimators":     [200, 300, 400],
        "max_depth":        [4, 5, 6, 7]
    }

    terminal.reset_screen()

    directory = backend.utils.select.create_unique_name(prefix = 'combined')
    path = backend.config.delden_relpath / directory
    path.mkdir(exist_ok = True)
    with open(path / 'experiments.txt', 'w+') as outfile:
        outfile.write(','.join(exps))
    length = len(exps)
    for n,i in enumerate(exps):
        title = backend.utils.format.B(f'EXPERIMENT {i} ')
        title += backend.utils.format.I(f'({n+1}/{length})')
        delden = DelDensity.DelDensity(save_dir = path, title = title)
        delden.set_experiments(i)
        delden.grid_search(itermax = N_experiments, **gridsearch_params)
        delden.save(filename = i)

    parsers.combine_deldensity_results(path)

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
    parsers.combine_deldensity_results(selection)

def procedure_install():
    backend.install.install()

def procedure_uninstall():
    backend.install.uninstall()

"""MAIN SCRIPT"""

args = parse_args()

if args.unit_tests is True:
    tests.run_tests()

if args.split is True:
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

if args.train_DNN is True:
    BucketManager.download('bins')
    procedure_train_DNN()

if args.score_DNN is True:
    procedure_score_DNN()

if args.test is True:
    # BucketManager.sync()
    BucketManager.download('density_data', force = True)

if args.cluster is True:
    procedure_cluster()

if args.delden is True:
    procedure_delden()

if args.delden_all is True:
    procedure_delden_all()

if args.sync is True:
    procedure_sync()

if args.force_sync is True:
    procedure_force_sync()

if args.delden_combine is True:
    procedure_delden_combine()

if args.install is True:
    procedure_install()

if args.uninstall is True:
    procedure_uninstall()
