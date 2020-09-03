"""
Created on Thu May  7 16:58:24 2020

@author: mcbeck
"""

"FEATURE IMPORTANCE"
"RECURSIVE FEATURE ELIMINATION"
"SHAP VALUE"

from typing import List, Tuple
from pathlib import Path
import warnings

from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import xgboost as xgb
import pandas as pd
import numpy as np

from ..utils.format import B, I, clean_str
from ..config.groups import delden_groups, delden_exps
from ..config.labels import delden_labels
from ..config.config import (
    density_data_relpath, delden_relpath, delden_pred_str, delden_savename
)

warnings.simplefilter(action = "ignore", category = Warning)

def train(
features:List[str], label:str, exps:List[str], itmax:int = 10,
pred_str:str = "del_den", directory:Path = None):

    output_file = "outputs/pred_delden_" + label + "_score.txt"
    score_list = [
        "ITER", "TRAIN", "TEST", "√MSE TRAIN", "R² TRAIN", "√MSE TEST",
        "R² TEST"
    ]
    score_lens = list(map(len, score_list))
    score_str = B('  '.join(score_list) + '\n')

    imp_list = ["FEATURE NAME", "ITER", "FEATURE INDEX", "IMPORTANCE"]
    imp_lens = list(map(len, imp_list))
    imp_str = B('  '.join(imp_list) + '\n')

    it = 0
    while it < itmax:

        df_all = pd.DataFrame()
        iter_title = (
            f" {B('EXPERIMENT')} {I(label)} {B('ITERATION')} {it} "
        )
        out_str = '\t' + iter_title.center(70, '–').center(76) + '\n\n'
        for exp in exps:
            fname = fold + "damage_" + exp + "_s25.txt"
            out_str += f"\t{B(f'INPUT FILE WITH {exp} DATA')}: "
            out_str += I(fname) + '\n'

            df_sm = pd.read_csv(fname, delim_whitespace=True)
            df = df_sm.dropna().copy()
            trans = RobustScaler()

            df[features] = trans.fit_transform(df[features].values)
            df_all = df_all.append(df, ignore_index=True)
            # df_all = df.copy()

        # random split train/test
        inds = np.random.uniform(0, 1, len(df_all)) <= 0.80

        df_all["is_train"] = inds
        train, test = (
            df_all[df_all["is_train"] == True],
            df_all[df_all["is_train"] == False],
        )

        x_train = train[features]
        y_train = train[pred_str]

        x_test = test[features]
        y_test = test[pred_str]

        n_train = len(y_train)
        n_test = len(y_test)
        rat = n_test / (n_train + n_test)

        # X = df_all[features]
        # y = df_all[pred_str]
        # weighted features
        # add features to explain subsets of data
        # data_dmatrix = xgb.DMatrix(data=X, label=y)

        # max_depth: Maximum depth of a tree.
        # Increasing this value will make the model more complex and more likely to overfit
        # colsample_bytree: subsample ratio of columns when constructing each tree
        # alpha: L1 regularization term on weights. Default=0
        # Increasing this value will make model more conservative
        # learning_rate, eta = Typical final values to be used: 0.01-0.2
        xgb_clf = xgb.XGBRegressor(objective="reg:squarederror")
        # parameters = {
        #     'colsample_bytree': [0.7, 0.8, 0.9],
        #     'alpha':            [0, 3, 5],
        #     'learning_rate':    [0.1, 0.2, 0.3],
        #     'n_estimators':     [100, 200, 300],
        #     'max_depth':        [3, 4, 5, 6]
        # }
        parameters = {
            "colsample_bytree": [0.8, 0.9],
            "alpha":            [0, 3],
            "learning_rate":    [0.1, 0.2],
            "n_estimators":     [200, 300],
            "max_depth":        [4, 5, 6],
        }
        grid_search = GridSearchCV(
            estimator = xgb_clf, param_grid = parameters, cv = 10, n_jobs = -1
        )

        grid_search.fit(x_train, y_train)
        xg_reg = grid_search.best_estimator_

        preds = xg_reg.predict(x_test)
        preds_train = xg_reg.predict(x_train)

        rmse_train = np.sqrt(mean_squared_error(y_train, preds_train))
        rmse_test = np.sqrt(mean_squared_error(y_test, preds))

        r2_test = r2_score(y_test, preds)
        r2_train = r2_score(y_train, preds_train)

        curr_str = (
            f"{it:d} {n_train:d} {n_test:d} {rmse_train:.4f} {r2_train:.4f} "
            f"{rmse_test:.4f} {r2_test:.4f}\n"
        )

        curr_list = [
            it, n_train, n_test, rmse_train, r2_train, rmse_test,
            r2_test
        ]

        curr_fmt = ['d', 'd', 'd', '.4f', '.4f', '.4f', '.4f']
        curr_fmt = [f'{i}{j}' for i,j in zip(score_lens, curr_fmt)]

        curr_list = [f'{i:<{j}}' for i,j in zip(curr_list, curr_fmt)]

        curr_str = I('  '.join(curr_list) + '\n')

        score_str = score_str + '\t' + curr_str
        out_str += '\n\t' + score_str + '\n'

        imps = xg_reg.feature_importances_
        imp = list(zip(features, featinds, imps))
        imp_rank = imp.copy()
        imp_rank.sort(key = lambda tup: tup[2], reverse = True)

        imp_fmt = []

        sorted_idx = np.argsort(np.array(imp)[:,2])[::-1]

        temp_str = imp_str
        for i in sorted_idx:
            ft = imp[i]
            if ft[2] == 0:
                break
            curr_list = [ft[0], it, ft[1], ft[2]]
            curr_str = f"{ft[0]:s} {it:d} {ft[1]:d} {ft[2]:.2f}\n"
            curr_fmt = ['s', 'd', 'd', '.2f']
            curr_fmt = [f'{i}{j}' for i,j in zip(imp_lens, curr_fmt)]
            curr_list = [f'{i:<{j}}' for i,j in zip(curr_list, curr_fmt)]
            curr_str = I('  '.join(curr_list) + '\n')
            temp_str += '\t' + curr_str

        out_str += '\t' + temp_str
        print('\033[3J\033[2J\033[H', end = '')
        print(out_str)
        it += 1

    f = open(output_file, "w")
    f.write(clean_str(score_str))
    f.close()

fold = "inputs/"

# predict the change in global density from one scan to the next

exp1s = ["M8_1", "M8_2"]
exp2s = ["MONZ3", "MONZ4", "MONZ5"]
exp3s = ["WG01", "WG02", "WG04"]
exp4s = ["MONZ3", "MONZ4", "MONZ5", "WG01", "WG02", "WG04"]

expinds = ["M8_1", "M8_2", "MONZ3", "MONZ4", "MONZ5", "WG01", "WG02", "WG04"]

feature_labels = ['full', 'noglobden', 'micro', 'curr']

for label in feature_labels:
    train(delden_groups[label], label, exp1s)
