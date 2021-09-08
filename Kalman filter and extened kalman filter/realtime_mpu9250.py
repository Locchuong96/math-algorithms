import numpy as np
import mpu9250 as mpu
import EKF_filter as f

def init(sensor):
	
	data = sensor.read_data()
	data = np.array([data])
	x_init = data.T

	return x_init

if __name__ == "__main__":

	mpu_9250 = mpu.serial_mpu9250()

	x_init = init(mpu_9250)
	print(" x_init \n",x_init)
	#print(x_init.shape)

	f_ekf = f.EKF_sensor(x_init,nval = 9)

	z = mpu_9250.read_data()
	z = np.array([z])
	z = z.T

	x_hat = f_ekf.calc_hat(z)

	print(" x_hat \n",x_hat)

	mpu_9250.close()