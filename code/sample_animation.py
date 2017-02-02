#!/usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation\

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(5, 5)

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
patch = [plt.Circle((1, -1), 0.1, fc='r') for x in range(0,10)]

y_ = [0,1,2,3,4,5,6,7,8,9,10]

def init():
    for z in range(0,len(patch)):
        patch[z].center = (2, 0)
        ax.add_patch(patch[z])
    return patch,

def animate(i):
    for z in range(0,len(patch)):
        x, y = patch[z].center
        x = x
        y = y_[(i+z)%len(y_)]
        patch[z].center = (x, y)
    return patch,

anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames = 10,
                               interval=200,
                               blit=False)
plt.show()
