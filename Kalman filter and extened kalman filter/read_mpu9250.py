import serial  
from datetime import datetime
import time
import numpy as np
import pandas as pd
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
		print(self.rawdata)  
		self.data = []

		print("Creating 8N1 connection to sensor ... ")
		try:
			self.con = serial.Serial(self.portname,self.baudrate,timeout = self.timeout)
			print("Connection Success!")
		except Exception as e:
			print("Connection failed: " + e)

	def read_data(self,time_collect):
		time.sleep(1)  # give some buffer time for retrieving data
		self.con.reset_input_buffer()

		print("Collecting data in %d seconds..." %time_collect)
		start_time = datetime.now()

		# block program and collect data
		while((datetime.now() - start_time).total_seconds() < time_collect):
			self.con.readinto(self.rawdata)
			self.data.append(self.rawdata[:]) # NOT self.data.append(self.rawdata)

		print("Exporting data in  ...")
		
		sensor_data = []

		for row_bytes in self.data:
			#print(row_bytes)
			row = []
			for j in range(self.numparams):
				byte = row_bytes[j*self.numbytes:(j+1)*self.numbytes]
				value, = struct.unpack(self.datatype,byte)
				row.append(value)
			
			sensor_data.append(row)

		df = pd.DataFrame(sensor_data,columns= ['gx','gy','gz','ax','ay','az','mx','my','mz'])

		df.to_csv('mpu9250.csv')

		print('Exported!')

	def close(self):
		self.con.close()
		print("Disconnected ...")

def main():
	sensor = serial_mpu9250()
	sensor.read_data(20)
	sensor.close()

if __name__ == "__main__":
	main()
