import numpy as np 
import time 
import matplotlib.pyplot as plt 

x = np.linspace(0,10,100)
y = np.cos(x)

plt.ion() # turn on interactive mode

figure,ax = plt.subplots(figsize = (8,6))
line1, = ax.plot(x,y)

plt.title("Dynamic Plot of sinx", fontsize =25)

plt.xlabel("X",fontsize = 18)
plt.ylabel("sinX",fontsize = 18)

for p in range(100):

	updated_y = np.cos(x - 0.05*p)

	line1.set_xdata(x)
	line1.set_ydata(updated_y)

	figure.canvas.draw() # draw the plot 
	figure.canvas.flush_events() # clar figures on every iterations so that successiv figures might not overlap
	time.sleep(0.1) # delay to slow down