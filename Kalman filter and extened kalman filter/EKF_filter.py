import numpy as np 

class EKF_sensor:
    def __init__(self,x_init,nval=6):
        """
        INPUT
        Using for MPU6050,MPU9250, etc,... 
        nval   : number of elements in the state space vector    
        x_init : state space vector, contain one or multi target's values
        """
        self.nval = nval                  # number of elements in the state space vector 
        self.x_init = x_init              # state space vector               shape (nval,1) 
        """
        INITIALIZE
        You can custom the default value follow your systems
        """
        self.P_init =np.eye(nval)         # covariance matrix                shape (nval,nval)
        self.A = np.eye(nval)             # transmission matrix              shape (nval,nval)
        self.B = np.ones((nval,nval))      # control matrix                   shape (nval,nval)
        self.H = np.ones((nval,nval))      # measurement matrix               shape (nval,nval)
        self.w = np.ones((nval,1)) * 1e-2  # bias of the sensors input values shape (nval,1)
        
        self.x_hat = self.x_init          # predicted value                  shape (nval,1)
        self.P_hat = self.P_init          # covariance matrix                shape (nval,nval)
        
        self.Q = np.eye(nval) * 1e-4      # system noise matrix              shape (nval,nval)
        self.R = np.eye(nval)             # mesurement noise matrix          shape (nval,nval)
        self.v = np.ones((nval,1)) * 1e-3  # observation noise                shape (nval,1)
        self.u = np.zeros((nval,1))       # control vector                   shape (nval,1)

        #print(self.nval)
    
    def calc_hat(self,z):
        # Read the sensor input
        self.z = z                        # sensor's input value vector      shape (nval,1)
        # Calculate
        # predict the next state A @ x_hat + B @ u + v
        self.x_hat = self.A @ self.x_hat + self.B @ self.u + self.v 
        # calculate corvariance matrix sigma_hat = A @ sigma_hat @ A.T + Q
        self.P_hat = self.A @ self.P_hat @ self.A.T + self.Q
        # calculate the measurement residual y = z - ( H @ x_hat + w).T
        self.y     = self.z - (self.H @ self.x_hat + self.w) # residual measurement vector shape (nval,1)
        # calculate measurement residual covariance S = H @ P @ H.T + R
        self.S     = self.H @ self.P_hat @ self.H.T + self.R     # residual measurement convariance matrix shape(nval,nval)
        # calculate the kalman gain K = P @ H @ S^-1
        self.K     = self.P_hat @ self.H @ np.linalg.inv(self.S) # Kalman gain vector shape (nval,nval)
        # caclculate and update state estimate x_hat = x_hat + K @ y
        self.x_hat = self.x_hat + self.K @ self.y
        # caclculate and update covariance matrix P = (1 - K @ H) @ P 
        self.P_hat = (np.eye(self.nval) - self.K @ self.H) @ self.P_hat  
        
        return self.x_hat