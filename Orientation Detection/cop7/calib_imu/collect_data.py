from datetime import datetime 
import serial
import struct
import numpy as np 
import copy
import time 

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

		# variable for storage the sensor data
		self.dataBlock = []
		self.data = []
		for i in range(self.numParams):
			self.data.append([])

		print('Trying to connect to: ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
		try:
			# create a serial connection
			self.serialConnection = serial.Serial(serialPort,serialBaud,timeout = 3)
			print('Connected to ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
		except:
			print("Failed to connect with " + str(serialPort) + ' a ' + str(serialBaud) + ' BAUD.')
			exit() # exit the python program

	def close(self):
		self.serialConnection.close()
		print('Disconnected ...')

	def getSerialData(self,collect_time):
		print("Wave your sensor around  %d seconds" % collect_time)
		print("Collecting data ...")
		# clear the the buffer input
		self.serialConnection.reset_input_buffer()
		# assign the startTime
		startTime = datetime.now()
		#keep read the sensor data unit the collect_time
		while (datetime.now() - startTime).total_seconds() <collect_time:
			self.serialConnection.readinto(self.rawData)
			self.dataBlock.append(self.rawData[:])

		print("Captured data for %d seconds" % collect_time)
		#close the connection
		self.close()
		print("Processing data ...")

		#export data to csv file
		for i in range(len(self.dataBlock)):
			for j in range(self.numParams):
				byteData = self.dataBlock[i][(j * self.dataNumBytes):(( j + 1) * self.dataNumBytes)]
				value, = struct.unpack(self.dataType,byteData)
				self.data[j].append(copy.copy(value))

		print("Exporting data ...")
		csvData = np.flip(np.array(self.data),1).transpose()
		np.savetxt('magnetometer.csv',csvData,delimiter = ',',fmt = '%i')
		print('Done')


def main():
	portName = 'COM5'
	baudRate = 115200
	dataNumBytes = 4
	numParams = 9 
	s = SerialRead(portName,baudRate,dataNumBytes,numParams)
	time.sleep(2)
	s.getSerialData(30)

if __name__ == '__main__':
	main()






