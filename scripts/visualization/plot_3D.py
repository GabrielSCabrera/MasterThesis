from mayavi import mlab
import numpy as np

import sys
sys.path.insert(0, '..')
from datasets import config

label = 'MONZ5'                  # Name of dataset
img_size = (1200, 1600)         # Saved image dimensions
break_point = 2                # Number of images to process (None)
mlab.options.offscreen = True   # Whether to hide the Mayavi UI

# Camera Position Settings (Use 'None' for default)
view_kwargs = {'azimuth'    :   90,
               'elevation'  :   70,
               'distance'   :   None,
               'focalpoint' :   None,
               'roll'       :   0,
               'reset_roll' :   True,
               'figure'     :   None}

"""Implementing Settings"""

dataset = config.bins[label]   # Initialize 'Binfo' instance
if break_point is None:
    break_point = len(dataset)+1
indices = np.arange(0, len(dataset))[:break_point]
if len(indices) > break_point:
    np.delete(indices[4])

f = mlab.figure(size = img_size, bgcolor = (1,1,1))

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
    mlab.savefig(f"../../results/img_3D/{label}_MPa_{pressure:02.1f}.png")
    print(f"\rRendering {int(100*(n+1)/len(indices)):2d}%", end = "")
print()
