'''
    Default configurations for the main script
'''

delden_xgb_gridsearch_defaults = {
    "colsample_bytree": [0.8, 0.9],
    "alpha":            [0, 3],
    "learning_rate":    [0.1, 0.2],
    "n_estimators":     [200, 300],
    "max_depth":        [4, 5, 6]
}
