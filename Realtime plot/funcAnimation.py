import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation

"""
figure is the figure object whose plot will be updated.

func_animate is the function to be called at each frame. Its first argument comes from the next value frames.

frames=10 is equal to range(10). Values from 0 to 9 is passed to the func_animate at each frame. We could also assign an interalbe to frames, like a list [0, 1, 3, 7, 12].

interval is the delay between frames in the unit of ms.

We could save the animation to a gif or mp4 with the parameters like fps and dpi
"""
x = []
y = []

figure,ax = plt.subplots(figsize = (4,3))
line, = ax.plot(x,y)
plt.axis([0,4*np.pi,-1,1])

def func_animate(i):
	x = np.linspace(0 ,4 * np.pi, 1000)
	y = np.sin(2 * (x - 0.1 * i))
	line.set_data(x,y)
	return line,


ani = FuncAnimation(figure,
				func_animate,
				frames = 10,
				interval = 50)

ani.save(r'animation.gif',fps = 10)

plt.show()

