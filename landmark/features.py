import numpy as np 
import math 
from fractions import Fraction
from scipy.odr import *

#landmark
Landmarks = []

class features_detection:
	def __init__(self):
		# variables
		self.EPSILON 		= 10
		self.DELTA 			= 501
		self.SNUM 			= 6
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
		self.FEATURES       = [] # for land mark

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
		self.NP =  len(self.LASERPOINTS) -1

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

	def seed_segment_detection(self,robot_position,break_point_ind):
		flag = True
		self.NP = max(0,self.NP)
		self.SEED_SEGMENTS = []

		for i in range(break_point_ind,(self.NP - self.PMIN)):
			predicted_points_to_draw = []
			j = i + self.SNUM
			m,b = self.odr_fit(self.LASERPOINTS[i:j])
			params = self.lineform_Si2G(m,b)

			for k in range(i,j):
				predicted_point = self.predict_point(params,self.LASERPOINTS[k][0], robot_position)

				d1 = self.dist_point2point(predicted_point,self.LASERPOINTS[k][0])
				if d1 > self.DELTA:
					flag = False
					break 

				d2 = self.dist_point2line(params,predicted_point)
				if d2 > self.EPSILON:
					flag = False
					break

				predicted_points_to_draw.append(predicted_point)

			if flag:
				self.LINE_PARAMS = params
				return [self.LASERPOINTS[i:j], predicted_points_to_draw,(i,j)]

		return False

	def seed_segment_growing(self,indices,break_point):
		line_eq = self.LINE_PARAMS
		i,j = indices
		# Beginning and Final points in the line segment
		PB = max(break_point,i-1)
		PF = min(j+1,len(self.LASERPOINTS) -1)
		
		while self.dist_point2line(line_eq,self.LASERPOINTS[PF][0]) < self.EPSILON:
			if PF > self.NP -1:
				break 
			else:
				m,b = self.odr_fit(self.LASERPOINTS[PB:PF])
				line_eq  = self.lineform_Si2G(m,b)
				POINT = self.LASERPOINTS[PF][0]

			PF = PF + 1 
			NEXTPOINT = self.LASERPOINTS[PF][0]

			if self.dist_point2point(POINT, NEXTPOINT) > self.GMAX:
				break

		PF = PF -1 

		while self.dist_point2line(line_eq,self.LASERPOINTS[PB][0]) <self.EPSILON:
			if PB < break_point: 
				break 
			else:
				m,b = self.odr_fit(self.LASERPOINTS[PB:PF])
				line_eq = self.lineform_Si2G(m,b)
				POINT = self.LASERPOINTS[PB][0]

			PB = PB - 1 
			NEXTPOINT  = self.LASERPOINTS[PB][0]
			if self.dist_point2point(POINT,NEXTPOINT) > self.GMAX:
				break 
		PB = PB + 1 
		LR = self.dist_point2point(self.LASERPOINTS[PB][0], self.LASERPOINTS[PF][0])
		PR = len(self.LASERPOINTS[PB:PF])

		if (LR >= self.LMIN) and (PR >= self.PMIN):
			self.LINE_PARAMS = line_eq
			m,b = self.lineform_G2Si(line_eq[0],line_eq[1],line_eq[2])
			#self.two_points = self.line_2points(m,b)
			self.LINE_SEGMENTS.append((self.LASERPOINTS[PB + 1][0], self.LASERPOINTS[PF - 1][0]))
			return  [self.LASERPOINTS[PB:PF],(self.LASERPOINTS[PB+1][0], self.LASERPOINTS[PF-1][0]), PF, line_eq,(m,b)]

		else:
			return False

	def linefeats_2point(self):
		new_rep = [] # the new representation of the features

		for feature in self.FEATURES:
			#[[m,b],endpoints]
			projection = self.projection_point2line((0,0),feature[0][0],feature[0][1])
			new_rep.append([feature[0],feature[1],projection])

		return new_rep

def dist_point2point(point1, point2):
	px = (point1[0] - point2[0]) ** 2
	py = (point1[1] - point2[1]) ** 2
	return math.sqrt(px + py)

def is_overlap(seg1,seg2):
	lenght1 = dist_point2point(seg1[0],seg1[1])
	lenght2 = dist_point2point(seg2[0],seg2[1])
	center1 = ( (seg1[0][0] + seg1[1][0])/2 , (seg1[0][1]+seg1[1][1])/2 )
	center2 = ( (seg2[0][0] + seg2[1][0])/2 , (seg2[0][1]+seg2[1][1])/2 )
	dist = dist_point2point(center1,center2)
	if dist > (lenght1 + lenght2)/2:
		return False
	else:
		return True

def landmark_association(landmarks):

	thresh = 10
	for l in landmarks:
		flag = False

		for i,Landmark in enumerate(Landmarks):
			#[[ [m,b], endpoints, projection_point ],...]
			dist = dist_point2point( l[2] , Landmark[2] )
			if dist < thresh:
				if not is_overlap(l[1],Landmark[1]):
					continue
				else:
					Landmarks.pop(i)
					Landmarks.insert(i,l)
					flag = True 
					break 
		if not flag:
			Landmarks.append(l)































