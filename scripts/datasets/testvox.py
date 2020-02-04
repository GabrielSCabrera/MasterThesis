import config
import numpy as np
from time import time
from mayavi import mlab

files = config.bins['M8_1'].bins

rn = 1000
cn = 1000
sn = 1200

all_data = []

frames = 34 # Maximum 34

print("0%", end = "")
for n,f in enumerate(files[:frames]):
    if n == 4:
        continue
    path = config.bin_dirs['M8_1'] + f
    data = np.fromfile(path, dtype = np.uint8)
    data = data.reshape(sn, rn, cn)
    x, y, z = np.where(data == 1)
    all_data.append([x, y, z])
    print(f"\r{int(100*(n+1)/(frames)):2d}%", end = "")
print()


points = mlab.points3d(*all_data[0], mode = "cube", color = (0, 0, 1),
                     scale_factor = 1)

# @mlab.animate(delay = 1000, ui = True)
def anim():
    f = mlab.gcf()
    n = 0
    # while True:
    for n,frame in enumerate(all_data):
        frame = all_data[n]
        points.mlab_source.reset(x = frame[0], y = frame[1], z = frame[2])
        mlab.savefig(f"./imgs/img_{n+1}.png")
        # print(n)
        # n += 1
        # n = n%len(all_data)
        # yield

anim()
# mlab.show()
