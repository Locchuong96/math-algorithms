import env
import sensors
import pygame 
import math 

environment = env.buildEnvironment((1200,600))
originalMap = environment.map.copy()
laser = sensors.LaserSensor(200,originalMap , uncertainty = (0.5,0.01))
environment.map.fill((0,0,0)) 
environment.infomap = environment.map.copy()

running = True

while running: 
	sensorOn = False 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if pygame.mouse.get_focused():
			sensorOn = True
		elif not pygame.mouse.get_focused():
			sensorON = False 
	if sensorOn:
		position = pygame.mouse.get_pos()
		laser.position = position
		sensor_data = laser.sense_obstacles()
		environment.dataStorage(sensor_data)
		environment.show_sensorData()
	environment.map.blit(environment.infomap,(0,0))

	pygame.display.update() 
