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
environment.map.fill((0,0,0)) # fill the map with black
environment.infomap = environment.map.copy()
environment_originalmap =  environment.map.copy()
running = True 

feature_detection = True
break_point_ind = 0

while running:
	#print("Start from begining \n")
	sensor_on = False
	#environment.infomap = environment.map.copy()
	environment.infomap = environment_originalmap.copy()
	feature_detection = True
	break_point_ind = 0
	endpoints = [(0,0),(0,0)]
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
			print("\nNew seed segment ROUND break_point_ind = {0} ,NP = {1}".format(break_point_ind,feature_map.NP))
			print(seedSeg)
			if seedSeg == False:
				break
			else:
				seedSegment = seedSeg[0]
				predicted_points_todraw = seedSeg[1]
				indices  =seedSeg[2]
				print("seed segment SUCCESS break_point_ind at seed segment: ",break_point_ind)
				results = feature_map.seed_segment_growing(indices, break_point_ind)
				if results == False:
					break_point_ind = indices[1]
					print("seed segment growing FAIL break_point_ind next: ",break_point_ind)
					continue
				else:
					line_seg 		= results[0] #0
					outermost 		= results[1] #2
					break_point_ind = results[2] #3
					line_eq 		= results[3] #4
					m,b 			= results[4] #5
					print("seed segment growing SUCCESS break_point_ind: ",break_point_ind)					
					endpoints[0] =feature_map.projection_point2line(outermost[0],m,b)
					endpoints[1] = feature_map.projection_point2line(outermost[1],m,b)
					color = random_color()
					for point in line_seg:
						environment.infomap.set_at((int(point[0][0]),int(point[0][1])),(0,255,0))
						pygame.draw.circle(environment.infomap,color,(int(point[0][0]),int(point[0][1])),2,0)

					print("DRAW line m= {0}, b= {1}, start= {2}, end= {3}, position = {4}".format(m,b,endpoints[0],endpoints[1],position))
					pygame.draw.line(environment.infomap,(255,0,0),endpoints[0],endpoints[1],2)

					#environment.data_storage(data)	

	environment.map.blit(environment.infomap,(0,0)) #dr
	pygame.display.update() # update the screen