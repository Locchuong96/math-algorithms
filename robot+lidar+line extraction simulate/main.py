import pygame 
import math 
import robot
import sensors
import features 

screen_width = 1200
screen_height = 600
fps = 10 
path = './map.png'
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
lidar = sensors.lidar_sensor(range = 200, map = background, sigma_distance = 0.5, sigma_angle = 0.01)

# create features extractor
feature_map = features.features_detection()

def random_color():
	levels = range(32,256,32)
	return tuple(random.choice(levels) for _ in range(3))

if __name__ == "__main__":

	while True:

		break_point_ind = 0
		endpoints = [(0,0),(0,0)]

		#fill the map with black to show just only the last frame
		#surface.fill((0,0,0))
		surface.blit(background,(0,0))

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

			for line in feature_map.LINE_SEGMENTS:
				pygame.draw.line(surface,(153,153,102),line[0],line[1],5)

			for obstacle in feature_map.LASERPOINTS:
				pygame.draw.circle(surface,(203,203,179),obstacle[0],3)

		pygame.display.update()

		clock.tick(fps)





