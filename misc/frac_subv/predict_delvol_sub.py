#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 14:52:17 2019

@author: mcbeck
"""

from sklearn.feature_selection import RFE
import statistics as stat
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import RobustScaler
import shap

import random
from datetime import datetime
random.seed(datetime.now())

# data from make_delvol_input.m

#e_strs = ['EALL_', 'ECRY_', 'EMA_']
e_strs = ['EALL_']
exps_all = ['M8_1', 'M8_2', 'MONZ3', 'MONZ4', 'MONZ5', 'WG01', 'WG02', 'WG04']

tit = 'pred_'

# how to split into training vs testing
split_str = 'rand' # rand, LR, TB, time

# 3D
dim_str = '3D_delvol'
#vols = [100, 200, 300]
#nos = [1000, 2000, 3000]
#vols = [300]
#nos = [1000, 2000, 3000]
# only one noise threshold and subvolume to get RFE and shap
nos = [3000] # 1000 or 3000 for RFE and shap
vols = [300] # 100 300 to run

# get RFE or shap values
# will change to true if length of vols>1
get_RFE = 0
get_shap = 0

features = ['dmin_min', 'dmin_25', 'dmin_50', 'dmin_75', 'dmin_max', 'th1_min', 'th1_25', 'th1_50', 'th1_75', 'th1_max', 'th3_min', 'th3_25', 'th3_50', 'th3_75', 'th3_max', 'l1_min', 'l1_25', 'l1_50', 'l1_75', 'l1_max', 'l3_min', 'l3_25', 'l3_50', 'l3_75', 'l3_max', 'ani_min', 'ani_25', 'ani_50', 'ani_75', 'ani_max', 'vol_min', 'vol_25', 'vol_50', 'vol_75', 'vol_max', 'dc_25', 'dc_50', 'dc_75', 'dc_max', 'tot_vol', 'rand']

numf = len(features)

fold = 'txts/inputs/'
out_str = fold.replace('inputs/', tit)

sub_str = ''
if len(vols)==1 and len(nos)==1:
    sub_str = '_n'+str(nos[0])+'_s'+str(vols[0])
    get_RFE = 0
    get_shap = 1

# predicting percent of failure stress
pred_str = 'delv50' # predict change in total volume delvtot or median delv50
#pred_str = 'delvtot'

print('predicting:', pred_str)

for e_str in e_strs:
    if 'ALL' in e_str:
        exps = ['M8_1', 'M8_2', 'MONZ3', 'MONZ4', 'MONZ5', 'WG01', 'WG02', 'WG04']
    elif 'CRY' in e_str:
        exps = ['MONZ3', 'MONZ4', 'MONZ5', 'WG01', 'WG02', 'WG04']
    elif 'EMA' in e_str:
        exps = ['M8_1', 'M8_2']
    elif e_str in exps_all:
            exps = [e_str]

    score_txt = out_str+e_str+pred_str+'_'+dim_str+sub_str+'_'+split_str+'_score.txt'
    pred_txt = score_txt.replace('score', 'preddist')
    imp_txt = score_txt.replace('score', 'imp')
    shap_txt = score_txt.replace('score', 'shap')
    recur_txt = score_txt.replace('score', 'recur')

    preds_str = "it vol noise is_test preds \n";
    score_str = "it vol noise num_train num_test rmse_train r2_train rmse_test r2_test \n";
    imp_str = "feat_str it vol noise feat_num feat_imp \n";
    shp_str = "feat_str it vol noise feat_num mean_shap \n";
    recur_str = "feat_str it vol noise feat_num recur_rank \n";

    print('writing scores to:', score_txt)

    for no in nos:
        for vol in vols:
            root = dim_str+'_a'+str(no)+'_subv'+str(vol)
            df_all = pd.DataFrame()
            ei= 0
            for exp in exps:
                print(exp)
                fname = fold+exp+'_'+root+'.txt'
                print('input file: ', fname)

                df_sm = pd.read_csv(fname, delim_whitespace=True)
                df = df_sm.dropna().copy()

                df_all = df_all.append(df, ignore_index = True)

            df_scale = df_all.copy()
            trans = RobustScaler()
            df_scale[features] = trans.fit_transform(df_scale[features].values)

            # remove outliers
            pred = df_scale[pred_str].values
            mid = stat.mean(pred)
            sig = stat.stdev(pred)

            lim_max = mid+2*sig
            lim_min = mid-2*sig

            p_inds = [1 if e<lim_max and e>lim_min else 0 for i, e in enumerate(pred)]

            df_scale["include"] = p_inds
            df_scale = df_scale[df_scale["include"]==1]
            print("limits of predictions", lim_min, lim_max)

            it=0
            while it<=0:

                # get the testing data
                # split into left and right sides
                if 'LR' in split_str:
                    vals = df_scale['x'].values
                    med = stat.mean(vals)
                    std = stat.stdev(vals)
                    split = med
                    print('separation of testing range:', round(split, 1))
                    print('x limits:', min(vals), max(vals))
                    inds = [1 if e>=split else 0 for i, e in enumerate(vals)]

                elif 'TB' in split_str:
                    print('splitting into top and bottom')
                    if '2d' in dim_str:
                        vals = df_scale['y'].values
                    else:
                        vals = df_scale['z'].values

                    med = stat.mean(vals)
                    split = med
                    print('separation of testing range:', round(split, 1))
                    print('limits:', min(vals), max(vals))
                    inds = [1 if e>=split else 0 for i, e in enumerate(vals)]

                elif 'time' in split_str:
                    # randomly select training and testing so that
                    # one time (scan) is in either training or testing
                    times = df_scale['sig_d'].values
                    timesu = set(times)
                    indt = np.random.uniform(0, 1, len(timesu)) <= .80

                    inds = [0 if e==1 else 0 for i, e in enumerate(times)]
                    ti=0
                    for time in times:
                        loc = list(timesu).index(time)
                        ib = indt[loc]
                        inds[ti] = ib
                        ti=ti+1

                elif 'rand' in split_str:
                    # split randomly
                    inds = np.random.uniform(0, 1, len(df_scale)) <= .80

                df_scale['is_train'] = inds
                train, test = df_scale[df_scale['is_train']==True], df_scale[df_scale['is_train']==False]

                x_train = train[features]
                y_train = train[pred_str]

                x_test = test[features]
                y_test = test[pred_str]

                ytrainu = set(y_train)
                ytestu = set(y_test)

                curr_tr = "%.0f %.0f %.0f %d " % (it, vol, no, 0)
                tr_str = ''
                for y in ytrainu:
                    tr_str = tr_str+str(round(y, 2))+' '

                curr_te = "%.0f %.0f %.0f %d " % (it, vol, no, 1)
                te_str = ''
                for y in ytestu:
                    te_str = te_str+str(round(y, 2))+' '

                preds_str = preds_str+"\n"+curr_tr+tr_str+"\n"+curr_te+te_str
                #print(preds_str)

                X = df_scale[features]
                y = df_scale[pred_str]

                n_train = len(y_train)
                n_test = len(y_test)
                rat = n_test/(n_train+n_test)
                print('# train, # test, test/(test+train):', n_train, n_test, round(rat, 2))

                # weighted features
                # add features to explain subsets of data
                data_dmatrix = xgb.DMatrix(data=X,label=y)

                # max_depth: Maximum depth of a tree.
                # Increasing this value will make the model more complex and more likely to overfit
                # colsample_bytree: subsample ratio of columns when constructing each tree
                # alpha: L1 regularization term on weights. Default=0
                # Increasing this value will make model more conservative
                # learning_rate, eta = Typical final values to be used: 0.01-0.2
                xgb_clf = xgb.XGBRegressor(objective ='reg:squarederror')
                #parameters = {'colsample_bytree':[0.7, 0.8, 0.9], 'alpha':[0, 3, 5],
                #      'learning_rate': [0.1, 0.2, 0.3],
                #      'n_estimators': [100, 200, 300], 'max_depth':[3, 4, 5, 6]}
                parameters = {'colsample_bytree':[0.8, 0.9], 'alpha':[3, 5],
                      'learning_rate': [0.1],
                      'n_estimators': [100, 200, 300], 'max_depth':[4, 5, 6]}
                grid_search = GridSearchCV(estimator=xgb_clf, param_grid=parameters, cv=10, n_jobs=-1)

                grid_search.fit(x_train, y_train)
                xg_reg = grid_search.best_estimator_

                preds = xg_reg.predict(x_test)
                preds_train = xg_reg.predict(x_train)

                rmse_train = np.sqrt(mean_squared_error(y_train, preds_train))
                rmse_test = np.sqrt(mean_squared_error(y_test, preds))

                r2_test = r2_score(y_test, preds)
                r2_train = r2_score(y_train, preds_train)

                curr_str = "%.0f %.0f %.0f %.0f %.0f %.2f %.2f %.2f %.2f \n" % (it, vol, no, n_train, n_test, rmse_train, r2_train, rmse_test, r2_test)
                score_str = score_str+curr_str
                print(score_str)

                # recurrsive feature elimation to find importance of features
                if get_RFE:
                    selector = RFE(xg_reg, 5, step=1)
                    selector = selector.fit(x_train, y_train)
                    ranks = selector.ranking_
                    ranktop = [numf-r for r in ranks]
                    recur = list(zip(features, ranktop, range(1, numf+1)))
                    recur.sort(key=lambda tup: tup[1], reverse=True)

                    recs = ""
                    for ft in recur:
                        recs = recs+ft[0]+" "+str(it)+" "+str(vol)+" "+str(no)+" "+str(ft[2])+" "+str(round(ft[1], 4))+"\n"

                    print(recs)
                    recur_str = recur_str+recs

                imps = xg_reg.feature_importances_
                imp = list(zip(features, imps, range(1, numf+1)))
                imp.sort(key=lambda tup: tup[1], reverse=True)

                fts = ""
                for ft in imp:
                    fts = fts+ft[0]+" "+str(it)+" "+str(vol)+" "+str(no)+" "+str(ft[2])+" "+str(round(ft[1], 4))+"\n"

                print(fts)
                imp_str = imp_str+fts

                if get_shap:
                    shap_vals = shap.TreeExplainer(xg_reg).shap_values(train[features])

                    shap.summary_plot(shap_vals, train[features], plot_type="bar")
                    shap_comb = shap_vals.transpose()

                    shap_mean = []
                    num_f = len(shap_comb)
                    for fi in range(len(shap_comb)):
                        vabs = abs(shap_comb[fi])
                        v_mean = stat.mean(vabs)
                        shap_mean.append(v_mean)

                    shapl = list(zip(features, shap_mean, range(1, numf+1)))
                    shapl.sort(key=lambda tup: tup[1], reverse=True)

                    shps = ""
                    for ft in shapl:
                        shps = shps+ft[0]+" "+str(it)+" "+str(vol)+" "+str(no)+" "+str(ft[2])+" "+str(round(ft[1], 4))+"\n"

                    print(shps)
                    shp_str = shp_str+shps

                it=it+1

    print(score_str)

    f= open(score_txt, "w")
    f.write(score_str)
    f.close()

    f= open(pred_txt, "w")
    f.write(preds_str)
    f.close()

    f= open(imp_txt, "w")
    f.write(imp_str)
    f.close()

    if get_RFE:
        f= open(recur_txt, "w")
        f.write(recur_str)
        f.close()
        print(recur_txt)

    if get_shap:
        print(shp_str)
        f= open(shap_txt, "w")
        f.write(shp_str)
        f.close()
        print(shap_txt)

    print(imp_txt)
    print(score_txt)
