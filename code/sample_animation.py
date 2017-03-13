#!/usr/bin/env python
import sqlite3
import numpy as np
import sys
import time
import random
import os.path
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from matplotlib import animation\

ITERATION = 0
people = 1000
sqlite_file = 'el-farol_stats.sqlite'    # name of the sqlite database file
table_names = ['bar_stats','queue_stats','street_stats']
iteration_col, patron_col, in_bar_col, in_queue_col, in_street_col = 'iteration', 'patron_number', 'in_bar', 'in_queue', 'in_street'
characteristics_str = 'Optimism', 'Patience', 'Extroversion'
locations_str = 'Bar', 'Queue', 'Street'
stats_out = ['' for x in locations_str]
for x in range(0,len(stats_out)):
    stats_out[x] = locations_str[x]+'\nPopulation %'
    for y in range(0,len(characteristics_str)):
        stats_out[x] += ':\n'+characteristics_str[y]
characteristics = [[random.random()*people for x in range(0,people)] for x in characteristics_str]
ind_wait = [0 for x in range(0,people)]
timer = [0 for x in range(0,people)]
locations = [[0 for x in range(0,people)] for x in locations_str]
leaving_q = [0 for x in range(0,people)]
leaving_b = [0 for x in range(0,people)]

#average characteristic value by location
def avg_char_by_loc(loc_arr,char_arr):
    char_temp = 0
    for x in range(0,people):
        if loc_arr[x] == 1:
            char_temp += char_arr[x]
    return "{0:.2f}".format(char_temp/sum(loc_arr)/people)

#execute patron behavior based on location and personality characteristics
def step(x,y,timer):
    bar, queue, street = locations
    optimism, patience, extroversion = characteristics
    temp_time = time.time()
    for y_ in range(0,people):
        if queue[y_] == 0 and bar[y_] == 0 and leaving_q[y_] == 0 and leaving_b[y_] == 0:
            x[y_], y[y_] = 1.95 + random.random()*0.1, (y[y_]+0.1)%10
            if y[y_]+0.1 > 10:
                optimism[y_] = random.random()*people
            if y[y_] < 4 and y[y_] > 3.5 and sum(queue) < optimism[y_]:
                x[y_], y[y_] = 2.4, 3.9 + random.random()*0.2
                queue[y_] = 1
                ind_wait[y_] = sum(queue)
                timer[y_] = ITERATION
        elif leaving_q[y_] == 1:
            x[y_] = 5.65 + + random.random()*0.1
            y[y_] -= 0.2
            if y[y_] < 0:
                x[y_],y[y_] = 2,0
                patience[y_] = random.random()*people
                leaving_q[y_] = 0
        elif leaving_b[y_] == 1:
            x[y_] = 6.95 + random.random()*0.1
            y[y_] += 0.2
            if y[y_] > 10:
                x[y_],y[y_] = 2,0
                extroversion[y_] = random.random()*people
                leaving_b[y_] = 0
        elif bar[y_] == 0 and queue[y_] == 1:
            if x[y_] < 5.7:
                x[y_] += 0.1
            elif x[y_] > 5.7:
                x[y_] = 5.7
            y[y_] = 3.9 + random.random()*0.2
            if x[y_] == 5.7:
                if ITERATION - timer[y_] > ind_wait[y_]:
                    bar[y_] = 1
                    queue[y_], ind_wait[y_] = 0,0
                elif ITERATION - timer[y_] > patience[y_]:
                    leaving_q[y_] = 1
                    y[y_] = 3.2
                    queue[y_], ind_wait[y_] = 0,0
        elif bar[y_] == 1:
            if sum(bar) > extroversion[y_]:
                leaving_b[y_] = 1
                x[y_],y[y_] = 7,8.35
                bar[y_] = 0
            else:
                x[y_], y[y_] = 6.2 + random.random()*1.6, 3.8 + random.random()* 4
        if (bar[y_], queue[y_]) == (0,0):
            street[y_] = 1
        else:
            street[y_] = 0
        global ITERATION
        if ITERATION % 10 == 0:
            if y_ == 1:
                print ITERATION
            if bar[y_] == 1:
                table_name1 = 'bar_stats'
            elif queue[y_] == 1:
                table_name1 = 'queue_stats'
            elif street[y_] == 1:
                table_name1 = 'street_stats'
            c.execute('INSERT INTO {tn} ({it},{pt},{oc},{pc},{ec})\
                VALUES({iter},{num},{opt},{pat},{ext})'\
                .format(tn=table_name1, it=iteration_col,\
                pt=patron_col, oc=characteristics_str[0], pc=characteristics_str[1],\
                ec=characteristics_str[2],iter=ITERATION,\
                num=y_,\
                opt=optimism[y_]*1.0/people,pat=patience[y_]*1.0/people,ext=extroversion[y_]*1.0/people
                ))
    ITERATION += 1

#randomly distribute starting positions of patrons on x = 2
def init_pos(p):
    x = [2 for i in range(0,p)]
    y = [random.random()*10 for i in range(0,p)]
    return x,y

def animate(i):
    plt.clf()
    plt.style.use('fivethirtyeight')
    fig.suptitle('Modified El-Farol', fontsize=14, fontweight='bold')
    ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
    ax.add_patch(patches.Rectangle((1.8,-0.1),0.4,10.2,fill=False,linewidth=3,edgecolor='#af0000'))
    ax.add_patch(patches.Rectangle((2.3,3.6),3.6,0.8,fill=False,linewidth=3,edgecolor='#afaf55'))
    ax.add_patch(patches.Rectangle((6,3.6),2,4.4,fill=False,linewidth=3,edgecolor='#00af00'))
    ax.add_patch(patches.Rectangle((6.8,8.2),0.4,4,fill=False,linewidth=3,edgecolor='#af0000'))
    ax.add_patch(patches.Rectangle((5.5,0),0.4,3.4,fill=False,linewidth=3,edgecolor='#af0000'))
    step(x_movements, y_movements, timer)
    ax.set_title('Frame Number: '+str(ITERATION))
    plt.scatter(x_movements,y_movements)
    global stats_out
    if sum(locations[0]) > 0:
        for x in range(0,len(stats_out)):
            stats_out[x] = locations_str[x]+'\nPopulation %:'+"{0:.2f}".format(sum(locations[x])*1.0/people)
            for y in range(0,len(characteristics)):
                stats_out[x] += '\n'+characteristics_str[y]+': '+avg_char_by_loc(locations[x],characteristics[y])
    ax.text(7, 1, stats_out[0], style='italic',
        bbox={'facecolor':'green', 'alpha':0.5, 'pad':10})
    ax.text(2.8, 1, stats_out[1], style='italic',
        bbox={'facecolor':'yellow', 'alpha':0.5, 'pad':10})
    ax.text(3, 7, stats_out[2], style='italic',
        bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    return

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
for x in table_names:
    c.execute('drop table if exists {tn}'.format(tn=x))
    c.execute('CREATE TABLE {tn} ({it} {ft},{pt} {ft},{oc} {ft},{pc} {ft},{ec} {ft}\
        )'\
            .format(tn=x, it=iteration_col,\
            pt=patron_col, oc=characteristics_str[0], pc=characteristics_str[1],\
            ec=characteristics_str[2], ft='INTEGER',\
            ))

x_movements, y_movements = init_pos(people)

plt.style.use('fivethirtyeight')

fig, ax = plt.subplots()

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))

anim = animation.FuncAnimation(fig, animate,
                               frames = 100,
                               interval=1,
                               blit=False)
plt.show()
#for x in range(0,10000):
#    animate(x)
for x in table_names:
    c.execute('SELECT * FROM {tn}'.format(tn=x))
    result = c.fetchall()
    file = open(x+".txt","w")
    for r in result:
        file.write(str(r).lstrip('()').rstrip(')')+'\n')
    file.close()
conn.commit()
conn.close()
