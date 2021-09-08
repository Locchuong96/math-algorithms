import random  
import matplotlib.pyplot as plt 
import time
import numpy as np 


x = np.arange(100)#initialize x 
y = np.random.random_integers(0,20,100) # initialize y

plt.ion() # activate interactive mode

fig,ax = plt.subplots(figsize = (8,4))
line1, = ax.plot(x,y)

plt.title("Realtime random plot")
plt.xlabel("x axis")
plt.ylabel("y axis")

for i in range(100):
	 
	y_now = np.random.random_integers(0,20,100)
	
	line1.set_xdata(x)
	line1.set_ydata(y_now)

	fig.canvas.draw()
	fig.canvas.flush_events()

	time.sleep(0.1)

	#plt.show()