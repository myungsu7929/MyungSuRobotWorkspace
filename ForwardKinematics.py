from base_utils.data import *


class DHparam():
    DH_list = []
    Operator_list = []
    
    def calc_endpoint(starting_point:Vector)->Vector:
        for param in DHparam.DH_list:
            screw_x = param.get_screw_x()
            screw_z = param.get_screw_z()
            DHparam.Operator_list.append(screw_x)
            DHparam.Operator_list.append(screw_z)
        DHparam.Operator_list.reverse()
        result = starting_point
        for operator in DHparam.Operator_list:
            result = operator._(result)
        return result
        
    def clear_DHlist():
        DHparam.DH_list.clear()

    def __init__(self, a, alpha:Angle, d, theta:Angle):
        self.ai_1 = a
        self.alphai_1 = alpha
        self.d = d
        self.theta = theta
        
        DHparam.DH_list.append(self)
 
    def update_a(self, value):
        self.ai_1 = value
    
    def update_alpha(self, value, unit="rad"):
        if isinstance(value, Angle):
            self.alphai_1 = value
        else:
            self.alphai_1.set_value(value, unit)
    
    def update_d(self,value):
        self.d = value
        
    def update_theta(self, value, unit="rad"):
        if isinstance(value, Angle):
            self.theta = value
        else:
            self.theta.set_value(value, unit)

    def get_screw_x(self)->OperatorMat:
        return OperatorMat(GaussRoll(self.alphai_1), Vector(self.ai_1,0,0)) 
    
    def get_screw_z(self)->OperatorMat:
        return OperatorMat(GaussYaw(self.theta), Vector(0,0,self.d))



if __name__ == "__main__":
    import time
    tic = time.time()
    DHparam(0, Angle(180,"deg"),156.4,Angle(0,"deg"))
    DHparam(0, Angle(90,"deg"),128.4,Angle(0,"deg"))
    DHparam(0, Angle(180,"deg"),410,Angle(0,"deg"))
    DHparam(0, Angle(90,"deg"),208.4,Angle(0,"deg"))
    DHparam(0, Angle(-90,"deg"),105.9,Angle(0,"deg"))
    DHparam(0, Angle(90,"deg"),105.9,Angle(0,"deg"))

  
    a = DHparam.calc_endpoint(Vector(0,0,0))
    toc = time.time()

    print(a)

                                                                                                                                                                                                                                                                                                                                                                                                                                                               
