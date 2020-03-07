from .binfo import Binfo
import numpy as np
import os

seed = 1337

np.random.seed(seed)

storage_path = os.path.expanduser("~") + '/Documents/MasterThesis/'

data_path           =   storage_path  + 'data/'
results_path        =   storage_path  + 'results/'

bins_relpath        =   data_path     + 'bins/'
split_bins_relpath  =   data_path     + 'split_bins/'
DNN_models_relpath  =   data_path     + 'DNN_models/'

plot_2D_relpath     =   results_path  + 'img_2D/'
plot_3D_relpath     =   results_path  + 'img_3D/'

DNN_model_extension     =   '.dnn'

if not os.path.isdir(bins_relpath):
    msg = ('Missing required directory: \'/Documents/MasterThesis/data/bins/\''
          f'.  Dataset required in this location.')
    raise IOError(msg)

if not os.path.isdir(results_path):
    os.mkdir(results_path)

if not os.path.isdir(split_bins_relpath):
    os.mkdir(split_bins_relpath)

if not os.path.isdir(DNN_models_relpath):
    os.mkdir(DNN_models_relpath)

if not os.path.isdir(plot_2D_relpath):
    os.mkdir(plot_2D_relpath)

if not os.path.isdir(plot_3D_relpath):
    os.mkdir(plot_3D_relpath)

labels = ['M8_1', 'M8_2', 'MONZ5', 'WG04']  # Names of datasets

bin_dirs = {
            'M8_1'  :   f'{bins_relpath}M8_1_bins',
            'M8_2'  :   f'{bins_relpath}M8_2_bins',
            'MONZ5' :   f'{bins_relpath}MONZ5_bins',
            'WG04'  :   f'{bins_relpath}WG04_bins'
           }

bin_dims = {
            'M8_1'  :   (1000, 1000, 1200),
            'M8_2'  :   (900,  900,  1200),
            'MONZ5' :   (800,  800,  1200),
            'WG04'  :   (800,  800,  1200)
           }

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

bins = {}
for l in labels:
    bins[l] = Binfo(l, bin_dirs[l], bin_dims[l], bin_stresses[l])
