import numpy as np 
import math 
from fractions import Fraction
from scipy.odr import *

LANDMARKS = []

class features_detection:
	def __init__(self):
		# variables
		self.EPSILON 		= 10
		self.DELTA 			= 501
		self.SNUM 			= 4
		self.PMIN 			= 20
		self.GMAX 			= 20
		self.SEED_SEGMENTS 	= []
		self.LINE_SEGMENTS 	= []
		self.LASERPOINTS 	= []
		self.LINE_PARAMS 	= None
		self.NP 			= len(self.LASERPOINTS) -1
		self.LMIN 			= 20 # minimum lenght of line segment 
		self.LR             = 0  # real lenght of line segment
		self.PR             = 0  #the number of laser points contained in the line segment

	# euclidian distance from point1 to point2
	def dist_point2point(self, point1, point2):
		px = (point1[0] - point2[0]) ** 2
		py = (point1[1] - point2[1]) ** 2
		return math.sqrt(px + py)

	# distance point to line written in general form
	def dist_point2line(self,params,point):
		A,B,C = params
		distance = abs(A * point[0] + B * point[1] + C)/math.sqrt(A**2 + B**2)
		return distance

	# general form to slope-intercept Ax + By + C = 0
	def lineform_G2Si(self,A,B,C):
		m = -A / B  
		b = -C / B
		return m,b

	# slope-intercepts to general form
	def lineform_Si2G(self,m,b):
		A,B,C = -m,1,-b
		if A < 0:
			A,B,C =  -A,-B,-C
		den_a = Fraction(A).limit_denominator(1000).as_integer_ratio()[1]
		den_c = Fraction(C).limit_denominator(1000).as_integer_ratio()[1]
		gcd = np.gcd(den_a,den_c) # uoc chung lon nhat
		lcm = den_a * den_c / gcd # boi chung nho nhat
		A = A * lcm #
		B = B * lcm
		C = C * lcm 
		return A,B,C

	# extract two points from a line equation under the slope intercepts form y = mx + b ( m: slope, b : intercept )
	def line_2points(self,m,b):
		x = 5
		y = m * x + b 
		x2 = 2000 
		y2 = m * x2 + b 
		return [(x,y),(x2,y2)]

	# from two point return a line form slope and intercept
	def points_2line(self,point1,point2):
		m,b = 0,0
		if point2[0] == point1[0]:
			pass
		else:
			m = (point2[1] - point1[1])/(point2[0] - point1[0])
			b = point2[1] - m * point2[0]
		return m,b

	# find the intersect point of two line
	def line_intersect_general(self, param1,param2):
		a1,b1,c1 = param1
		a2,b2,c2 = param2 
		x_intersection = (c1*b2 - b1*c2)/(b1*a2 - a1*b2)
		y_intersection = (a1*c2 - a2*c1)/(b1*a2 - a1*b2)
		return x_intersection,y_intersection

	# find the projection of point to line
	def projection_point2line(self,point,m,b):
		x,y = point
		m2 = -1/m 
		b2 = y - m2*x
		x_projection = -(b-b2)/(m-m2)
		y_projection = m2 * x_projection + b2
		return x_projection,y_projection

	# turn angle and distance into position
	def AD2pos(self,distance,angle,robot_position):
		x = distance * math.cos(angle) + robot_position[0]
		y = -distance * math.sin(angle) + robot_position[1]
		return x,y

	def laser_points_set(self,data):
		self.LASERPOINTS = []
		if not data:
			pass
		else:
			for point in data:
				coordinates = self.AD2pos(point[0],point[1],point[2])
				self.LASERPOINTS.append([coordinates,point[1]]) # (x,y) and angle
		#self.NP =  len(self.LASERPOINTS)

	# calculate the y value while given params slope and intercept and y
	def linear_func(self,params,x):
		m,b = params   
		return m * x + b 

	# ODR orthogonal distance regression
	def odr_fit(self,laser_points):
		x = np.array([i[0][0] for i in laser_points]) # laser_point = [[(x,y),angle]]
		y = np.array([i[0][1] for i in laser_points])

		#create a model for fitting
		linear_model = Model(self.linear_func) # from scipy

		#create a realdata object using our initiated data from above
		data = RealData(x,y) # from scipy

		#set up ODR with the model and data
		odr_model = ODR(data,linear_model,beta0 = [0.,0.])

		#run the regression
		out = odr_model.run()
		m,b = out.beta
		return m,b

	def predict_point(self,line_params,sensed_point,robot_position):
		m,b = self.points_2line(robot_position,sensed_point)
		params1 = self.lineform_Si2G(m,b)
		predx,predy = self.line_intersect_general(params1,line_params)
		return predx,predy

	def seed_segment_detection(self,robot_position):
		self.SEED_SEGMENTS 	= []
		self.LINE_SEGMENTS 	= []
		# self.LASERPOINTS
		# self.SNUM
		# print("NP: {0}, SNUM: {1}, NUMBER of line: {2}".format(self.NP,self.SNUM,self.NP//self.SNUM))
		index = 0
		for i in range(0,len(self.LASERPOINTS)//self.SNUM):
			if i == 0:
				self.SEED_SEGMENTS.append(self.LASERPOINTS[0:self.SNUM])

			else:
				index += self.SNUM
				self.SEED_SEGMENTS.append(self.LASERPOINTS[index: index + self.SNUM])

		self.SEED_SEGMENTS.append(self.LASERPOINTS[index + self.SNUM:])

		# detect line segment from seed segment
		for seed in self.SEED_SEGMENTS:
			#Check the element number in seed:
			if len(seed) == self.SNUM:
				m,b = self.odr_fit(seed)
				params = self.lineform_Si2G(m,b)
				flag = True

				for j in range(len(seed)):

					predicted_point = self.predict_point(params,seed[j][0],robot_position)

					d1 = self.dist_point2point(predicted_point,seed[j][0])

					if d1 > self.DELTA:
						flag = False
						break 

					d2 = self.dist_point2line(params,predicted_point)
					if d2 > self.EPSILON:
						flag = False
						break

					d3 = self.dist_point2point(seed[0][0],seed[-1][0])
					if d3 > self.GMAX:
						flag = False
						break

					if flag:
						start_point = self.projection_point2line(seed[0][0],m,b)
						end_point = self.projection_point2line(seed[-1][0],m,b)
						# calc the the projection point of (0,0) into the line (m,b)
						projection_point = self.projection_point2line((0,0),m,b)
						self.LINE_SEGMENTS.append((start_point,end_point,projection_point))


def dist_point2point(point1, point2):
	px = (point1[0] - point2[0]) ** 2
	py = (point1[1] - point2[1]) ** 2
	return math.sqrt(px + py)

def is_overlap(line1,line2):
	lenght1 = dist_point2point(line1[0],line1[1])
	lenght2 = dist_point2point(line2[0],line2[1])
	center1 = ( (line1[0][0] + line1[1][0])/2 , (line1[0][1]+line1[1][1])/2 )
	center2 = ( (line2[0][0] + line2[1][0])/2 , (line2[0][1]+line2[1][1])/2 )
	dist = dist_point2point(center1,center2)
	if dist > (lenght1 + lenght2)/2:
		return False
	else:
		return True


def landmark_association(line_segment):

	thresh = 10

	for l in line_segment:
		flag = False 
		
		if len(LANDMARKS) == 0:
			LANDMARKS.append(l)
		
		else:
			for i, landmark in enumerate(LANDMARKS):

				#print(l[2],landmark[2])

				dist = dist_point2point(l[2], landmark[2])
				
				#print(dist)

				if dist < thresh:
					if not is_overlap((l[0],l[1]),(landmark[0],landmark[1])):
						continue
					else:
						LANDMARKS.pop(i)
						LANDMARKS.insert(i,l)
						flag = True 
						break 

			if not flag:
				LANDMARKS.append(l)










































