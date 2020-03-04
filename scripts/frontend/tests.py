import numpy as np
from ..backend import *
from .visualization import *

def test_plot_2D():

    for label in config.labels:

        params = {
                  'label'       :   label,
                  # Saved image resolution (dpi)
                  'img_dpi'     :   300,
                  # Depth of image slice (from 0 to 1)
                  'save_dir'    :   config.plot_2D_relpath,
                  'y_depth_ratio' :  0.5
                 }

        savenames = plot_2D.generate_save_imgs(**params)

        params = {
                  'savenames'   :   savenames,
                  'save_dir'    :   config.plot_2D_relpath,
                  'label'       :   label
                 }

        plot_2D.create_gif(**params)

def test_plot_3D():
    # Camera Position Settings (Use 'None' for default)
    view_kwargs = {'azimuth'    :   90,
                   'elevation'  :   70,
                   'distance'   :   None,
                   'focalpoint' :   None,
                   'roll'       :   0,
                   'reset_roll' :   True,
                   'figure'     :   None}

    for label in config.labels:

        params = {
                  'label'       :   label,
                  # Saved image dimensions (px, px)
                  'img_size'    :   (1200, 1600),
                  'save_dir'    :   config.plot_3D_relpath,
                  'view_kwargs' :   view_kwargs
                 }

        savenames = plot_3D.generate_save_imgs(**params)

        params = {
                  'savenames'   :   savenames,
                  'save_dir'    :   config.plot_3D_relpath,
                  'label'       :   label
                 }

        plot_3D.create_gif(**params)

def test_split_2D():

    label = 'M8_1'

    params = {
              'dataset'     :   config.bins[label],
              'splits'      :   100,
              'mode'        :   'col',
              'test_size'   :   0.25,
              'limit'       :   0.1,
              'shuffle'     :   True
             }

    label += '_2D_' + params['mode']

    X_train, X_test, y_train, y_test = split_2D.test_train_split(**params)

    print('Pre-Saving Shapes:', end = '\n\t')
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    print('Pre-Saving Ones:', end = '\n\t')
    print(np.sum(X_train), np.sum(X_test), np.sum(y_train), np.sum(y_test))

    file_io.save_split(label, X_train, X_test, y_train, y_test)
    del X_train; del X_test; del y_train; del y_test

    X_train, X_test, y_train, y_test = file_io.load_split(label)

    print('Post-Loading Shapes:', end = '\n\t')
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    print('Post-Loading Ones:', end = '\n\t')
    print(np.sum(X_train), np.sum(X_test), np.sum(y_train), np.sum(y_test))

def test_split_3D():

    label = 'M8_1'

    params = {
              'dataset'     :   config.bins[label],
              'splits'      :   128,
              'mode'        :   'col',
              'test_size'   :   0.25,
              'limit'       :   0.1,
              'shuffle'     :   True
             }

    label += '_3D_' + params['mode']

    X_train, X_test, y_train, y_test = split_3D.test_train_split(**params)

    print('Pre-Saving Shapes:', end = '\n\t')
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    print('Pre-Saving Ones:', end = '\n\t')
    print(np.sum(X_train), np.sum(X_test), np.sum(y_train), np.sum(y_test))

    file_io.save_split(label, X_train, X_test, y_train, y_test)
    del X_train; del X_test; del y_train; del y_test

    X_train, X_test, y_train, y_test = file_io.load_split(label)

    print('Post-Loading Shapes:', end = '\n\t')
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    print('Post-Loading Ones:', end = '\n\t')
    print(np.sum(X_train), np.sum(X_test), np.sum(y_train), np.sum(y_test))

def run_tests():
    test_plot_2D()
    test_plot_3D()
    test_split_2D()
    test_split_3D()
