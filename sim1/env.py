import math 
import pygame 

class build_environment:
	def __init__(self,map_dimensions):
		pygame.init()
		self.pointcloud = [] # a list storage every point cloud at a specify position
		self.external_map = pygame.image.load('./map.png') # load your map
		self.mapw, self.maph = map_dimensions # get the demension of the map
		self.window_name = 'Lidar Simulation'
		pygame.display.set_caption(self.window_name) # set the title for display window
		self.map = pygame.display.set_mode((self.mapw,self.maph)) # create a window with screen side as given
		self.map.blit(self.external_map,(0,0)) # blit the external map on screen at position (0,0)
		# define some color
		self.black = (0,0,0)
		self.grey  =(70,70,70)
		self.blue  = (0,0,255)
		self.green = (0,255,0)
		self.red = (255,0,0)
		self.white = (255,255,255)

	def AD2pos(self,distance,angle,sensor_position):
		"""
		Return the distance and angle from the data lsit lidar return after a scane round
		"""
		x = distance * math.cos(angle) + sensor_position[0]
		y = -distance * math.sin(angle) + sensor_position[1]

		return (int(x),int(y))

	def data_storage(self,data):
		for element in data:
			point = self.AD2pos(element[0],element[1],element[2])
			if point not in self.pointcloud:
				self.pointcloud.append(point) #this pointcloud keep bigger and it storage every point from the whole map

	def draw_pointcloud(self):
		self.infomap = self.map.copy()
		for point in self.pointcloud:
			self.infomap.set_at((point[0],point[1]),(255,0,0))








