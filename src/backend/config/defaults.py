'''
    Default configurations for the main script
'''
from .config import bins

split_defaults = {
    'dataset'     :   bins['M8_1'],
    'splits'      :   None,
    'mode'        :   'slice',
    'test_size'   :   0.25,
    'limit'       :   1,
    'shuffle'     :   True
}

delden_xgb_gridsearch_defaults = {
    "colsample_bytree": [0.8, 0.9],
    "alpha":            [0, 3],
    "learning_rate":    [0.1, 0.2],
    "n_estimators":     [200, 300],
    "max_depth":        [4, 5, 6]
}
