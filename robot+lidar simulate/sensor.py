import pygame 
import math 
import numpy as np

def add_noise(distance,angle,sigma):
	mean           = np.array([distance,angle])
	covariance     = np.diag(sigma ** 2) # two noise are not correlated
	distance,angle = np.random.multivariate_normal(mean, covariance)
	# make sure we dont have ny negative value
	distance 	   = max(distance,0)
	angle   	   = max(angle,0)

	return [distance,angle]


class lidar_sensor:
	def __init__(self,range,map,distance_sigma,angle_sigma):
		self.range           = range 
		self.speed           = 4    # round per second
		self.sigma           = np.array([distance_sigma,angle_sigma])
		self.position        = (0,0)
		self.map             = map 
		self.w,self.h 		 = pygame.display.get_surface().get_size()
		self.sense_obstacles = []

	def distance(self,obstacle_position):
		px = (obstacle_position[0] - self.position[0])**2
		py = (obstacle_position[1] - self.position[1])**2
		return  math.sqrt(px+py)

	def scan(self):
		data = []
		x1,y1 = self.position[0],self.position[1]
		for angle in np.linspace(0,2*math.pi,60,False):
			x2 = x1 + self.range * math.cos(angle)
			y2 = y1 + self.range * math.sin(angle)

			for i in range(0,100):
				u = i/100
				# using iterpolation to get the position between x1,y1 and x2,y2
				x = int(x2 * u + x1 * (1 - u))
				y = int(y2 * u + y2 * (1 - u))
				# if the current point is in the map
				if  0 <x<self.w and  0<y<self.h:
					# get the color of the current point
					color = self.map.get_at((x,y))
					# the color type is RGBA, if the color is black
					if (color[0],color[1],color[2]) == (0,0,0):
						# calculate the distance of the current point
						distance = self.distance((x,y))
						output   = add_noise(distance,angle,self.sigma)
						# output = [[distance,angle],(lidar.x, lidar.y)]
						output.append(self.position)
						# store  the measurement
						data.append(output)
						break
		if len(data)>0:
			return data
		else:
			return False











