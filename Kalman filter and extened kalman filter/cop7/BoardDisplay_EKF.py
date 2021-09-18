import Wireframe_EKF as wf
import readSensor_tcp as tcp
import pygame  
from operator import itemgetter 

def initializeBlock():
	block = wf.Wireframe()
	block_nodes = [(x,y,z) for x in (-1.5,1.5) for y in (-1,1) for z in (-0.1,0.1)] #list of (x,y,z)
	node_colors = [(255,255,255)] * len(block_nodes)
	block.addNodes(block_nodes,node_colors)
	block.outputNodes() #print out infomation of block
	faces = [(0, 2, 6, 4), (0, 1, 3, 2), (1, 3, 7, 5), (4, 5, 7, 6), (2, 3, 7, 6), (0, 1, 5, 4)]
	colors = [(255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0)]
	block.addFaces(faces,colors)
	block.outputFaces()

	return block

class ProjectionViewer:
	def __init__(self,width,height,wireframe):
		""" Display 3D objects on Pygame screen """
		self.width = width
		self.height = height 
		self.wireframe = wireframe #the block created by initializeBlock function
		self.screen = pygame.display.set_mode((width,height))
		pygame.display.set_caption("Attitude Determination using Quaternions")
		self.background = (10,10,50)
		self.clock = pygame.time.Clock()
		pygame.font.init()
		self.font = pygame.font.SysFont("Comic Sans MS",20)

	def run(self,sensorInstance):
		""" Create a pygame screen until it is closed """
		running = True 
		loopRate = 50
		# angularVelocity = [0.25,0.25,0.25] # set the gyro from sensor
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					sensorInstance.close() # close the connection sensor

			self.clock.tick(loopRate) # tick the internal block
			#angularVelocity = [sensorInstance.data[3],sensorInstance.data[4],sensorInstance.data[5]] # get the gyro from sensor
			self.wireframe.quatRotate([sensorInstance.data[0],sensorInstance.data[1],sensorInstance.data[2]],
										[sensorInstance.data[3],sensorInstance.data[4],sensorInstance.data[5]],
										[sensorInstance.data[6],sensorInstance.data[7],sensorInstance.data[8]], 1/loopRate) # dt = 1/loopRate
			self.display(sensorInstance)
			pygame.display.flip() # update the screen python

	# One vanishing point perspective view algorithm NOT USE
	def projectOnePointPerspective(self,x,y,z,win_width,win_height,P,S,scaling_constant,pvDepth):
		# In Pygame, the y axis is downward pointing
		# In order to make y point upwards, a rotation around x axis by 180 degrees is needed
		# This will result in y' = -y, z' = -z
		xPrime = x 
		yPrime = -y
		zPrime = -z
		xProjected = XPrime * (S/ (zPrime + P)) * scaling_constant + win_width/2  # move your object into center of screen
		yProjected = YPrime * (S/ (zPrime + P)) * scaling_constant + win_height/2 # move your object into center of screen
		pvDepth.append(1/(zPrime + P))
		return (round(xProjected),round(yProjected))

	#Normal projection
	def projectOthorgraphic(self,x,y,z,win_width,win_height,scaling_constant,pvDepth):
		# In Pygame, the y axis is downward pointing
		# In order to make y point upwards, a rotation around x axis by 180 degrees is needed
		# This will result in y' = -y, z' = -z
		xPrime = x 
		yPrime = -y
		xProjected = xPrime * scaling_constant + win_width /2
		yProjected = yPrime * scaling_constant + win_height /2
		# Note that there is no negative sign here because our rotation to computer frame
		# assumes that the computer frame is x-right, y-up, z-out
		# so this rotation z-coordinate below is already in the outward direction
		pvDepth.append(z)
		return (round(xProjected),round(yProjected))

	def messageDisplay(self,text,x,y,color):
		#display the message of angle on the screen
		textSurface = self.font.render(text,True,color,self.background)
		textRect = textSurface.get_rect()
		textRect.topleft = (x,y)
		self.screen.blit(textSurface,textRect) # draw a textRect with textSurface on the screen

	def display(self,sensorInstance):
		""" Draw wirefames on the screen. """
		self.screen.fill(self.background)

		#Get the current attitude
		roll, pitch, yaw = self.wireframe.getAttitude() # return the roll, pitch,yaw
		ax,ay,az,gy,gx,gz,mx,my,mz = sensorInstance.data  # get data of the sensor to display

		self.messageDisplay("Roll %.1f" % roll,self.screen.get_width()*0.75,self.screen.get_height()*0,(220,20,60))
		self.messageDisplay("Pitch %.1f" % pitch,self.screen.get_width()*0.75,self.screen.get_height()*0.05,(0,255,255))
		self.messageDisplay("Yaw %.1f" % yaw,self.screen.get_width()*0.75,self.screen.get_height()*0.1,(65,105,255))
		self.messageDisplay("Ax %.1f" % ax,self.screen.get_width()*0.75,self.screen.get_height()*0.15,(255,105,255))
		self.messageDisplay("Ay %.1f" % ay,self.screen.get_width()*0.75,self.screen.get_height()*0.2,(255,105,255))
		self.messageDisplay("Az %.1f" % az,self.screen.get_width()*0.75,self.screen.get_height()*0.25,(255,105,255))
		self.messageDisplay("Gx %.1f" % gx,self.screen.get_width()*0.75,self.screen.get_height()*0.3,(255,105,255))
		self.messageDisplay("Gy %.1f" % gy,self.screen.get_width()*0.75,self.screen.get_height()*0.35,(255,105,255))
		self.messageDisplay("Gz %.1f" % gz,self.screen.get_width()*0.75,self.screen.get_height()*0.4,(255,105,255))
		self.messageDisplay("Mx %.1f" % mx,self.screen.get_width()*0.75,self.screen.get_height()*0.45,(255,105,255))
		self.messageDisplay("My %.1f" % my,self.screen.get_width()*0.75,self.screen.get_height()*0.5,(255,105,255))
		self.messageDisplay("Mz %.1f" % mz,self.screen.get_width()*0.75,self.screen.get_height()*0.55,(255,105,255))
		
		# Transform nodes o perspective view
		dist = 5
		pvNodes = []
		pvDepth = []
		# loop over the nodes in block, caculate itself othographic value and storage in pvNodes
		for node in self.wireframe.nodes:
			
			point = [node.x,node.y,node.z] # create a point 
			newCoord = self.wireframe.rotatePoint(point) #rotate this point
			comFrameCoord = self.wireframe.convertToComputerFrame(newCoord)

			pvNodes.append(self.projectOthorgraphic(comFrameCoord[0],comFrameCoord[1],comFrameCoord[2],
								self.screen.get_width(),self.screen.get_height(),70,pvDepth))

			""" NOT USE
			pvNodes.append(self.projectOnePointPerspective(node.x,node.y,node.z,self.screen.get_width(),self.screen.get_height(),5,10,30,pvDepth))
			"""
			# storage the z value of node to pvDepth
			#pvDepth.append(node.z)

		#print("pvDepth",pvDepth)
		
		# Calculate the average Z values of each face 
		avg_z = []
		#loop over each face in the the block
		for face in self.wireframe.faces:
			n = pvDepth 
			# calculate the average z value of each face using nodeIndexes ex (2,6,4,0)
			z = (n[face.nodeIndexes[0]] + n[face.nodeIndexes[1]] + n[face.nodeIndexes[2]] + n[face.nodeIndexes[3]]) / 4.0 
			avg_z.append(z) 

		#print("avg_z",avg_z)

		# Draw the faces using the Painter's algorithm:
		for idx, val in sorted(enumerate(avg_z),key = itemgetter(1)):
			face = self.wireframe.faces[idx]
			pointList = [pvNodes[face.nodeIndexes[0]],
						pvNodes[face.nodeIndexes[1]],
						pvNodes[face.nodeIndexes[2]],
						pvNodes[face.nodeIndexes[3]]]

			#print(pointList)

			pygame.draw.polygon(self.screen,face.color,pointList)

if __name__ == "__main__":

	numParams = 9
	url = "http://192.168.1.8"
	timeout = 1
	s =  tcp.TcpRead(url = url,numParams = numParams,timeout = timeout)
	s.readtcpStart()

	block = initializeBlock()
	pv = ProjectionViewer(640,480,block)
	pv.run(s)



