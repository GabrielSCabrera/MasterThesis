#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:58:24 2020

@author: mcbeck
"""

import warnings

warnings.simplefilter(action = "ignore", category = Warning)

from datetime import datetime
import statistics as stat
import random

from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_squared_error
from sklearn.feature_selection import RFE
from sklearn.metrics import r2_score

import xgboost as xgb
import pandas as pd
import numpy as np
import shap

random.seed(datetime.now())

fold = "inputs/"

# predict the change in global density from one scan to the next
pred_str = "del_den"

exp1s = ["M8_1", "M8_2"]
exp2s = ["MONZ3", "MONZ4", "MONZ5"]
exp3s = ["WG01", "WG02", "WG04"]
exp4s = ["MONZ3", "MONZ4", "MONZ5", "WG01", "WG02", "WG04"]

expinds = ["M8_1", "M8_2", "MONZ3", "MONZ4", "MONZ5", "WG01", "WG02", "WG04"]

# nume = 3+len(expinds)
nume = 4


featcombins = ["all", "noglobden", "micro", "curr"]
for feat_str in featcombins:

    features = [
        "glob_den", "sigd", "ep", "del_f", "del_sig", "del_ep", "den_p10",
        "den_p20", "den_p30", "den_p40", "den_p50", "den_mean", "den_p60",
        "den_p70", "den_p80", "den_p90", "den_max", "den_sum", "den_std",
        "den_numloc", "den_volloc", "dist_p10", "dist_p20", "dist_p30",
        "dist_p40", "dist_p50", "dist_mean", "dist_p60", "dist_p70", "dist_p80",
        "dist_p90", "dist_max", "dist_sum", "dist_std", "c_20", "c_30", "c_40",
        "c_50", "c_60", "c_70", "c_80", "c_90", "c_100", "c_len",
    ]
    featinds = list(range(1, len(features) + 1))

    if "noglobden" in feat_str:
        features = [
            "sigd", "ep", "del_f", "del_sig", "del_ep", "den_p10", "den_p20",
            "den_p30", "den_p40", "den_p50", "den_mean", "den_p60", "den_p70",
            "den_p80", "den_p90", "den_max", "den_sum", "den_std", "den_numloc",
            "den_volloc", "dist_p10", "dist_p20", "dist_p30", "dist_p40",
            "dist_p50", "dist_mean", "dist_p60", "dist_p70", "dist_p80",
            "dist_p90", "dist_max", "dist_sum", "dist_std", "c_20", "c_30",
            "c_40", "c_50", "c_60", "c_70", "c_80", "c_90", "c_100", "c_len",
        ]
        del featinds[0]
    elif "micro" in feat_str:
        features = [
            "den_p10", "den_p20", "den_p30", "den_p40", "den_p50", "den_mean",
            "den_p60", "den_p70", "den_p80", "den_p90", "den_max", "den_sum",
            "den_std", "den_numloc", "den_volloc", "dist_p10", "dist_p20",
            "dist_p30", "dist_p40", "dist_p50", "dist_mean", "dist_p60",
            "dist_p70", "dist_p80", "dist_p90", "dist_max", "dist_sum",
            "dist_std", "c_20", "c_30", "c_40", "c_50", "c_60", "c_70", "c_80",
            "c_90", "c_100", "c_len",
        ]
        del featinds[0:6]
    elif "curr" in feat_str:
        features = [
            "glob_den", "sigd", "ep", "den_p10", "den_p20", "den_p30",
            "den_p40", "den_p50", "den_mean", "den_p60", "den_p70", "den_p80",
            "den_p90", "den_max", "den_sum", "den_std", "den_numloc",
            "den_volloc", "dist_p10", "dist_p20", "dist_p30", "dist_p40",
            "dist_p50", "dist_mean", "dist_p60", "dist_p70", "dist_p80",
            "dist_p90", "dist_max", "dist_sum", "dist_std", "c_20", "c_30",
            "c_40", "c_50", "c_60", "c_70", "c_80", "c_90", "c_100", "c_len",
        ]
        del featinds[3:6]

    numf = len(features)
    numi = len(featinds)

    print("# features, inds", numf, numi)

    score_txt = "outputs/pred_delden_allexp_" + feat_str + "_score.txt"
    score_str = "ei it num_train num_test rmse_train r2_train rmse_test r2_test \n"

    imp_txt = score_txt.replace("score", "imp")
    imp_str = "feat_str ei it feat_ind imp \n"

    ei = 1
    itmax = 10
    while ei <= nume:
        if ei == 1:
            exps = exp1s
        elif ei == 2:
            exps = exp2s
        elif ei == 3:
            exps = exp3s
        elif ei == 4:
            exps = exp4s
        elif ei > 4:
            exps = [expinds[ei - 4]]

        it = 0
        while it < itmax:
            df_all = pd.DataFrame()
            for exp in exps:
                print(exp)
                fname = fold + "damage_" + exp + "_s25.txt"
                print("input file: ", fname)

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
            print("# train, # test, test/(test+train):", n_train, n_test, round(rat, 2))

            X = df_all[features]
            y = df_all[pred_str]
            # weighted features
            # add features to explain subsets of data
            data_dmatrix = xgb.DMatrix(data=X, label=y)

            # max_depth: Maximum depth of a tree.
            # Increasing this value will make the model more complex and more likely to overfit
            # colsample_bytree: subsample ratio of columns when constructing each tree
            # alpha: L1 regularization term on weights. Default=0
            # Increasing this value will make model more conservative
            # learning_rate, eta = Typical final values to be used: 0.01-0.2
            xgb_clf = xgb.XGBRegressor(objective="reg:squarederror")
            # parameters = {'colsample_bytree':[0.7, 0.8, 0.9], 'alpha':[0, 3, 5],
            #              'learning_rate': [0.1, 0.2, 0.3],
            #              'n_estimators': [100, 200, 300], 'max_depth':[3, 4, 5, 6]}
            parameters = {
                "colsample_bytree": [0.8, 0.9],
                "alpha": [0, 3],
                "learning_rate": [0.1, 0.2],
                "n_estimators": [200, 300],
                "max_depth": [4, 5, 6],
            }
            grid_search = GridSearchCV(
                estimator=xgb_clf, param_grid=parameters, cv=10, n_jobs=-1
            )

            grid_search.fit(x_train, y_train)
            xg_reg = grid_search.best_estimator_

            preds = xg_reg.predict(x_test)
            preds_train = xg_reg.predict(x_train)

            rmse_train = np.sqrt(mean_squared_error(y_train, preds_train))
            rmse_test = np.sqrt(mean_squared_error(y_test, preds))

            r2_test = r2_score(y_test, preds)
            r2_train = r2_score(y_train, preds_train)

            curr_str = "%d %d %d %d %.4f %.4f %.4f %.4f \n" % (
                ei, it, n_train, n_test, rmse_train, r2_train, rmse_test,
                r2_test,
            )
            score_str = score_str + curr_str
            print(score_str)

            imps = xg_reg.feature_importances_
            imp = list(zip(features, featinds, imps))
            imp_rank = imp.copy()
            imp_rank.sort(key=lambda tup: tup[2], reverse=True)

            for ft in imp:
                curr_str = "%s %d %d %d %.2f \n" % (ft[0], ei, it, ft[1], ft[2])
                imp_str = imp_str + curr_str

            print(imp_rank[0:5])
            it = it + 1

        ei = ei + 1

    f = open(score_txt, "w")
    f.write(score_str)
    f.close()

    f = open(imp_txt, "w")
    f.write(imp_str)
    f.close()
