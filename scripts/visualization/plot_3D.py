from mayavi import mlab
import numpy as np
import os

import sys
sys.path.insert(0, '..')
from datasets import config

labels = ['M8_1', 'M8_2', 'MONZ5', 'WG04']  # Names of datasets
img_size = (1200, 1600)                     # Saved image dimensions
break_point = 3                             # Number of images to process
mlab.options.offscreen = True               # Whether to hide the Mayavi UI

# Camera Position Settings (Use 'None' for default)
view_kwargs = {'azimuth'    :   90,
               'elevation'  :   70,
               'distance'   :   None,
               'focalpoint' :   None,
               'roll'       :   0,
               'reset_roll' :   True,
               'figure'     :   None}

"""Functions"""

def plot_circles(dataset):
    x0, y0, z0 = dataset.dims

    x0 /= 2
    y0 /= 2

    r = np.sqrt(x0**2 + y0**2)/2
    t = np.linspace(0, 2*np.pi, 100)

    x1 = r*np.cos(t) + x0
    y1 = r*np.sin(t) + y0
    z1 = np.zeros_like(t)

    x2 = r*np.cos(t) + x0
    y2 = r*np.sin(t) + y0
    z2 = np.ones_like(t)*z0

    mlab.plot3d(x1, y1, z1, representation = 'wireframe', color = (0.2, 0.2, 1))
    mlab.plot3d(x2, y2, z2, representation = 'wireframe', color = (0.2, 0.2, 1))

def init_dataset(label, break_point):
    dataset = config.bins[label]   # Initialize 'Binfo' instance
    if break_point is None:
        break_point = len(dataset)+1
    indices = np.arange(0, len(dataset))[:break_point]

def generate_save_imgs(dataset, img_size):
    f = mlab.figure(size = img_size, bgcolor = (1,1,1))

    plot_circles(dataset)
    mlab.view(**view_kwargs)

    print("Rendering 0%", end = "")

    for n, data in enumerate(dataset.iter_ones(indices)):
        if n == 0:
            points = mlab.points3d(data[0], data[1], data[2], mode = "cube",
                                   color = (0.2, 0.2, 1), scale_factor = 1,
                                   line_width = 5)
        else:
            points.mlab_source.reset(x = data[0], y = data[1], z = data[2])
        pressure = float(dataset.pressures[indices[n]])
        savename = f"../../results/img_3D/{label}_{n+1:02d}_MPa_{pressure:03.1f}.png"
        mlab.savefig(savename)
        print(f"\rRendering {int(100*(n+1)/len(indices)):2d}%", end = "")
    print()

"""Main Code"""

for label in labels:
    dataset = init_dataset(label, break_point)
    generate_save_imgs(dataset)
