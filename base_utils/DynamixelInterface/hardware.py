from base_utils.data import *
from DynamixelSocket.dynamixel_socket import DynamixelSocket


class MotorInterface():
    socket = DynamixelSocket()
    def __init__(self, motor_id, angle_offset=180):
        self.id = motor_id
        self.offset = Angle(angle_offset, 'deg')

    
    def set_pos(self, angle:Angle)->None:
        actual_value = angle +  self.offset
        MotorInterface.socket.set_pos(self.id , actual_value)
    
    def get_pos(self):
        return MotorInterface.socket.read_pos(self.id)
    
    def turn_on(self):
        MotorInterface.socket.turn_on(self.id)
    
    def turn_off(self):
        MotorInterface.socket.turn_off(self.id)
