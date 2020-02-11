from .binfo import Binfo

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
