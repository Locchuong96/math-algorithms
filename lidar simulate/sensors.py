import pygame 
import math 
import numpy as np

def uncertainty_add(distance,angle,sigma):
	mean           = np.array([distance,angle])
	covariance     = np.diag(sigma ** 2)
	distance,angle = np.random.multivariate_normal(mean,covariance)
	distance       = max(distance,0)
	angle          = max(angle,0)
	return [distance,angle]

class LaserSensor: 
	def __init__(self,Range,map,uncertainty):
		self.Range = Range
		self.speed = 4 # rounds per second
		self.sigma = np.array([uncertainty[0],uncertainty[1]])
		self.position =(0,0)
		self.map = map  
		self.W,self.H = pygame.display.get_surface().get_size()
		self.sensedObstacles = []

	def distance(self,obstaclePosition):
		px = (obstaclePosition[0] - self.position[0]) ** 2
		py = (obstaclePosition[1] - self.position[1]) ** 2
		return math.sqrt(px + py)

	def sense_obstacles(self):
		data  = []
		x1,y1 = self.position[0],self.position[1]
		for angle in np.linspace(0,math.pi * 2, 60, False):
			x2 = x1 + self.Range * math.cos(angle)
			y2 = y1 - self.Range * math.sin(angle)
			for i in range(0,100):
				u = i/100
				x = int(x2 * u + x1 * ( 1 - u ))
				y = int(y2 * u + y1 * ( 1 - u ))
				if 0 <x<self.W and 0<y<self.H:
					color = self.map.get_at((x,y))
					if (color[0],color[1],color[2]) == (0,0,0):
						distance = self.distance((x,y))
						output   = uncertainty_add(distance,angle,self.sigma)
						output.append(self.position)
						# store the measurements
						data.append(output)
						break
		if len(data) > 0:
			return data
		else:
			return False




