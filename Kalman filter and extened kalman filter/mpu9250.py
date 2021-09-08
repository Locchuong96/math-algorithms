import serial  
from datetime import datetime
import time
import numpy as np
import struct  

class serial_mpu9250():
	def __init__(self,portname = 'COM5',baudrate = 115200,numbytes = 4,numparams = 9,timeout = 3 ):
		self.portname  = portname   
		self.baudrate  = baudrate  
		self.numbytes  = numbytes
		self.datatype  = None
		
		if self.numbytes == 2:
			self.datatype = 'h' # 2 bytes integer
		elif self.numbytes == 4:
			self.datatype = 'f' # 4 bytes float 
		
		self.numparams = numparams
		self.timeout   = timeout 
		self.rawdata = bytearray(self.numparams * self.numbytes)  

		print("Creating 8N1 connection to sensor ... ")
		try:
			self.con = serial.Serial(self.portname,self.baudrate,timeout = self.timeout)
			print("Connection Success!")
		except Exception as e:
			print("Connection failed: " + e)

	def read_data(self):
		
		#time.sleep(1.0)  # give some buffer time for retrieving data
		
		self.con.reset_input_buffer()
		
		self.con.readinto(self.rawdata)

		self.data = []

		for j in range(self.numparams):
			byte = self.rawdata[j*self.numbytes:(j+1)*self.numbytes]
			value, = struct.unpack(self.datatype,byte)
			self.data.append(value)

		return self.data

	def close(self):
		self.con.close()
		print("Disconnected ...")
