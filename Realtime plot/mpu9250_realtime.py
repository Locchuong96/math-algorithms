import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation 
import requests as rs

plt.style.use('fivethirtyeight')

niter = 0
x  = []
ax = []
ay = []
az = []
gx = []
gy = []
gz = []
mx = []
my = []
mz = []

url = "http://192.168.1.11"

def animate(i):

	global niter

	res = rs.get(url)
	data = res.json()

	x.append(niter)
	niter +=1

	ax.append(data['ax'])
	ay.append(data['ay'])
	az.append(data['az'])
	gx.append(data['gx'])
	gy.append(data['gy'])
	gz.append(data['gz'])
	mx.append(data['mx'])
	my.append(data['my'])
	mz.append(data['mz'])

	plt.cla()

	plt.plot(x,ax,label = "ax")
	plt.plot(x,ay,label = "ay")
	plt.plot(x,az,label = "az")
	plt.plot(x,gx,label = "gx")
	plt.plot(x,gy,label = "gy")
	plt.plot(x,gz,label = "gz")
	plt.plot(x,mx,label = "mx")
	plt.plot(x,my,label = "my")
	plt.plot(x,mz,label = "mz")

	plt.legend(loc = 'upper left')# display the legend after cleared by cla
	plt.tight_layout()


ani = FuncAnimation(plt.gcf(),animate,interval = 1000)

plt.show()