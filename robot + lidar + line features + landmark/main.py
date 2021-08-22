import pygame 
import math 
import robot
import sensors
import features 

screen_width = 1200
screen_height = 600
fps = 10 
path = './map2.png'
start_pos = (70,70,0)

#initialize pygame 
pygame.init()
text = pygame.font.Font('PokemonGb-RAeo.ttf',8)
clock = pygame.time.Clock()
surface = pygame.display.set_mode((screen_width,screen_height))
background = pygame.image.load(path).convert()
pygame.display.set_caption('simulate environment')

# create robot model
model = robot.DDR(surface,text,start_pos)

# create lidar sensor
lidar = sensors.lidar_sensor(range = 120, map = background, sigma_distance = 0.5, sigma_angle = 0.01)

# create features extractor
feature_map = features.features_detection()

if __name__ == "__main__":

	while True:

		break_point_ind = 0
		endpoints = [(0,0),(0,0)]

		#fill the map with black to show just only the last frame
		surface.fill((0,0,0))
		#keep background image
		#surface.blit(background,(0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		model.move()

		lidar.position = (model.x,model.y)

		if not lidar.scan:
			continue
		else:
			data = lidar.scan()
			feature_map.laser_points_set(data)
			feature_map.seed_segment_detection(lidar.position)
			
			# calculate landmark
			features.landmark_association(feature_map.LINE_SEGMENTS)

			# draw landmark
			for line in features.LANDMARKS:
				pygame.draw.line(surface,(0,0,255),line[0],line[1],5)

			# draw current line
			for line in feature_map.LINE_SEGMENTS:
				pygame.draw.line(surface,(255,102,255),line[0],line[1],3)

			# draw obstacle point
			for obstacle in feature_map.LASERPOINTS:
				pygame.draw.circle(surface,(255,26,140),obstacle[0],2)

		pygame.display.update()

		clock.tick(fps)





