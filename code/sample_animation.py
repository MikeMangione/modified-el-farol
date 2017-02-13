#!/usr/bin/env python
import numpy as np
import time
import random
from matplotlib import pyplot as plt
from matplotlib import animation\

ITERATION = 0
people = 1000
optimism = [random.random()*people for x in range(0,people)]
patience = [random.random()*people for x in range(0,people)]
extroversion = [random.random()*people for x in range(0,people)]
ind_wait = [0 for x in range(0,people)]
timer = [0 for x in range(0,people)]
queue = [0 for x in range(0,people)]
bar = [0 for x in range(0,people)]
leaving_q = [0 for x in range(0,people)]
leaving_b = [0 for x in range(0,people)]

def step(x,y,queue,bar,timer):
    temp_time = time.time()
    for y_ in range(0,len(y)):
        if queue[y_] == 0 and bar[y_] == 0 and leaving_q[y_] == 0 and leaving_b[y_] == 0:
            y[y_] = (y[y_]+0.1)%10
            if y[y_] > 6 and sum(queue) < optimism[y_]:
                queue[y_] = 1
                ind_wait[y_] = sum(queue)
                timer[y_] = ITERATION
        elif leaving_q[y_] == 1:
            y[y_] -= 0.2
            if y[y_] < 0:
                x[y_],y[y_] = 2,0
                leaving_q[y_] = 0
        elif leaving_b[y_] == 1:
            x[y_] += 0.2
            if x[y_] > 10:
                x[y_],y[y_] = 2,0
                leaving_b[y_] = 0
        elif bar[y_] == 0:
            if x[y_] < 6 - y_ * 0.00002:
                x[y_] += 0.1
            else:
                pass
            if y[y_] > 4:
                y[y_] -= 0.2
            else:
                pass
            if x[y_] >= 6 - y_ * 0.00002 and y[y_] <= 4:
                if ITERATION - timer[y_] > ind_wait[y_]:
                    bar[y_] = 1
                    queue[y_], ind_wait[y_] = 0,0
                elif ITERATION - timer[y_] > patience[y_]:
                    leaving_q[y_] = 1
                    queue[y_], ind_wait[y_] = 0,0
        elif bar[y_] == 1:
            x[y_], y[y_] = 6 + random.random()*2, 4 + random.random()* 4
            if sum(bar) > extroversion[y_]:
                leaving_b[y_] = 1
                bar[y_] = 0
    global ITERATION
    ITERATION += 1
    return x,y

def update_pos(p):
    x = [2 for i in range(0,p)]
    y = [random.random()*10 for i in range(0,p)]
    return x,y

def animate(i):
    plt.clf()
    ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
    x, y = step(x_movements, y_movements, queue, bar, timer)
    plt.scatter(x_movements,y_movements)
    return

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
