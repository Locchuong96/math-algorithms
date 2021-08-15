import  pygame 
import math 
import numpy as np

def uncertainty_add(distance,angle,sigma):
	"""
	Add noise follow the gauss distribution
	sigma is diagonal matrix, meaning distance and angle are not correlated
	"""
	mean =  np.array([distance,angle])
	covariance = np.diag(sigma ** 2)
	distance, angle = np.random.multivariate_normal(mean,covariance) # return a random number of distance and angle
	distance = max(distance,0) # make sure distance not negative
	angle = max(angle,0) # make sure angle are not negative
	return [distance,angle]

class lidar_sensor:
	def __init__(self, range, map, sigma_distance, sigma_angle):
		self.range = range 
		self.speed = 4  # Hz round per second
		self.sigma = np.array([sigma_distance,sigma_angle]) #matrix sigma for uncertainty
		self.position = (0,0)
		self.map = map
		self.w, self.h = pygame.display.get_surface().get_size() # get screen size of current window display in pygame
		self.obstacles = [] #storage obstacles postions
	
	def distance(self, obstacle_position):
		px = (obstacle_position[0] -  self.position[0])**2
		py = (obstacle_position[1] - self.position[1])**2
		return math.sqrt(px + py)

	def scan(self):
		data = []
		x1 = self.position[0]
		y1 = self.position[1]
		for angle in np.linspace(0,2*math.pi,60,False):
			x2 = x1 + self.range * math.cos(angle)
			y2 = y1 - self.range * math.sin(angle) # y1 minus because in the coordinate of the pygame, y axis is go down

			for  i in range(0,100):
				u = i/100
				x = int( x2 * u + x1 * (1-u) ) #split the line between sensor and (x2,y2) 100 session, using interpolation to calculate each session's point
				y = int( y2 * u + y1 * (1-u) )
				#check if the current point is in the screen
				if 0 <x<self.w and 0<y<self.h: 
					color = self.map.get_at((x,y)) # color type RGBA
					# if the color is black 
					if (color[0],color[1],color[2]) == (0,0,0):
						distance = self.distance((x,y))
						output = uncertainty_add(distance,angle,self.sigma)#add noise
						output.append(self.position) # output = [distance_noise,angle_noise,(x,y)]
						# store the measurements
						data.append(output)
						break
		if len(data) >0:
			return data
		else:
			return False






