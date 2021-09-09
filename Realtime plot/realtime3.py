import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
import random
import pandas as pd

plt.style.use('fivethirtyeight')

x = []
y1 = []
y2 = []

def animate(i):

	data = pd.read_csv('data.csv')

	x= data['x_value']
	y1 = data['total_1']
	y2 = data['total_2']

	#clear the axes
	plt.cla()
	plt.plot(x,y1,label = "y1")
	plt.plot(x,y2,label = "y2")

	plt.legend(loc = 'upper left')# display the legend after cleared by cla
	plt.tight_layout()

# plt.gcf() get current figure
ani = FuncAnimation(plt.gcf(),animate,interval = 1000)

plt.show()