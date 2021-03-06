from typing import List, Tuple, Dict
from datetime import datetime
from textwrap import wrap
from pathlib import Path
from io import StringIO
import warnings
import sys
import os

from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import xgboost as xgb
import pandas as pd
import numpy as np

from ..config.defaults import delden_xgb_gridsearch_defaults as xgb_def
from ..config.groups import delden_groups, delden_exps
from ..config.config import n_jobs as delden_n_jobs
from ..utils.select import create_unique_name
from ..utils.format import B, I, clean_str
from ..utils.terminal import reset_screen
from ..config.labels import delden_labels
from ..config.config import (
    density_data_relpath, delden_relpath, delden_pred_str, delden_savename,
    delden_datafile, delden_xgb_obj, delden_cv_folds, term_width,
    delden_train_data, delden_test_data, delden_train_pred_data,
    delden_test_pred_data, delden_scores_data
)

class DelDensity:

    # CONSTRUCTOR
    def __init__(
    self, data_dir:Path = None, save_dir:Path = None, title:str = None,
    verbose:bool = True):
        '''
            Returns a new instance of class DelDensity
        '''
        if data_dir is None:
            self.data_dir = density_data_relpath
        else:
            self.data_dir = data_dir

        if save_dir is None:
            self.save_dir = delden_relpath
        else:
            self.save_dir = save_dir

        if title is None:
            title = 'MODEL'
        self.title = title

        self.exps = delden_exps['all']
        self.feats = delden_groups['all']
        self.pred_str = delden_pred_str
        self.verb = verbose

        self.reset()

        self.scores_cols = [
            "ITER", "TRAIN", "TEST", "√MSE TRAIN", "R² TRAIN", "√MSE TEST",
            "R² TEST"
        ]
        self.scores_fmt = ['d', 'd', 'd', '.4f', '.4f', '.4f', '.4f']

        self.imps_cols = ["FEATURE NAME", "ITER", "FEATURE INDEX", "IMPORTANCE"]
        self.imps_fmt = ['s', 'd', 'd', '.2f']

    # SETTERS
    def reset(self):
        '''
            Resets the DelDensity instance, and removes all training/testing
            results.  Does not affect system parameters, such as selected
            experiments, features, or training labels.
        '''
        self.is_trained = False
        self.scores_arr = []
        self.imps = [[]]
        self.y_train = []
        self.y_test = []
        self.y_train_pred = []
        self.y_test_pred = []
        self.r2_train = []
        self.rmse_train = []
        self.r2_test = []
        self.rmse_test = []
        self.best_models = []

    def set_experiments(self, *labels:Tuple[str]):
        '''
            Select the experiments whose data will be used for training.
        '''
        self.reset()
        exps = []
        for exp in labels:
            if exp in delden_exps.keys():
                exps.extend(delden_exps[exp])
            elif exp not in delden_exps['all']:
                msg = (
                    f'Unrecognized experiment `{exp}` passed to method '
                    f'`set_experiments`.'
                )
                raise ValueError(msg)
            else:
                exps.append(exp)
        self.exps = tuple(set(exps))

    def set_features(self, *labels:Tuple[str]):
        '''
            Select the features which will be included in the model.
        '''
        self.reset()
        self.feats = tuple(labels)
        for feature in self.feats:
            if feature not in delden_groups['all']:
                msg = (
                    f'Unrecognized feature `{feature}` passed to method '
                    f'`set_features`.'
                )
                raise ValueError(msg)

    def set_training_label(self, pred_str:str):
        '''
            Sets the column label on which the input data is trained.
        '''
        self.reset()
        self.pred_str = pred_str

    def set_verbose(self, state:bool):
        '''
            Sets the object verbosity: i.e. whether or not status updates are
            printed to the terminal.
        '''
        self.verb = state

    def set_data_directory(self, path:Path):
        '''
            Sets the directory from which to read the density data.
        '''
        self.reset()
        self.data_dir = path
        if not self.data_dir.is_dir():
            msg = f'Location `{self.data_dir:s}` is a non-existent directory.'
            raise IOError(msg)

    def set_save_directory(self, path:Path):
        '''
            Sets the directory into which results are stored.
        '''
        self.reset()
        self.save_dir = path
        if not self.save_dir.is_dir():
            msg = f'Location `{self.save_dir:s}` is a non-existent directory.'
            raise IOError(msg)

    # GETTERS
    @property
    def experiments(self) -> Tuple[str]:
        '''
            Returns the tuple of experiment labels.
        '''
        return self.exps

    @property
    def features(self) -> Tuple[str]:
        '''
            Returns the tuple of included features.
        '''
        return self.feats

    @property
    def training_label(self) -> str:
        '''
            Returns the column label on which the input data is trained.
        '''
        return self.pred_str

    @property
    def trained(self) -> bool:
        '''
            Returns whether or not the system has been trained to completion as
            a boolean.
        '''
        return self.is_trained

    @property
    def data_directory(self) -> Path:
        '''
            Returns the current data directory.
        '''
        return self.data_dir

    @property
    def save_directory(self) -> Path:
        '''
            Returns the current save directory.
        '''
        return self.save_dir

    @property
    def verbose(self) -> bool:
        '''
            Returns a boolean representing whether the instance is verbose.
        '''
        return self.verb

    @property
    def scores(self) -> np.ndarray:
        '''
            Returns an array of scores for each iteration of the training.
            Columns are defined as follows:

            iteration, training split, training, training RMSE, training R²,
            testing RMSE, testing R².
        '''
        return np.array(self.scores_arr)

    def __str__(self) -> str:
        '''
            Returns a string containing information about the given instance,
            such as the included experiments and features.  Also contains
            training/testing results if the model is trained/tested.
        '''

        out_str = self._str_features()

        if self.is_trained:
            out_str += '\n\n' + self._str_scores()
            out_str += '\n\n' + self._str_importances()

        return f'{self.title}\n\n{out_str}'

    # TRAINING
    def grid_search(
    self, itermax:int = 10, train_size:Tuple[float] = 0.8,
    objective:str = None, colsample_bytree:List[float] = None,
    alpha:List[float] = None, learning_rate:List[float] = None,
    n_estimators:List[float] = None, max_depth:List[float] = None,
    n_jobs:int = None, cv:int = None, log:bool = False):
        '''
            Performs a grid search over the given parameters:

                colsample_bytree
                alpha
                learning_rate
                n_estimators
                max_depth
        '''
        self.reset()
        if self.verb:
            reset_screen()
            print(self.__str__())

        if objective is None:
            objective = delden_xgb_obj

        if n_jobs is None:
            n_jobs = delden_n_jobs

        if cv is None:
            cv = delden_cv_folds

        estimator = xgb.XGBRegressor(objective = objective)

        param_grid = self._gridsearch_params(
            colsample_bytree, alpha, learning_rate, n_estimators, max_depth
        )

        for i in range(itermax):
            grid_search = GridSearchCV(
                estimator = estimator, param_grid = param_grid, cv = cv,
                n_jobs = n_jobs
            )

            X_train, X_test, y_train, y_test = \
            self._preprocess(train_size, log = log)

            grid_search.fit(X_train, y_train)
            best_estimator = grid_search.best_estimator_
            self.best_models.append(best_estimator)

            y_train_pred = best_estimator.predict(X_train)
            rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))
            r2_train = r2_score(y_train, y_train_pred)

            y_test_pred = best_estimator.predict(X_test)
            rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))
            r2_test = r2_score(y_test, y_test_pred)

            self.y_train.append(list(y_train))
            self.y_train_pred.append(list(y_train_pred))
            self.r2_train.append(r2_train)
            self.rmse_train.append(rmse_train)

            self.y_test.append(list(y_test))
            self.y_test_pred.append(list(y_test_pred))
            self.r2_test.append(r2_test)
            self.rmse_test.append(rmse_test)

            self.scores_arr.append([
                i, len(y_train), len(y_test), rmse_train, r2_train, rmse_test,
                r2_test
            ])

            imps = best_estimator.feature_importances_
            idx = np.arange(len(self.feats))
            imps = list(zip(self.feats, idx, imps))
            sorted_idx = np.argsort(np.array(imps)[:,2])[::-1]
            if self.imps[-1]:
                self.imps.append([])
            ignored = 0
            for j in sorted_idx:
                feat = imps[j]
                if feat[2] >= 1E-16:
                    self.imps[-1].append([feat[0], i, feat[1], feat[2]])
                else:
                    ignored += 1

            if self.verb:
                reset_screen()
                print(self.title, end = '\n\n')
                print(self._str_importances(ignored) + '\n')
                print(self._str_scores())

        self.is_trained = True

    def save(self, filename:str = None):
        '''
            Saves the results as a set of files, into a new directory.
        '''
        if not self.is_trained:
            msg = (
                'Attempting to save data from untrained model – run method '
                'DelDensity.grid_search() before attempting to save.'
            )
            raise RuntimeError(msg)

        if filename is None:
            filename = create_unique_name(prefix = delden_savename)
        save_path = self.save_dir / filename
        save_path.mkdir(exist_ok = True)

        summary_path = save_path / 'summary.txt'

        out_str = (
            f'Model Saved {datetime.now()}\n\n'
            f'EXPERIMENT FILES: {self._str_experiments()}\n\n'
            f'SCORES:\n{clean_str(self._str_scores())}\n\n'
            f'IMPORTANCES (VALUES OF ZERO OMITTED):'
        )

        for i in range(len(self.imps)):
            out_str += clean_str(f'\n{self._str_importances(idx = i)}')

        out_str += f'\n\nREFERENCE MATERIAL\n'
        out_str += f'{clean_str(clean_str(self._str_features()))}\n\n'

        with open(summary_path, 'w+') as outfile:
            outfile.write(out_str)

        y_train_path = save_path / delden_train_data
        y_test_path = save_path / delden_test_data

        y_train_pred_path = save_path / delden_train_pred_data
        y_test_pred_path = save_path / delden_test_pred_data

        scores_out_path = save_path / delden_scores_data

        with open(y_train_path, 'w+') as outfile:
            outfile.write(self._str_array_out(self.y_train))

        with open(y_test_path, 'w+') as outfile:
            outfile.write(self._str_array_out(self.y_test))

        with open(y_train_pred_path, 'w+') as outfile:
            outfile.write(self._str_array_out(self.y_train_pred))

        with open(y_test_pred_path, 'w+') as outfile:
            outfile.write(self._str_array_out(self.y_test_pred))

        with open(scores_out_path, 'w+') as outfile:
            outfile.write(self._str_scores_out())

    # PRIVATE METHODS
    @staticmethod
    def _read_data(data_path:Path) -> pd.DataFrame:
        '''
            Reads the data from the given file and returns a pandas dataframe.
            Also cleans the data and drops frames with NaN values.
        '''
        return pd.read_csv(data_path, delim_whitespace = True).dropna().copy()

    def _str_features(self, width:int = None) -> str:
        '''
            Returns information about the features being used in the model.
        '''
        if width is None:
            width = term_width
        sorted_feats = sorted(self.feats)
        string = map(delden_labels.get, sorted_feats)
        len_max = max(max(map(len, sorted_feats)), 9)
        string = (wrap(i, width - (len_max + 2)) for i in string)
        join_str = '\n' + ' '*(len_max+1)
        string = (join_str.join(i) for i in string)
        sorted_feats = (B(i) for i in sorted_feats)
        string = zip(sorted_feats, string)
        string = (f'{i[0]:{len_max+7}s} {I(i[1])}' for i in string)
        string = '\n'.join(string)
        title = f'{"FEATURES":{len_max}s} DEFINITIONS'
        title = B(title)
        string = f"{title}\n\n{string}"
        return string

    def _str_scores(self) -> str:
        '''
            Returns a string containing the scores on an iterative basis.
        '''

        return self._tabulate(
            self.scores_cols, self.scores_fmt, self.scores_arr
        )

    def _str_importances(self, ignored:int = 0, idx:int = -1) -> str:
        '''
            Returns a string containing information about feature importances.
        '''

        out_str = self._tabulate(self.imps_cols, self.imps_fmt, self.imps[idx])
        if ignored > 0:
            out_str += I(f'\n\tOmitted {ignored} features with zero importance')
        return out_str

    def _str_array_out(self, arr:np.ndarray) -> str:
        '''
            Formats a 2-D numpy array for saving to file.
        '''
        out = ''
        for row in arr:
            for i in row:
                out += f'{i:f},'
            out = out[:-1] + '\n'
        return out

    def _str_scores_out(self) -> str:
        '''
            Returns a string containing a table of score values.
            Columns are:

                R² Train, R² Test, RMSE Train, RMSE Test
        '''
        iterator = zip(
            self.r2_train, self.r2_test, self.rmse_train, self.rmse_test
        )
        out = ''
        for i,j,k,l in iterator:
            out += f'{i:f},{j:f},{k:f},{l:f}\n'
        return out[:-1]

    def _str_experiments(self) -> str:
        '''
            Lists the experiments being used as training/testing data.
        '''
        if len(self.exps) == 1:
            return f'{self.exps[0]}.'
        elif len(self.exps) == 2:
            return f'{self.exps[0]} and {self.exps[1]}.'
        else:
            out = ''
            for n, exp in enumerate(self.exps):
                out += f'{exp}'
                if n < len(self.exps)-2:
                    out += ', '
                elif n == len(self.exps)-2:
                    out += ', and '
                else:
                    out += '.'
            return out

    def _preprocess(
    self, train_size:int, log:bool = False) -> pd.DataFrame:
        '''
            Reads all experiment data and returns a set of scaled & split
            DataFrames.
        '''
        data = pd.DataFrame()
        for exp in self.exps:
            path = self.data_dir / delden_datafile.format(exp)
            df = self._read_data(path)
            # if log:
                # scaler = MinMaxScaler()
            # else:
                # scaler = RobustScaler()
            scaler = StandardScaler()
            data = data.append(df, ignore_index = True)
        # data[:] = scaler.fit_transform(data[:].values)
        X = np.array(data.drop(self.pred_str, axis = 1))
        X = scaler.fit_transform(X)

        y = np.array(data[self.pred_str])
        if log:
            X, y = self._logarithm(X, y)

        return train_test_split(X, y, train_size = train_size)

    def _logarithm(
    self, X:np.ndarray, y:np.ndarray) -> Tuple[np.ndarray]:
        '''
            Takes the training and testing sets, and converts all values to
            their logarithms.  NaN values are removed.
        '''
        idx = y >= 0

        X = X[idx,:]
        y = y[idx]

        y = np.log(y + 1E-16)

        return X, y

    def _gridsearch_params(
    self, colsample_bytree:List[float] = None, alpha:List[float] = None,
    learning_rate:List[float] = None, n_estimators:List[float] = None,
    max_depth:List[float] = None) -> Dict[str, List[float]]:
        '''
            Prepares the parameters for a gridsearch.
        '''
        parameters = xgb_def.copy()

        if colsample_bytree is not None:
            parameters['colsample_bytree'] = colsample_bytree

        if alpha is not None:
            parameters['alpha'] = alpha

        if learning_rate is not None:
            parameters['learning_rate'] = learning_rate

        if n_estimators is not None:
            parameters['n_estimators'] = n_estimators

        if max_depth is not None:
            parameters['max_depth'] = max_depth

        return parameters

    @staticmethod
    def _tabulate(cols:Tuple[str], fmt:Tuple[str], data:np.ndarray) -> str:
        '''
            Creates a table using the given column titles, column string
            formatting keys, and data.
        '''
        col_lens = tuple(map(len, cols))
        out_str = '\t' + B('  '.join(cols) + '\n')
        row_fmt = [f'{i}{j}' for i,j in zip(col_lens, fmt)]

        for row in data:
            out_list = [f'{i:<{j}}' for i,j in zip(row, row_fmt)]
            temp_str = I('  '.join(out_list) + '\n')
            out_str = out_str + '\t' + temp_str

        return out_str
