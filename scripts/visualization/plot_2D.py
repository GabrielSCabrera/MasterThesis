from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os

import sys
sys.path.insert(0, '..')
from datasets import config

labels = ['M8_1', 'M8_2', 'MONZ5', 'WG04']  # Names of datasets
img_dpi = 300                               # Saved image resolution (dpi)
y_depth_ratio = 0.5                         # Depth of image slice (from 0 to 1)
save_dir = '../../results/img_2D/'          # Where to save the images

"""Functions"""

def generate_save_imgs(label, img_dpi, y_depth_ratio, save_dir):
    dataset = config.bins[label]   # Initialize 'Binfo' instance
    stresses = config.bin_stresses[label]
    points = np.arange(1,len(stresses)+1,1)

    x0, y0, z0 = dataset.dims
    depth = int(y0*y_depth_ratio)
    savenames = []

    print("Rendering 0%", end = "")
    for n, data in enumerate(dataset):
        data = data[:,depth]

        fig, ax = plt.subplots(1,2)
        plt.tight_layout(pad = 2.0)

        im = ax[0].imshow(data.T, aspect="auto", interpolation='none')
        colors = [im.cmap(im.norm(0)), im.cmap(im.norm(1))]
        patches = [Patch(color=colors[0], label="Solid"),
                   Patch(color=colors[1], label="Fracture")]
        ax[0].set_xlabel('Core Sample $x$-Axis')
        ax[0].set_ylabel('Core Sample $z$-Axis')
        ax[0].set_xticks([])
        ax[0].set_yticks([])
        ax[0].set_title('Core Sample Cross-Section')
        ax[0].legend(handles=patches)

        ax[1].plot(points, stresses, color = 'tab:gray', linestyle = '-.',
                   label = 'Future Stress')

        ax[1].plot(points[:n+1], stresses[:n+1], color = 'tab:blue',
                   linestyle = '-', label = 'Past Stress')

        ax[1].plot(points[n], stresses[n], 'r^',
                   label = 'Current Stress')


        ax[1].set_title('Axial Stress Applied to Sample')
        ax[1].set_xlim([np.min(points), np.max(points)])
        ax[1].set_xlabel('Experiment Step')
        ax[1].set_ylabel('Axial Stress [MPa]')
        ax[1].legend()

        pressure = float(dataset.pressures[n])
        savename = f"{save_dir}{label}_{n+1:02d}_MPa_{pressure:03.1f}.png"
        plt.savefig(savename, dpi = img_dpi)
        plt.close()
        print(f"\rRendering {int(100*(n+1)/(len(dataset)-1)):2d}%", end = "")
        savenames.append(savename)
    print()

    return savenames

def create_gif(savenames, save_dir, label):
    images = []
    for filename in savenames:
        images.append(imageio.imread(filename))
    imageio.mimsave(f'{save_dir}{label}.gif', images, duration = 0.25)

"""Main Code"""

for label in labels:
    savenames = generate_save_imgs(label, img_dpi, y_depth_ratio, save_dir)
    create_gif(savenames, save_dir, label)
