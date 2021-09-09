import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
import random
from itertools import count 

plt.style.use('fivethirtyeight')

x = []
y = []
index= count()

def animate(i):
	x.append(next(index))
	y.append(random.randint(0,5))

	#clear the axes
	plt.cla()
	plt.plot(x,y)

# plt.gcf() get current figure
ani = FuncAnimation(plt.gcf(),animate,interval = 1000)

plt.tight_layout()
plt.show()