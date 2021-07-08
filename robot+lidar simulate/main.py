import env
import sensor
import pygame 
import math

environment = env.build_environment((1200,600))
running = True

original_map = environment.map.copy()

lidar = sensor.lidar_sensor(200,original_map,distance_sigma = 0.01,angle_sigma = 0.01)
environment.map.fill((0,0,0))

running = True

while running:
	sensorOn = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if pygame.mouse.get_focused():
			sensorOn = True
		elif not pygame.mouse.get_focused():
			sensorOn = False

	if sensorOn:
		position       = pygame.mouse.get_pos()
		lidar.position = position
		sensor_data    = lidar.scan()
		environment.data_storage(sensor_data)
		environment.show_sensordata()
	environment.map.blit(environment.infomap,(0,0))

	pygame.display.update()




	pygame.display.update()