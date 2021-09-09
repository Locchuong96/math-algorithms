from threading import Thread
import serial  
import time  
import struct
import numpy as np

class SerialRead:
	def __init__(self,serialPort ='COM5', serialBaud = 115200, dataNumBytes = 4, numParams = 9):

		self.port = serialPort # PortName
		self.baud = serialBaud # the speed of transmition
		self.dataNumBytes = dataNumBytes
		self.rawData = bytearray(numParams * dataNumBytes)
		self.dataType = None # float or integer 
		if dataNumBytes == 2:
			self.dataType = 'h' # 2 bytes integer
		elif dataNumBytes == 4:
			self.dataType = 'f' # 4 bytes float
		self.numParams = numParams
		self.data = np.zeros(numParams) # the list of gyro, acc, mag after math
		self.isRun = True  # Flag to create a thread
		self.isReceiving = False # Flag receive data, True if receiving data
		self.thread = None

		print('Trying to connect to: ' + str(serialPort) + ' at ' + str(serialBaud) + 'BAUD.')
		try:
			# create a serial connection
			self.serialConnection = serial.Serial(serialPort,serialBaud,timeout = 3)
			print('Connected to ' + str(serialPort) + ' at ' + str(serialBaud) + 'BAUD.')
		except:
			print("Failed to connect with " + str(serialPort) + ' a ' + str(serialBaud) + 'BAUD.')
			exit() # exit the python program

	# create a thread to read data
	def readSerialStart(self):
		#create a thread
		if self.thread == None:
			self.thread = Thread(target = self.backgroundThread)
			# start the thread
			self.thread.start()
			#Block until we start receiving values
			while self.isReceiving != True:
				# continue the main if is Flag isReciving = True 
				time.sleep(0.1)

	# create the function execute from the tread
	def backgroundThread(self): # retrieve data
		time.sleep(1.0) #give some buffer time for retrieving data
		# reset the buffer input
		self.serialConnection.reset_input_buffer()
		#This loop keep runing in the thread
		while (self.isRun): 
			# read the buffer input the N bytes and storage it into rawData
			self.serialConnection.readinto(self.rawData)
			# set the flag isReceiving True to continue the main
			self.isReceiving = True 

	# close the thread and connection
	def close(self):
		self.isRun = False # stop read raw data
		self.thread.join() # wait until the thread is terminated
		self.serialConnection.close() # close the connection
		print('Disconnected...')

	# create a function execute data
	def getSerialData(self):
		# copy the private data
		privateData = self.rawData[:]
		# loop over each byte
		for i in range(self.numParams): 
			data_bytes = privateData[(i * self.dataNumBytes) : (i * self.dataNumBytes + self.dataNumBytes)]
			# create value follow dataType
			value, = struct.unpack(self.dataType,data_bytes)
			if i == 0: 
				value = (value - 1.2) * -np.pi/180 # gyro gx - bias deg/s - > rad/s
			elif i == 1: 
				value = (value - 0.5) * -np.pi/180 # gyro gy - bias deg/s - > rad/s
			elif i == 2: 
				value = (value + 8.1) * -np.pi/180 # gyro gz - bias deg/s - > rad/s
			elif i == 3: 
				value = value #  acceleration x
			elif i == 4: 
				value = value #  acceleration y
			elif i == 5: 
				value = value #  acceleration z
			elif i == 6: 
				value = value #  mag x
			elif i == 7: 
				value = value #  mag y
			elif i == 8: 
				value = value #  mag z

			#write down the data
			self.data[i] = value

		return self.data









