import requests

class tcp_mpu9250():
	def __init__(self,url = "http://192.168.1.11"):
		self.url = url
		self.data = []
		self.ax = 0.0
		self.ay = 0.0
		self.az = 0.0
		self.gx = 0.0
		self.gy = 0.0
		self.gz = 0.0
		self.mx = 0.0
		self.my = 0.0
		self.mz = 0.0

	def read_data(self):

		self.data = []

		res = requests.get(self.url)

		json = res.json()

		self.ax = json['ax']
		self.ay = json['ay']
		self.az = json['az']

		self.gx = json['gx']
		self.gy = json['gy']
		self.gz = json['gz']

		self.mx = json['mx']
		self.my = json['my']
		self.mz = json['mz']

		self.data = [self.ax,self.ay,self.az,self.gx,self.gy,self.gz,self.mx,self.my,self.mz]

		return self.data
