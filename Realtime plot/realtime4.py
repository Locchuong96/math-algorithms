import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
import random
import pandas as pd
import numpy as np

plt.style.use('fivethirtyeight')

fig = plt.figure()
ax = plt.axes(xlim = (0,200),ylim = (-2000,2000))
line,  = ax.plot([],[],lw= 2)

x = []
y1 = []
y2 = []

# initialization function: plot the background of each frame
def init():
    line.set_data([],[])
    return line,

def animate(i):

	data = pd.read_csv('data.csv')

	x = data['x_value']
	y1 = data['total_1']
	# y2 = data['total_2']

	line.set_data(x,y1)

	return line,

# plt.gcf() get current figure
ani = FuncAnimation(fig,animate,init_func = init,
    frames = 200,interval= 20,blit = True)

plt.show()