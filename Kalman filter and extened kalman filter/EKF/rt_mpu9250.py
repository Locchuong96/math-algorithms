import numpy as np
import mpu9250 as mpu
import EKF_filter as f

mpu_9250 = mpu.tcp_mpu9250()

z = [0,0,0,0,0,0,0,0,0] #mpu_9250.read_data()
z = np.array([z])
x_init = z.T

f_ekf = f.EKF_sensor(x_init,nval = 9)

if __name__ == "__main__":

	while True:

		z = mpu_9250.read_data()
		z = np.array([z])
		z = z.T

		x_hat = f_ekf.calc_hat(z)

		print(" x_hat \n",x_hat)