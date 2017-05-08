#!/usr/bin/env python
import numpy as np
import time
import random
import os
import csv
import matplotlib.patches as patches
from operator import attrgetter
from collections import deque
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation\

characteristics_str = 'optimism', 'patience', 'extroversion'
locations_str = 'Bar','Queue','Street',"Leaving_Queue","Leaving_Bar"
DAY, ITERATION = 0,0

class Bar:
    def __init__(self,*args):
        self.max_occupancy = people
        self.current_occupancy = 0

class Queue:
    def __init__(self,*args):
        self.wait_time = 0
        self.current_line = deque([])

class Patron:
    def __init__(self,*args):
        self.cumulative_happiness = 0
        self.happiness = 0
        self.characteristics = np.asarray([random.random() for x in characteristics_str])
        self.location = "Street"
        self.x = 2
        self.y = random.random()*10
        self.time_entered_queue = 0
        self.length_at_queue_start = 0

    def init_friends(self):
        self.friends = [patrons[i] for i in sorted(random.sample(xrange(len(patrons)), friend_num))]

    def trait_handler(self, trait):
        if cuml_hap_use:
            self.characteristics[characteristics_str.index(trait)] += ((max(self.friends, key=attrgetter('cumulative_happiness')).characteristics - self.characteristics)/2)[characteristics_str.index(trait)]
        else:
            self.characteristics[characteristics_str.index(trait)] += ((max(self.friends, key=attrgetter('happiness')).characteristics - self.characteristics)/2)[characteristics_str.index(trait)]

    def state_string(self):
        return str(self.characteristics[0])+","+str(self.characteristics[1])+","+str(self.characteristics[2])+","+str(self.happiness)+","+str(locations_str.index(self.location))

    def day_reset(self):
        self.cumulative_happiness += self.happiness
        self.happiness = 0
        self.location = "Street"
        self.x = 2
        self.y = random.random()*10
        self.time_entered_queue = 0
        self.length_at_queue_start = 0

def y_n_answer(str):
    valid_yes_ans = ['y','yes','of course!']
    if str.lower() in valid_yes_ans:
        return True
    return False

#average characteristic value by location
def avg_char_by_loc(loc_arr,char_arr):
    char_temp = 0
    for p in patrons:
        thing = [p.characteristics[0],p.characteristics[1],p.characteristics[2]][char_arr]
        if p.location == loc_arr:
            char_temp += thing
    crowd = sum(1 for p in patrons if p.location == loc_arr)
    if crowd != 0:
        return "{0:.2f}".format((char_temp*1.0)/crowd)
    else:
        return 0

#execute patrons behavior based on location and personality characteristics
def step():
    temp_time = time.time()
    for y_ in patrons:
        if y_.location == "Street" and not (y_.y < 4 and y_.y > 3.5 and sum(1 for p in patrons if p.location == "Queue") < y_.characteristics[0] * people):
            y_.x, y_.y = 1.95 + random.random()*0.1, (y_.y+0.1)%10
            #reset the patron's optimism stat if out of frame
            if y_.y + 0.1 > 10:
                y_.trait_handler("optimism")
            #if the patrons exist in a certain location, and the queue is less than their patience threshold
        elif y_.location == "Street":
                y_.x, y_.y = 2.4, 3.9 + random.random()*0.2
                y_.location = "Queue"
        elif y_.location == "Leaving_Queue":
            y_.x = 5.65 + + random.random()*0.1
            y_.y -= 0.2
            if y_.y < 0:
                y_.x,y_.y = 2,0
                y_.trait_handler("patience")
                y_.location = "Street"
        elif y_.location == "Leaving_Bar":
            y_.x = 6.95 + random.random()*0.1
            y_.y += 0.2
            #reset extroversion stats when out of frame
            if y_.y > 10:
                y_.x,y_.y = 2,0
                y_.trait_handler("extroversion")
                y_.location = "Street"
        elif y_.location == "Queue":
            if y_.x == 5.7:
                if ITERATION - y_.time_entered_queue > y_.length_at_queue_start:
                    y_.location = "Bar"
                    y_.length_at_queue_start = 0
                elif ITERATION - y_.time_entered_queue > y_.characteristics[1] * people or capacity <= sum(1 for p in patrons if p.location == "Bar"):
                    y_.location = "Leaving_Queue"
                    y_.y = 3.2
                    y_.length_at_queue_start = 0
            else:
                y_.happiness += -1 * y_.characteristics[1]
                if y_.x < 5.7:
                    y_.x += 0.05
                elif y_.x >= 5.7:
                    y_.x = 5.7
                    y_.length_at_queue_start = sum(1 for p in patrons if p.location == "Queue")
                    y_.time_entered_queue = ITERATION
                y_.y = 3.9 + random.random()*0.2
        elif y_.location == "Bar":
            if sum(1 for p in patrons if p.location == "Bar") > y_.characteristics[2] * capacity:
                y_.location = "Leaving_Bar"
                y_.x,y_.y = 7,8.35
            else:
                y_.happiness += y_.characteristics[2]
                y_.x, y_.y = 6.2 + random.random()*1.6, 3.8 + random.random()* 4
        table_name1 = y_.location
        global ITERATION, iter_rate
        if ITERATION % iter_rate == 0:
            if patrons.index(y_) == 0:
                print ITERATION
            db.append(str(DAY)+","+str(ITERATION)+","+y_.state_string())
    ITERATION += 1

def animate(i):
    global ITERATION, DAY
    if ITERATION == iteration_count:
        ITERATION = 0
        DAY += 1
        for x in patrons:
            x.day_reset()
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
    ax.set_title('Day Number: '+str(DAY)+' Frame Number: '+str(ITERATION))
    x_movements,y_movements = [z.x for z in patrons],[z.y for z in patrons]
    plt.scatter(x_movements,y_movements)
    global stats_out
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

db = []#["day, iteration, optimism, patience, extroversion, happiness"]
cuml_hap_use = y_n_answer(raw_input("\nCumulative happiness model? "))
people = int(raw_input("\nHow large is the population? "))
patrons = [Patron() for x in range(people)]
capacity = int(raw_input("\nWhat is the percent capacity of the bar relative to the population (0-100)? ")) * people / 100
friend_num = int(raw_input("\nHow many connections should each patron have? "))
for x in patrons:
    x.init_friends()
day_count = int(raw_input("\nHow many days? "))
iteration_count = int(raw_input("\nHow many iterations per day? "))
iter_rate = int(raw_input("\nData collection rate? (> total iterations / 10  casues serious lag) "))

stats_out = ['' for x in locations_str]
for x in range(0,len(stats_out)):
    stats_out[x] = locations_str[x]+'\nPopulation %'
    for y in range(0,len(characteristics_str)):
        stats_out[x] += ':\n'+characteristics_str[y]
if y_n_answer(raw_input("\nAnimate? ")):
    plt.style.use('fivethirtyeight')

    fig, ax = plt.subplots()

    ax = plt.axes(xlim=(0, 10), ylim=(0, 10))

    anim = animation.FuncAnimation(fig, animate,
                                   frames = day_count * iteration_count,
                                   interval=1,
                                   blit=False,
                                   repeat=False)
    plt.show()

else:
    for x in range(day_count):
        for y in range(iteration_count):
            step()
        ITERATION = 0
        DAY += 1
        for z in patrons:
            z.day_reset()

#make .txt files for three states of patronslocation:
#street, queue, and bar
file = open("Cumulative"+str(cuml_hap_use)+"population"+str(people)+"capacity"+str(capacity)+"connections"+str(friend_num)+"day"+str(day_count)+"results.csv","w")
for x in db:
    file.write(x+'\n')
file.close()

if y_n_answer(raw_input("\nShow graphs? ")):
    file = open("Cumulative"+str(cuml_hap_use)+"population"+str(people)+"capacity"+str(capacity)+"connections"+str(friend_num)+"day"+str(day_count)+"results.csv","rU")
    my_list = np.asarray([list(map(float,rec)) for rec in csv.reader(file, delimiter=',')])
    if y_n_answer(raw_input("\nShow traits by day and by iteration? ")):
        days = my_list.T[0]
        days.tolist()
        days = sorted(list(set(days)))
        print days
        iterations = my_list.T[1]
        iterations.tolist()
        iterations = sorted(list(set(iterations)))
        for day_num in range(len(days)):
            for it_num in range(len(iterations)):
                da = days[day_num]
                it = iterations[it_num]
                print da,it
                plt.style.use('fivethirtyeight')
                fig = plt.figure()
                ax = fig.add_subplot(131)
                ax1 = fig.add_subplot(132)
                ax2 = fig.add_subplot(133)
                fig.suptitle('Day Number: '+str(day_num)+'Frame Number: '+str(it), fontsize=14, fontweight='bold')
                graph = np.asarray([x for x in my_list if x[0] == da and x[1] == it]).T
                if graph.shape == (0,):
                    ax.scatter(0,0,0)
                else:
                    ax.set_xlabel('optimism')
                    ax.set_ylabel('happiness')
                    ax1.set_xlabel('patience')
                    ax1.set_ylabel('happiness')
                    ax2.set_xlabel('extroversion')
                    ax2.set_ylabel('happiness')
                    ax.scatter(graph[2],graph[5])
                    ax1.scatter(graph[3],graph[5])
                    ax2.scatter(graph[4],graph[5])
                    ax.set_xlim([0,1])
                    ax1.set_xlim([0,1])
                    ax2.set_xlim([0,1])
                plt.draw()
                plt.pause(0.01)
                if (day_num != len(days) - 1 or it_num != len(iterations) - 1) and it != 900.0:
                        plt.close(fig)
    if y_n_answer(raw_input("\nShow traits/happiness by location/iteration? ")):
        for z in range(len(locations_str)-2):
            i = 2
            graph = np.asarray([x for x in my_list if x[6] == z]).T
            days = graph[0]
            days.tolist()
            days = sorted(list(set(days)))
            iterations = graph[1]
            iterations.tolist()
            iterations = sorted(list(set(iterations)))
            for day_num in range(len(days)):
                for it_num in range(len(iterations)):
                    da = days[day_num]
                    it = iterations[it_num]
                    plt.style.use('fivethirtyeight')
                    fig = plt.figure()
                    fig.suptitle(locations_str[z], fontsize=14, fontweight='bold')
                    ax = fig.add_subplot(131)
                    ax1 = fig.add_subplot(132)
                    ax2 = fig.add_subplot(133)
                    fig.suptitle(locations_str[z]+' Day Number: '+str(day_num)+'Frame Number: '+str(it), fontsize=14, fontweight='bold')
                    graph = np.asarray([x for x in my_list if x[0] == da and x[1] == it]).T
                    if graph.shape == (0,):
                        ax.scatter(0,0,0)
                    else:
                        ax.set_xlabel('optimism')
                        ax.set_ylabel('happiness')
                        ax1.set_xlabel('patience')
                        ax1.set_ylabel('happiness')
                        ax2.set_xlabel('extroversion')
                        ax2.set_ylabel('happiness')
                        ax.scatter(graph[2],graph[5])
                        ax1.scatter(graph[3],graph[5])
                        ax2.scatter(graph[4],graph[5])
                        ax.set_xlim([0,1])
                        ax1.set_xlim([0,1])
                        ax2.set_xlim([0,1])
                        #ax.set_zlim([min(graph[5]),max(graph[5])])
                    plt.draw()
                    plt.pause(0.01)
                    if (day_num != len(days) - 1 or it_num != len(iterations) - 1) and it != 900.0:
                            plt.close(fig)
