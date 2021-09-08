import numpy as np 
import matplotlib.pyplot as plt 

"""
However, to make a real-time scatter,
 we can just update the values of x and y and add scatter points in each iteration
 """
for i in range(100):
	
	x= i
	y = np.sin(x)

	plt.scatter(x,y)

	plt.title("Real Time plot")
	plt.xlabel("x")
	plt.ylabel("y")

	plt.pause(0.5)

plt.show()