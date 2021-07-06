import pygame
import math 

class build_environment:
	def __init__(self,map_dimensions):
		pygame.init()
		self.point_cloud    = []
		self.external_map   = pygame.image.load('map.png')
		self.mapw,self.maph = map_dimensions
		self.map_windowname = 'Simulate Workspace'
		pygame.display.set_caption(self.map_windowname)
		self.map = pygame.display.set_mode((self.mapw,self.maph))
		self.map.blit(self.external_map,(0,0))
		#Colors
		self.color_black = (0,0,0)
		self.color_grey  = (70,70,70)
		self.color_blue  = (0,0,255)
		self.color_green = (0,255,0)
		self.color_red   = (255,0,0)
		self.color_white = (255,255,255)

	def da2pos(self,distance,angle,robot_position):
		"""
		calculate the position via the angle and the distance
		"""
		x = distance * math.cos(angle) + robot_position[0]
		y = distance * math.sin(angle) + robot_position[1]
		return (int(x),int(y))

	def data_storage(self,data):
		print(len(self.point_cloud))
		for element in data:
			point = self.da2pos(element[0],element[1],element[2])
			if point not in self.point_cloud:
				self.point_cloud.append(point)

	def show_sensordata(self):
		self.infomap = self.map.copy()
		for point in self.point_cloud:
			self.infomap.set_at(( int(point[0]),int(point[1])),(0,255,0))




