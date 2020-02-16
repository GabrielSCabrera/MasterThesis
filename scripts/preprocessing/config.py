from binfo import Binfo
import numpy as np

bins_relpath = '../../data/bins/'

bin_dirs = {'M8_1'  :   f'{bins_relpath}M8_1_bins',
            'M8_2'  :   f'{bins_relpath}M8_2_bins',
            'MONZ5' :   f'{bins_relpath}MONZ5_bins',
            'WG04'  :   f'{bins_relpath}WG04_bins'}

bin_dims = {'M8_1'  :   (1000, 1000, 1200),
            'M8_2'  :   (900,  900,  1200),
            'MONZ5' :   (800,  800,  1200),
            'WG04'  :   (800,  800,  1200)}

bins = {}
bins['M8_1']    =   Binfo('M8_1',     bin_dirs['M8_1'],   bin_dims['M8_1'])
bins['M8_2']    =   Binfo('M8_2',     bin_dirs['M8_2'],   bin_dims['M8_2'])
bins['MONZ5']   =   Binfo('MONZ5',    bin_dirs['MONZ5'],  bin_dims['MONZ5'])
bins['WG04']    =   Binfo('WG04',     bin_dirs['WG04'],   bin_dims['WG04'])

bin_stresses = {}
bin_stresses['M8_1'] = np.concatenate([np.arange(26,82,4), np.arange(80,120,2),
                       np.arange(122,132,2)])

bin_stresses['M8_2'] = np.concatenate([np.arange(152,186), np.arange(187,197)])

bin_stresses['MONZ5'] = np.concatenate([[2, 5], np.arange(30,45,5),
                        np.arange(40,90,5), np.arange(92,132,2),
                        np.arange(131,150), np.arange(150.5,162,0.5)])

bin_stresses['WG04'] = np.concatenate([[15], np.arange(15,100,5),
                       np.arange(95,115,5), np.arange(112,142,2), [141],
                       np.arange(144,149), [148.5, 149, 142, 143, 149.5, 149.5,
                       150, 150.5, 151, 151.5, 152, 152.5]])

bin_fail_times = {}
bin_fail_times['M8_1'] = np.arange(0, len(bin_stresses['M8_1']))[::-1] + 1
bin_fail_times['M8_2'] = np.arange(0, len(bin_stresses['M8_2']))[::-1] + 1
bin_fail_times['MONZ5'] = np.arange(0, len(bin_stresses['MONZ5']))[::-1] + 1
bin_fail_times['WG04'] = np.arange(0, len(bin_stresses['WG04']))[::-1] + 1
