#!/usr/bin/env python
import numpy as np
import sys
import time
import math
import random
import os.path
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from matplotlib import animation\

class Patron:
    def __init__(self,*args):
        self.optimism = random.randint(0,(people+1))
        self.patience = random.randint(0,(people+1))
        self.extroversion = random.randint(0,(people+1))
        self.location = "Street"
        self.x = 2
        self.y = random.random()*10
        self.time_entered_queue = 0
        self.length_at_queue_start = 0

    def state_string(self):
        return str(self.optimism)+","+str(self.patience)+","+str(self.extroversion)+","+str(self.location)

db = ["iteration, optimism, patience, extroversion, location"]
ITERATION = 0
people = int(raw_input("\nHow large is the population? "))
patrons = [Patron() for x in range(people)]

def trait_handler(trait_type, trait_value):
    return random.randint(0,(people+1))
#average characteristic value by location
def avg_char_by_loc(loc_arr,char_arr):
    char_temp = 0
    for p in patrons:
        thing = [p.optimism,p.patience,p.extroversion][char_arr]
        if p.location == loc_arr:
            char_temp += thing
    if sum(1 for p in patrons if p.location == loc_arr) != 0:
        return "{0:.2f}".format(char_temp/sum(1 for p in patrons if p.location == loc_arr)/people)
    else:
        return 0

#execute patrons behavior based on location and personality characteristics
def step():
    temp_time = time.time()
    for y_ in patrons:
        if y_.location == "Street" and not (y_.y < 4 and y_.y > 3.5 and sum(1 for p in patrons if p.location == "Queue") < y_.optimism):
            y_.x, y_.y = 1.95 + random.random()*0.1, (y_.y+0.1)%10
            #reset the patron's optimism stat if out of frame
            if y_.y + 0.1 > 10:
                y_.optimism = trait_handler(characteristics_str[0],y_.optimism)
            #if the patrons exist in a certain location, and the queue is less than their patience threshold
        elif y_.location == "Street":
                y_.x, y_.y = 2.4, 3.9 + random.random()*0.2
                y_.location = "Queue"
                y_.length_at_queue_start = sum(1 for p in patrons if p.location == "Queue")
                y_.time_entered_queue = ITERATION
        elif y_.location == "Leaving_Queue":
            y_.x = 5.65 + + random.random()*0.1
            y_.y -= 0.2
            if y_.y < 0:
                y_.x,y_.y = 2,0
                y_.patience = trait_handler(characteristics_str[1],y_.patience)
                y_.location = "Street"
        elif y_.location == "Leaving_Bar":
            y_.x = 6.95 + random.random()*0.1
            y_.y += 0.2
            #reset extroversion stats when out of frame
            if y_.y > 10:
                y_.x,y_.y = 2,0
                y_.extroversion = trait_handler(characteristics_str[2],y_.extroversion)
                y_.location = "Street"
        elif y_.location == "Queue":
            if y_.x < 5.7:
                y_.x += 0.05
            elif y_.x >= 5.7:
                y_.x = 5.7
            y_.y = 3.9 + random.random()*0.2
            if y_.x == 5.7:
                if ITERATION - y_.time_entered_queue > y_.length_at_queue_start:
                    y_.location = "Bar"
                    y_.length_at_queue_start = 0
                elif ITERATION - y_.time_entered_queue > y_.patience:
                    y_.location = "Leaving_Queue"
                    y_.y = 3.2
                    y_.length_at_queue_start = 0
        elif y_.location == "Bar":
            if sum(1 for p in patrons if p.location == "Bar") > y_.extroversion:
                y_.location = "Leaving_Bar"
                y_.x,y_.y = 7,8.35
            else:
                y_.x, y_.y = 6.2 + random.random()*1.6, 3.8 + random.random()* 4
        table_name1 = y_.location
        global ITERATION
        db.append(str(ITERATION)+","+y_.state_string())
    ITERATION += 1

def animate(i):
    plt.clf()
    plt.style.use('fivethirtyeight')
    fig.suptitle('Modified El-Farol', fontsize=14, fontweight='bold')
    ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
    #hueristic box sizes for patronsmovement
    ax.add_patch(patches.Rectangle((1.8,-0.1),0.4,10.2,fill=False,linewidth=3,edgecolor='#af0000'))
    ax.add_patch(patches.Rectangle((2.3,3.6),3.6,0.8,fill=False,linewidth=3,edgecolor='#afaf55'))
    ax.add_patch(patches.Rectangle((6,3.6),2,4.4,fill=False,linewidth=3,edgecolor='#00af00'))
    ax.add_patch(patches.Rectangle((6.8,8.2),0.4,4,fill=False,linewidth=3,edgecolor='#af0000'))
    ax.add_patch(patches.Rectangle((5.5,0),0.4,3.4,fill=False,linewidth=3,edgecolor='#af0000'))
    step()
    ax.set_title('Frame Number: '+str(ITERATION))
    x_movements,y_movements = [z.x for z in patrons],[z.y for z in patrons]
    plt.scatter(x_movements,y_movements)
    global stats_out
    if any(p.location == "Bar" for p in patrons):
        for x in range(0,len(stats_out)):
            stats_out[x] = locations_str[x]+'\nPopulation %:'+"{0:.2f}".format(sum(1 for p in patrons if p.location == locations_str[x])*1.0/people)
            for y in range(0,len(characteristics_str)):
                stats_out[x] += '\n'+characteristics_str[y]+': '+str(avg_char_by_loc(locations_str[x],y))
    ax.text(7, 1, stats_out[0], style='italic',
        bbox={'facecolor':'green', 'alpha':0.5, 'pad':10})
    ax.text(2.8, 1, stats_out[1], style='italic',
        bbox={'facecolor':'yellow', 'alpha':0.5, 'pad':10})
    ax.text(3, 7, stats_out[2], style='italic',
        bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    return

characteristics_str = 'Optimism', 'Patience', 'Extroversion'
locations_str = 'Bar','Queue','Street',"Leaving_Queue","Leaving_Bar"
stats_out = ['' for x in locations_str]
for x in range(0,len(stats_out)):
    stats_out[x] = locations_str[x]+'\nPopulation %'
    for y in range(0,len(characteristics_str)):
        stats_out[x] += ':\n'+characteristics_str[y]

plt.style.use('fivethirtyeight')

fig, ax = plt.subplots()

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))

anim = animation.FuncAnimation(fig, animate,
                               frames = 100,
                               interval=1,
                               blit=False)
plt.show()

#make .txt files for three states of patronslocation:
#street, queue, and bar
file = open("results.txt","w")
for x in db:
    file.write(x+'\n')
file.close()
