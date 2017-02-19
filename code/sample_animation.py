#!/usr/bin/env python
import sqlite3
import numpy as np
import sys
import time
import random
import os.path
import matplotlib.patches as patches
import matplotlib.cm as cm
from matplotlib.mlab import bivariate_normal
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib import animation\

ITERATION = 0

def avg_optimism(arr):
    opt = 0
    for x in range(0,people):
        if arr[x] == 1:
            opt += optimism[x]
    return "{0:.2f}".format(opt/sum(arr)/people)

def avg_patience(arr):
    pat = 0
    for x in range(0,people):
        if arr[x] == 1:
            pat += patience[x]
    return "{0:.2f}".format(pat/sum(arr)/people)

def avg_extroversion(arr):
    ext = 0
    for x in range(0,people):
        if arr[x] == 1:
            ext += extroversion[x]
    return "{0:.2f}".format(ext/sum(arr)/people)

def step(x,y,queue,bar,timer):
    temp_time = time.time()
    for y_ in range(0,people):
        if queue[y_] == 0 and bar[y_] == 0 and leaving_q[y_] == 0 and leaving_b[y_] == 0:
            y[y_] = (y[y_]+0.1)%10
            if y[y_] < 3 and y[y_] > 2 and sum(queue) < optimism[y_]:
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
            if y[y_] < 4:
                y[y_] += 0.2
            else:
                pass
            if x[y_] >= 6 - y_ * 0.00002 and y[y_] >= 4:
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
        if (bar[y_], queue[y_]) == (0,0):
            street[y_] = 1
        else:
            street[y_] = 0
        global ITERATION
        if ITERATION % 10 == 0:
            c.execute('INSERT INTO {tn} ({it},{pt},{ib},{iq},{isc},{oc},{pc},{ec})\
                VALUES({iter},{num},{bar},{queue},{street},{opt},{pat},{ext})'\
                .format(tn=table_name1, it=iteration_col,\
                pt=patron_col, ib=in_bar_col,\
                iq=in_queue_col, isc=in_street_col,\
                oc=optimism_col, pc=patience_col,\
                ec=extroversion_col,iter=ITERATION,\
                num=y_,bar=bar[y_],queue=queue[y_],street=street[y_],\
                opt=optimism[y_]*1.0/people,pat=patience[y_]*1.0/people,ext=extroversion[y_]*1.0/people
                ))
    ITERATION += 1
    return x,y

def update_pos(p):
    x = [2 for i in range(0,p)]
    y = [random.random()*10 for i in range(0,p)]
    return x,y

def animate(i):
    plt.clf()
    fig.suptitle('Modified El-Farol', fontsize=14, fontweight='bold')
    ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
    ax.add_patch(patches.Rectangle((5.8,3.8),2.4,4.4,fill=False))
    x, y = step(x_movements, y_movements, queue, bar, timer)
    ax.set_title('Frame Number: '+str(ITERATION))
    plt.scatter(x_movements,y_movements)
    global bar_stats, queue_stats, street_stats
    if sum(bar) > 0:
        bar_stats = 'Bar\nPopulation %:'+"{0:.2f}".format(sum(bar)*1.0/people)+'\nOptimism: '+avg_optimism(bar)+'\nPatience: '+avg_patience(bar)+'\nExtroversion: '+avg_extroversion(bar)
        queue_stats = 'Queue\nPopulation %:'+"{0:.2f}".format(sum(queue)*1.0/people)+'\nOptimism: '+avg_optimism(queue)+'\nPatience: '+avg_patience(queue)+'\nExtroversion: '+avg_extroversion(queue)
        street_stats = 'Street\nPopulation %:'+"{0:.2f}".format(sum(street)*1.0/people)+'\nOptimism: '+avg_optimism(street)+'\nPatience: '+avg_patience(street)+'\nExtroversion: '+avg_extroversion(street)
    ax.text(7, 1, bar_stats, style='italic',
        bbox={'facecolor':'green', 'alpha':0.5, 'pad':10})
    ax.text(3, 1, queue_stats, style='italic',
        bbox={'facecolor':'yellow', 'alpha':0.5, 'pad':10})
    ax.text(3, 7, street_stats, style='italic',
        bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    return

sqlite_file = 'el-farol_stats.sqlite'    # name of the sqlite database file
table_name1 = 'simulation'
iteration_col, patron_col, in_bar_col, in_queue_col, in_street_col = 'iteration', 'patron_number', 'in_bar', 'in_queue', 'in_street'
optimism_col, patience_col, extroversion_col = 'optimism', 'patience', 'extroversion'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute('drop table if exists {tn}'.format(tn=table_name1))
c.execute('CREATE TABLE {tn} ({it} {ft},{pt} {ft},{ib} {ft},{iq} {ft},{isc} {ft},{oc} {ft},{pc} {ft},{ec} {ft}\
    )'\
        .format(tn=table_name1, it=iteration_col,\
        pt=patron_col, ib=in_bar_col,\
        iq=in_queue_col, isc=in_street_col,\
        oc=optimism_col, pc=patience_col,\
        ec=extroversion_col, ft='INTEGER',\
        ))

people = 1000
bar_stats = 'Bar\nPopulation %:\nOptimism:\nPatience:\nExtroversion: '
queue_stats = 'Queue\nPopulation %:\nOptimism:\nPatience:\nExtroversion: '
street_stats = 'Street\nPopulation %:\nOptimism:\nPatience:\nExtroversion: '
optimism = [random.random()*people for x in range(0,people)]
patience = [random.random()*people for x in range(0,people)]
extroversion = [random.random()*people for x in range(0,people)]
ind_wait = [0 for x in range(0,people)]
timer = [0 for x in range(0,people)]
queue = [0 for x in range(0,people)]
bar = [0 for x in range(0,people)]
street = [0 for x in range(0,people)]
leaving_q = [0 for x in range(0,people)]
leaving_b = [0 for x in range(0,people)]

x_movements, y_movements = update_pos(people)

fig, ax = plt.subplots()

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))

anim = animation.FuncAnimation(fig, animate,
                               frames = 100,
                               interval=1,
                               blit=False)
plt.show()
c.execute('SELECT * FROM {tn}'.format(tn=table_name1))
result = c.fetchall()
for r in result:
    print r,
conn.commit()
conn.close()
