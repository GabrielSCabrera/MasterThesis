#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 14:21:13 2019

@author: mcbeck
"""

import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plt

# made in make_2D.m
#bfil = '/Users/mcbeck/Dropbox/HADES/tracking/matlab/mats/M8_1/bins/M8_1_130MPa.bin'
#rn = 1000
#cn = 1000
#sn = 1200

#bfil = '/Users/mcbeck/Dropbox/HADES/tracking/matlab/mats/M8_2/bins/M8_2_196MPa.bin'
#rn = 900
#cn = 900
#sn = 1200

bfil = '/Users/mcbeck/Dropbox/HADES/tracking/matlab/mats/MONZ5/bins/MONZ5_161.5MPa.bin'
rn = 800
cn = 800
sn = 1200

#bfil = '/Users/mcbeck/Dropbox/HADES/tracking/matlab/mats/WG04/bins/WG04_63_152.5MPa.bin'
#rn = 800
#cn = 800
#sn = 1200

data=np.fromfile(bfil,dtype='uint8')
data=data.reshape(sn, rn, cn)

ci = 400
sli = data[:,ci,:]

fig = plt.figure(figsize=(6, 3.2))
ax = fig.add_subplot(111)
plt.imshow(sli)
ax.set_aspect('equal')