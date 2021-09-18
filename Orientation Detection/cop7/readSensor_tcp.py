import requests
from threading import Thread
import numpy as np
import time

class TcpRead:

	def __init__(self,url = "http://192.168.1.11",numParams = 9,timeout = 2):

		self.url = url # sensor url 
		self.numParams = numParams # data value
		self.timeout = timeout 
		self.data = np.zeros(numParams) # the list of the gyro,acc,mag after math
		self.isRun = True # Flag to create a thread
		self.isReceiving = False # Flag receive data, True is receiving data
		self.thread = None

		print('Trying to connect to: ' + url)
		try:
			res = requests.get(self.url,timeout = self.timeout)
		except Exception as e:
			print('Connect to: ' + url + " FAILED")
			exit() # exit the python program

	def readtcpStart(self):
		# create a thread
		if self.thread == None:
			self.thread = Thread(target = self.backgroundThread)
			# start the thread
			self.thread.start()
			# block unitl we start receiving values
			while self.isReceiving != True:
				# continue the main if the Flag isReciving = True
				time.sleep(0.1)

	def backgroundThread(self):
		while (self.isRun):
			try:
				res = requests.get(self.url,timeout = self.timeout)
				imu = res.json()
				self.data[0] = imu['ax']
				self.data[1] = imu['ay']
				self.data[2] = imu['az']
				self.data[3] = (imu['gy'] - 1.25) * -np.pi/180
				self.data[4] = (imu['gx'] - 0.3) * -np.pi/180
				self.data[5] = (imu['gz'] + 8.15) * np.pi/180
				self.data[6] = imu['mx']
				self.data[7] = imu['my']
				self.data[8] = imu['mz']
				self.isReceiving = True
				# print(self.data)
			except:
				pass

	def close(self):
		self.isRun = False
		self.thread.join()
		print(self.url + " Disconnected...")





