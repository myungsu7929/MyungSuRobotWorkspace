import os
import sys
sys.path.append(__path__)
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from sdk import *
from ..import *

# ADDR_TORQUE_ENABLE          = 64
# ADDR_GOAL_POSITION          = 116
# ADDR_PRESENT_POSITION       = 132
# DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
# DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
# BAUDRATE                    = 4500000
# PROTOCOL_VERSION            = 2.0
# DEVICENAME                  = '/dev/ttyUSB0'

# portHandler = PortHandler(DEVICENAME)
# packetHandler = PacketHandler(PROTOCOL_VERSION)
# if portHandler.openPort():
#     print("success to open port")

class DynamixelSocket():
    def __init__(self):
        self.torque_enable_addr = 64
        self.goal_pos_addr = 116
        self.cur_pos_addr = 132
        self.baudrate = 20000000
        self.device_name = '/dev/ttyUSB0'

        self.port_handler = PacketHandler(self.device_name)
        self.packet_handler = PacketHandler(2.0)

        if self.portHandler.openPort():
                print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            quit()
            
            
            # Set port baudrate
        if self.portHandler.setBaudRate(self.baudrate):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()

    def deg2pulse(self, angle:Angle)->int:
        angle.to_deg()
        pulse = int(angle.value / 0.088)
        return pulse
    
    def pulse2deg(self, pulse_value:int)->float:
        deg_value = pulse_value*0.088
        return deg_value

    def read_pos(self, id):
        data, comm_result, err = self.packet_handler.read4ByteTxRx(self.port_handler, id, self.cur_pos_addr)
        return Angle(self.pulse2deg(data), 'deg')

    def set_pos(self, id, angle):
        pulse_value = self.deg2pulse(angle)
        


    def torque_on(self, id):
        comm_result, err = self.packet_handler.write1ByteTxRx(self.port_handler, id, self.torque_enable_addr, 1)
    def torque_off(self, id):
        comm_result, err = self.packet_handler.write1ByteTxRx(self.port_handler, id, self.torque_enable_addr, 0)
    


class MotorInterface():
    socket = DynamixelSocket()
    def __init__(self, motor_id, angle_offset=180):
        self.id = motor_id
        self.offset = Angle(angle_offset, 'deg')

    
    def set_pos(self, angle:Angle)->None:
        actual_value = angle +  self.offset
        MotorInterface.socket.set_pos(self.id , actual_value)
    
    def get_pos(self):
        result = MotorInterface.socket.read_pos(self.id)
     
        return result -self.offset
    
    def turn_on(self):
        MotorInterface.socket.torque_on(self.id)
    
    def turn_off(self):
        MotorInterface.socket.torque_off(self.id)

if __name__ == "__main__":
    motor = MotorInterface(0)


