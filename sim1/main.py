import env 
import pygame 
import math 
import sensors
import features
import random

def random_color():
	levels = range(32,256,32)
	return tuple(random.choice(levels) for _ in range(3))

feature_map = features.features_detection()
environment = env.build_environment((1200,600))
environment_originalmap =  environment.map.copy()# copy the original known map
sensor = sensors.lidar_sensor(range = 200, map = environment_originalmap, sigma_distance = 0.5, sigma_angle = 0.01)
environment.map.fill((255,255,255)) # fill the map with black
environment.infomap = environment.map.copy()
environment_originalmap =  environment.map.copy()
running = True 

feature_detection = True
break_point_ind = 0

while running:
	sensor_on = False
	environment.infomap = environment.map.copy()
	feature_detection = True
	break_point_ind = 0
	endpoints = [0,0]
	predicted_points_todraw = []

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
			quit() 
		if pygame.mouse.get_focused():
			sensor_on = True
		elif not pygame.mouse.get_focused():
			sensor_on = False

	if sensor_on:
		position = pygame.mouse.get_pos()
		sensor.position = position
		data = sensor.scan()
		feature_map.laser_points_set(data)

		while break_point_ind < (feature_map.NP - feature_map.PMIN):
			seedSeg = feature_map.seed_segment_detection(sensor.position,break_point_ind)
			if seedSeg == False:
				break
			else:
				seedSegment = seedSeg[0]
				predicted_points_todraw = seedSeg[1]
				indices  =seedSeg[2]
				results = feature_map.seed_segment_growing(indices, break_point_ind)
				if results == False:
					break_point_ind = indices[1]
					continue
				else:
					line_eq = results[1]
					m,c = results[5]
					line_seg = results[0]
					outermost = results[2]
					break_point_ind = results[3]

					endpoints[0] =feature_map.projection_point2line(outermost[0],m,c)
					endpoints[1] = feature_map.projection_point2line(outermost[1],m,c)

					color = random_color()

					for point in line_seg:
						environment.infomap.set_at((int(point[0][0]),int(point[0][1])),(0,255,0))
						pygame.draw.circle(environment.infomap,color,(int(point[0][0]),int(point[0][1])),2,0)

					pygame.draw.line(environment.infomap,(255,0,0),endpoints[0],endpoints[1],2)

					environment.data_storage(data)
					#environment.draw_pointcloud()					

	environment.map.blit(environment.infomap,(0,0)) #dr
	pygame.display.update() # update the screen