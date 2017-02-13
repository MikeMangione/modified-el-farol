#!/usr/bin/env python
import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib import animation\

def step(x,y,queue,bar):
    for y_ in range(0,len(y)):
        if queue[y_] == 0:
            y[y_] = (y[y_]+0.1)%10
            if y[y_] > 6 and y_ % 2 == 0:
                queue[y_] = 1
        elif bar[y_] == 0:
            if x[y_] < 6 - y_ * 0.00002 * sum(queue):
                x[y_] += 0.1
            if y[y_] > 4:
                y[y_] -= 0.2
    return x,y

def update_pos(p):
    x = [2 for i in range(0,p)]
    y = [random.random()*10 for i in range(0,p)]
    return x,y

def animate(i):
    plt.clf()
    ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
    x, y = step(x_movements, y_movements, queue, bar)
    plt.scatter(x_movements,y_movements)
    return

people = 1000
queue = [0 for x in range(0,people)]
bar = [0 for x in range(0,people)]
x_movements, y_movements = update_pos(people)

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(5, 5)

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))

anim = animation.FuncAnimation(fig, animate,
                               frames = 10,
                               interval=1,
                               blit=False)
plt.show()
