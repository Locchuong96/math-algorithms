import numpy as np 
import Quaternion_simple as quat 
#Node stores each point of block
class Node:
	def __init__(self,coordinates,color):
		self.x = coordinates[0]
		self.y = coordinates[1]
		self.z = coordinates[2]
		self.color = color

#Face stores 4 nodes that make up a face of the block
class Face:
	def __init__(self,nodes,color):
		self.nodeIndexes = nodes
		self.color = color

# Wireframe stores the details of the block
class Wireframe:
	def __init__(self):
		self.nodes = []
		self.edges = []
		self.faces = []
		#self.quaternion = quat.Quaternion() #create a quaternion
		self.sys = quat.System()

	def addNodes(self,nodeList,colorList):
		for node,color in zip(nodeList,colorList):
			self.nodes.append(Node(node,color))

	def addFaces(self,faceList,colorList):
		for indexes,color in zip(faceList,colorList):
			self.faces.append(Face(indexes,color))

	def outputNodes(self):
		print("\n---Nodes---")
		for i,node in enumerate(self.nodes):
			print("id: %d Position: (%.2f,%2.f,%2.f) \t Color: (%d, %d, %d)" % 
					(i,node.x,node.y,node.z,node.color[0],node.color[1],node.color[2]))

	def outputFaces(self):
		print("\n---Faces---")
		for i,face in enumerate(self.faces):
			print("id: %d: \t Color (%.2f,%.2f,%.2f)" % (i,face.color[0],face.color[1],face.color[2]))
			for nodeIndex in face.nodeIndexes:
				print("\t Node %d" % nodeIndex)

	#Add new function for quaternion
	
	def quatRotate(self,w,a,m,dt):
		#self.quaternion.rotate(w,dt)
		self.sys.predict(w,dt)
		self.sys.update(a,m)

	def rotatePoint(self,point):
		#rotationMat = quat.getRotMat(self.quaternion.q)
		rotationMat = quat.getRotMat(self.sys.xHat[0:4])
		return np.matmul(rotationMat,point)

	def convertToComputerFrame(self,point):
		computerFrameChangeMatrix = np.array([[-1,0,0],[0,0,-1],[0,-1,0]])
		return np.matmul(computerFrameChangeMatrix,point)

	def getAttitude(self):
		#return quat.getEulerAngles(self.quaternion.q)
		return quat.getEulerAngles(self.sys.xHat[0:4])

