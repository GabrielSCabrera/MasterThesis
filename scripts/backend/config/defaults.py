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
