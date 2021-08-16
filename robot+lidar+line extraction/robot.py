import pygame
import math 

color_black = (0,0,0)
color_white = (255,255,255)
color_red   = (255,0,0) 
color_blue  = (0,0,255)
color_green = (0,255,0)
color_trail = (0,255,255)

class DDR:
	"""
	Differential Drive robot
	Control by rotate angle and linear moving
	"""
	def __init__(self,map,text_font,start_pos,step_linear = 10, step_rotate = 3,bot_color = (0,255,0),footprint = False):
		self.map = map 
		self.text_font = text_font
		self.x = start_pos[0] #pixel
		self.y = start_pos[1] # pixel
		self.theta = start_pos[2] # degree
		self.step_linear = step_linear
		self.step_rotate = step_rotate
		self.mm2p = 3.7793 # milimter to pixel
		self.width = 15 
		self.lenght_x = 20
		self.lenght_y = 10
		self.foots = []
		self.color = bot_color
		self.footprint = footprint 

	def move(self):
		key = pygame.key.get_pressed() #get the input key

		# moving forward
		if key[pygame.K_UP]:
			self.x = self.x + self.step_linear * math.cos(-math.radians(self.theta))
			self.y = self.y + self.step_linear * math.sin(-math.radians(self.theta))

		# stepback
		if key[pygame.K_DOWN]:
			self.x = self.x - self.step_linear * math.cos(-math.radians(self.theta))
			self.y = self.y - self.step_linear * math.sin(-math.radians(self.theta))

		# rotate CW
		if key[pygame.K_z]:
			self.theta += self.step_rotate
			if self.theta == 360:
				self.theta = 0

		# rotate CCW
		if key[pygame.K_x]:
			self.theta -= self.step_rotate
			if self.theta == -360:
				self.theta = 0

		# calculate the position of x axis peak point
		x_peak = ( self.x + self.lenght_x * math.cos(-math.radians(self.theta)) , self.y + self.lenght_x * math.sin(-math.radians(self.theta)))
		y_peak = ( self.x + self.lenght_y * math.cos(-math.radians(self.theta) + math.pi/2) , self.y + self.lenght_y * math.sin(-math.radians(self.theta) + math.pi/2))

		# draw the robot with position
		pygame.draw.circle(self.map,self.color,(self.x,self.y),self.width)
		pygame.draw.line(self.map,color_red,(self.x,self.y),x_peak,3)
		pygame.draw.line(self.map,color_blue,(self.x,self.y),y_peak,3)

		txt_content = self.text_font.render("({0},{1},{2})".format(round(self.x,2),round(self.y,2),round(self.theta,2)),True,color_white,color_black)
		txt_rect = (self.x,self.y +self.width)

		self.map.blit(txt_content,txt_rect)

		# storage robot step
		self.foots.append((self.x,self.y))

		# draw robot footprint 
		if self.footprint:
			for i in range(len(self.foots)):
				pygame.draw.circle(self.map,color_trail,self.foots[i],2)

		if self.foots.__sizeof__() > 6000:
			self.foots.pop(0) # drop the first footstep if foots list out of size max











