from binfo import Binfo

bins_relpath = '../../data/bins_extracted/'

bin_dirs = {'M8_1'  :   bins_relpath + 'M8_1_bins/',
            'M8_2'  :   bins_relpath + 'M8_2_bins/',
            'MONZ5' :   bins_relpath + 'MONZ5_bins/',
            'WG04'  :   bins_relpath + 'WG04_bins/'}

bin_dims = {'M8_1'  :   (1000, 1000, 1200),
            'M8_2'  :   (900, 900, 1200),
            'MONZ5' :   (800, 800, 1200),
            'WG04'  :   (800, 800, 1200)}

bins = {'M8_1':Binfo('M8_1', bin_dirs['M8_1'], bin_dims['M8_1'])}

# Initializing Binfo object for M8_1 dataset
bins['M8_1'].get_frames()
#rn = 1000
#cn = 1000
#sn = 1200
