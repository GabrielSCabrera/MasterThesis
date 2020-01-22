#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 14:52:17 2019

@author: mcbeck
"""

import statistics as stat
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import RobustScaler
import matplotlib.pyplot as plt
import shap

import random
from datetime import datetime
random.seed(datetime.now())

# 3D data
# predict failure in individual experiments
exps = ['M8_1', 'M8_2', 'MONZ5', 'WG04']

# dimensions, slice increment, noise thresholds
# 3D fracture data
nois = [2000, 2000, 2000, 2000] # noise thresholds
#nois = [2000, 2000, 1000, 1000] 
meds_vert = [200, 200, 200, 200] # vertical coordinate to split on
dim = '3D' # data with 3 dimensions
mstr = ''
lim = 1 # M8s are better with full range, monz5 and wg better with smaller range

# 2D fracture data
# made in extract_feat_frac_2D_vert.m
#nois = [200, 200, 200, 200] # noise thresholds
#meds_vert = [200, 400, 400, 200] # vertical coordinate to split on
#meds = [300, 300, 300, 300] # horizontal (x) coordinate to split on
#dim = '2d_vert' # data taken from 2d slices
##mstr = 'm10_'
#mstr = 'm1_' # 'm10_' frequency of slices
#lim = 1 # 0.5, 1

# how to split into training and testing
#split_str = 'PERP' # perpendicular slices (only for 2D)
split_str = 'LR' # left and right sides
#split_str = 'TB' # top and bottom
#split_str = 'rand' # random

# rmse < 0.1 (bad rmse>0.5)
# r2>0.6 ok, r2 > 0.8 very good

fold = 'txts/inputs/'
out_str = fold.replace('inputs/', 'pred')
score_txt = out_str+'_frac_'+dim+'_'+mstr+'score_'+split_str+'_lim'+str(lim)+'.txt'
imp_txt = score_txt.replace('score', 'imp')
shap_txt = score_txt.replace('score', 'shap')

score_str = "exp lim num_train num_test rmse_train r2_train rmse_test r2_test \n";
imp_str = "feat_str exp lim feat_num feat_imp \n";
shp_str = "feat_str exp lim feat_num mean_shap \n";

print('writing scores to:', score_txt)

# in 3D
# axial stress, distance from failure
#'sig', 'sig_d', 'cx', 'cy', 'cz' plus the features   
# in 2D
# sig sig_d slice mx cx cy plus the features
features = ['area', 'theta', 'lmin', 'lmax', 'aniso', 'dcmin', 'dc5', 'dc10', 'dc25', 'dc50', 'dc75']
numf = len(features)

# predicting percent of failure stress
pred_str = 'sig_d'

ei=0
for exp in exps:
    print(exp)
    a = nois[ei]
    fname = fold+exp+'_'+dim+'_frac_full_'+mstr+'a'+str(a)+'.txt'
    print('input file: ', fname)
        
    df_sm = pd.read_csv(fname, delim_whitespace=True)  
    df_scale = df_sm.dropna().copy()
    
    trans = RobustScaler()# works better with outliers
    df_scale[features] = trans.fit_transform(df_scale[features].values)  
    
    #df_scale = df_scale[df_scale[pred_str]<lim]
    
    # only take values within center of rock
    vals = df_scale['cx'].values
    mid = stat.mean(vals)
    stdx = stat.stdev(vals)
    #x0 = mid-(0.5*stdx)
    #x1 = mid+(0.5*stdx)
    x0 = mid-(stdx)
    x1 = mid+(stdx)
    print("limiting to x range:", round(x0), round(x1))

    df_scale = df_scale[df_scale['cx']>x0]
    df_scale = df_scale[df_scale['cx']<x1]
    
    # separate training and testing into left and right sides of sample
    if 'LR' in split_str:
        print('splitting into left and right sides')
        vals = df_scale['cx'].values
        mid_split = mid-(stdx/2)
        
        print('separation of testing range:', mid_split)
        print('x limits:', min(vals), max(vals))
        
        inds = [1 if e>=mid_split else 0 for i, e in enumerate(vals)]    
    
    # split top to bottom
    elif 'TB' in split_str:
        print('splitting into top and bottom')
        if '2d' in dim:
            vals = df_scale['cy'].values
        else:
            vals = df_scale['cz'].values
            
        mid = stat.mean(vals) 
        stdv = stat.stdev(vals)
        mid_split = mid-(stdv/2)
        print('separation of testing range:', mid_split)
        print('verical limits:', min(vals), max(vals))
        
        inds = [1 if e>=mid_split else 0 for i, e in enumerate(vals)]      
    # perpendicualr 
    elif 'PERP' in split_str:
        print("splitting into perpendicular slices")
        vals = df_scale['slice'].values
        inds = [1 if e==1 else 0 for i, e in enumerate(vals)] 
            
    # random
    else:
        print('splitting randomly 20/80')
        inds = np.random.uniform(0, 1, len(df_scale)) <= .80
    
    
    #dist_perc = df_scale['sig_d']
#    plt.figure(3)
#    plt.plot(dists, sigs, 'ko')
#    plt.xlabel('norm stress distance')
#    plt.ylabel('stress')
    
    df_scale['is_train'] = inds
    train, test = df_scale[df_scale['is_train']==True], df_scale[df_scale['is_train']==False]
    
    sig_dists = df_scale[pred_str].values
    print("range of stress distances:", round(min(sig_dists), 3), round(max(sig_dists), 3))
    
    x_train = train[features]
    y_train = train[pred_str]
    
    # only remove values from testing with the limit?
    
    x_test = test[features]
    y_test = test[pred_str]
    
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
    parameters = {'colsample_bytree':[0.9], 'alpha':[5], 'learning_rate': [0.1],
                  'n_estimators': [50, 100, 200], 'max_depth':[3, 5, 7]}
    grid_search = GridSearchCV(estimator=xgb_clf, param_grid=parameters, cv=10, n_jobs=-1)
    
    grid_search.fit(x_train, y_train)
    xg_reg = grid_search.best_estimator_
    
    preds = xg_reg.predict(x_test)
    preds_train = xg_reg.predict(x_train)
    
    rmse_train = np.sqrt(mean_squared_error(y_train, preds_train))
    rmse_test = np.sqrt(mean_squared_error(y_test, preds))
    
    r2_test = r2_score(y_test, preds)
    r2_train = r2_score(y_train, preds_train)
    
    curr_str = "%.0f %.2f %.0f %.0f %.2f %.2f %.2f %.2f \n" % (ei, lim, n_train, n_test, rmse_train, r2_train, rmse_test, r2_test)
    score_str = score_str+curr_str
    print(score_str)
    
    # plot predicted vs observed
    plt.figure(1)
    plt.plot(y_test, preds, 'ko')
    plt.plot([0, max(y_test)], [0, max(preds)], 'r-')
    plt.ylabel('predicted')
    plt.xlabel('observed')
    plt.title('testing')
    plt.show()
    
    plt.figure(2)
    plt.plot(y_train, preds_train, 'ko')
    plt.plot([0, max(y_train)], [0, max(preds_train)], 'r-')
    plt.ylabel('predicted')
    plt.xlabel('observed')
    plt.title('training')
    plt.show()

    imps = xg_reg.feature_importances_
    imp = list(zip(features, imps, range(1, numf+1)))
    imp.sort(key=lambda tup: tup[1], reverse=True)
    
#    plt.figure(3)
#    plt.barh(range(len(imps)), imps.sort(key=lambda tup: tup[0], reverse=True), color='b', align='center')
#    plt.yticks(range(len(imps)), [features[i] for i in imps])
#    plt.xlabel('Relative Importance')
#    plt.show()
    
    fts = ""
    for ft in imp:
        fts = fts+ft[0]+" "+str(ei)+" "+str(lim)+" "+str(ft[2])+" "+str(round(ft[1], 4))+"\n"
    
    print(fts)
    imp_str = imp_str+fts
    
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
        shps = shps+ft[0]+" "+str(ei)+" "+str(lim)+" "+str(ft[2])+" "+str(round(ft[1], 4))+"\n"
    
    print(shps)
    shp_str = shp_str+fts
    
    
    ei=ei+1

print(score_str)

f= open(score_txt, "w")
f.write(score_str)
f.close()

print(imp_str)

f= open(imp_txt, "w")
f.write(imp_str)
f.close()

            
print(shp_str)
f= open(shap_txt, "w")
f.write(shp_str)
f.close()

print(imp_txt)
print(score_txt)
print(shap_txt)

