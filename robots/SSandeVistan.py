
from base_utils.data import *
import numpy as np
import math

class SSandeVistanOptimizer():
    def __init__(self):
        self.D = 100.
        self.L1 = 305.941
        self.L2 = 300.
        self.update_rate = 1

    def grad_x1(self, theta1, theta2, theta3):
        result = (self.L1*np.sin(theta2)+self.L2*np.sin((theta2+theta3)))*np.sin(theta1)
        return result

    def grad_x2(self, theta1, theta2, theta3):
        result = (-1*self.L1*np.cos(theta1)-self.L2*np.cos(theta2+theta3))*np.cos(theta3)
        return result

    def grad_x3(self, theta1, theta2, theta3):
        result = -self.L2*np.cos(theta2+theta3)*np.cos(theta1)
        return result

    def grad_y1(self, theta1, theta2, theta3):
        result = -1 * (self.L1*np.sin(theta2)+self.L2*np.sin((theta2+theta3)))*np.cos(theta1)
        return result

    def grad_y2(self, theta1, theta2, theta3):
        result = (-1*self.L1*np.cos(theta1)-self.L2*np.cos(theta2+theta3))*np.sin(theta3)
        return result

    def grad_y3(self, theta1, theta2, theta3):
        result = -300*np.cos(theta2+theta3)*np.sin(theta1)
        return result

    def grad_z1(self, theta1, theta2, theta3):
        return 0.

    def grad_z2(self, theta1, theta2, theta3):
        result = -self.L1*np.sin(theta2) -self.L2*np.sin(theta2+theta3)
        return result

    def grad_z3(self, theta1, theta2, theta3):
        result = -1*self.L2*np.sin(theta2+theta3)
        return result

    def Javcobian(self, angle1:Angle, angle2:Angle, angle3:Angle)->np.array:
        angle1.to_rad()
        angle2.to_rad()
        angle3.to_rad()

        jacobian = np.array([[self.grad_x1(angle1.value, angle2.value, angle3.value), self.grad_y1(angle1.value, angle2.value, angle3.value), self.grad_z1(angle1.value, angle2.value, angle3.value)],
                             [self.grad_x2(angle1.value, angle2.value, angle3.value), self.grad_y2(angle1.value, angle2.value, angle3.value), self.grad_z2(angle1.value, angle2.value, angle3.value)],
                             [self.grad_x3(angle1.value, angle2.value, angle3.value), self.grad_y3(angle1.value, angle2.value, angle3.value), self.grad_z3(angle1.value, angle2.value, angle3.value)]])
        return jacobian

    def get_updated_angle(self, cur_pos:Vector, dst_pos:Vector, theta1:Angle, theta2:Angle, theta3:Angle)-> tuple:
        derivative = 2*np.matmul(self.Javcobian(theta1, theta2, theta3), (dst_pos.arr-cur_pos.arr))

        theta2.set_value(theta2.value - derivative[1]*self.update_rate, unit='rad')
        theta3.set_value(theta3.value - derivative[2]*self.update_rate, unit='rad')
        theta1.set_value(theta1.value - derivative[0]*self.update_rate, unit='rad')
        
        return (theta1, theta2 ,theta3)


