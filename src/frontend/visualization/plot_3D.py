# from mayavi import mlab
import numpy as np
import imageio
import os

from ...backend import config

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

def generate_save_imgs(label, img_size, save_dir, view_kwargs):

    dataset = config.bins[label]   # Initialize 'Binfo' instance

    mlab.options.offscreen = True               # Whether to hide the Mayavi UI

    f = mlab.figure(size = img_size, bgcolor = (1,1,1))


    plot_circles(dataset)
    mlab.view(**view_kwargs)

    print("Rendering 0%", end = "")

    savenames = []
    for n, data in enumerate(dataset.iter_ones()):
        try:
            if n == 0:
                points = mlab.points3d(data[0], data[1], data[2], mode = "cube",
                                       color = (0.2, 0.2, 1), scale_factor = 1,
                                       line_width = 5)
            else:
                points.mlab_source.reset(x = data[0], y = data[1], z = data[2])
            pressure = float(dataset.pressures[n])
            savename = f"{save_dir}{label}_{n+1:02d}_MPa_{pressure:03.1f}.png"
            mlab.savefig(savename)
            print(f"\rRendering {int(100*(n+1)/(len(dataset)-1)):2d}%", end = "")
            savenames.append(savename)
        except MemoryError:
            perc = int(100*(n+1)/(len(dataset)-1))
            msg = f'\rCaught MemoryError, rendering interrupted (at {perc:2d}%)'
            print(msg)
            break
    print()
    return savenames

def create_gif(savenames, save_dir, label):
    images = []
    for filename in savenames:
        images.append(imageio.imread(filename))
    imageio.mimsave(f'{save_dir}{label}.gif', images, duration = 0.25)
