import config
import numpy as np
from time import time
import matplotlib.pyplot as plt

path = config.bin_dirs['M8_1'] + "M8_1_26MPa.bin"
data = np.fromfile(path, dtype = np.uint8)

rn = 1000
cn = 1000
sn = 1200
data = data.reshape(sn, rn, cn)

ci = 400
ci_0 = 400
sli = data[:,ci_0,:]

fig = plt.figure(figsize=(6, 3.2))
ax = fig.add_subplot(111)
plt.imshow(sli)
ax.set_aspect('equal')
plt.show()

######################
import matplotlib
import matplotlib.animation as animation


fps = 30
nSeconds = 5

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure(figsize=(6, 3.2))

im = plt.imshow(sli, interpolation='none', aspect='auto')#, vmin=0, vmax=1)

def animate_func(i):
    im.set_array(data[:,ci_0 + i,:])
    return [im]

anim = animation.FuncAnimation(
                               fig,
                               animate_func,
                               frames = nSeconds * fps,
                               interval = 1000 / fps, # in ms
                               )
plt.show()
# plt.show()
# anim.save('test_anim.mp4', fps=fps, extra_args=['-vcodec', 'libx264'])

print('Done!')

# plt.show()  # Not required, it seems!
