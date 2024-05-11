import math
import numpy as np

    
class Length():
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value
    
    def set(self, x):
        self.value = x
    
    def __str__(self):
        return str(self.value)

    def get_mm(self):
        return self.value/1000.0
    
    def get_cm(self):
        return self.value/100.0
    
    def __add__(self, other):
        if not isinstance(other, Length):
            raise ValueError("lengh must calulate with Length Object")
        return Length(self.value + other.value)
    
    def __sub__(self, other):
        if not isinstance(other, Length):
            raise ValueError("lengh must calulate with Length Object")
        return Length(self.value - other.value)


class Angle():
    def __init__(self, value, unit='rad'):
        if unit != 'rad' and unit != 'deg':
            raise "Unit of Angle object must be rad or deg"
        self.value = value
        self.unit = unit
    
    def __str__(self):
        return f"{self.value} in {self.unit}"

    def get_value(self):
        return self.value, self.unit
    
    def set_value(self, new_value, unit='rad'):
        if unit != 'rad' and unit != 'deg':
            raise "Unit of Angle object must be rad or deg"
        self.value = new_value
        self.unit = unit

    def toggle_unit(self):
        if self.unit== "rad":
            self.value = 180.0 *self.value / math.pi
        else:
            self.value = math.pi * self.value / 180.0
    
    def to_deg(self):
        if self.unit == 'deg':
            pass
        else:
            self.toggle_unit()
            return self
    
    def to_rad(self):
        if self.unit == 'rad':
            pass
        else:
            self.toggle_unit()
            return self
        
    def __add__(self, angle):
        self.to_rad()
        angle.to_rad()
        return Angle(self.value + angle.value, 'rad')
        
    
    def __addr__(self, angle):
        self.to_rad()
        angle.to_rad()
        return Angle(self.value + angle.value, 'rad')
        

    def __sub__(self, angle):
        self.to_rad()
        angle.to_rad()
        return Angle(self.value - angle.value, 'rad')
        
        
    


class Vector():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.arr = np.array([[self.x],
                            [self.y],
                            [self.z]])

    def __str__(self):
        return f"<{self.x} {self.y} {self.z}>"
    
    def __iter__(self):
        return [self.x ,self.y, self.z]
    
    def get_cood(self):
        return self.x, self.y, self.z
    
    def set_cood(self, x, y, z):
        if x != None:
            self.x = x
        if y != None:
            self.y = y
        if z != None:
            self.z = z
        
        self.arr = np.array([[self.x],
                            [self.y],
                            [self.z]])
    
    def get_size(self):
        return float(np.sqrt((self.x**2 + self.y**2 +self.z**2)))

    def unify(self):
        size = float(np.sqrt((self.x**2 + self.y**2 +self.z**2)))
        x = self.x/size
        y = self.y/size
        z = self.z/size
        return Vector(x,y,z)
        
    def __add__(self, vector):
        return Vector(self.x+vector.x, self.y+vector.y, self.z+vector.z)
    
    def __sub__(self, vector):
        return Vector(self.x-vector.x, self.y-vector.y, self.z-vector.z)
    
    def product(self, vector):
        return self.x*vector.x + self.y*vector.y + self.z*vector.z 


class Matrix():
    def __init__(self, target_x:Vector=None, target_y:Vector=None, target_z:Vector=None, need_unify = False):
        if need_unify:
            col_x = target_x.unify()
            col_y = target_y.unify()
            col_z = target_z.unify()
        else:
            col_x = target_x
            col_y = target_y
            col_z = target_z

        if target_x !=None and target_y !=None and target_z !=None:
            self.mat = np.concatenate([col_x.arr ,col_y.arr ,col_z.arr], axis=1)
        else:
            self.mat = np.eyes(3)

    def __str__(self):
        return self.mat 
    

    def _(self, tensor):
        if isinstance(tensor, Vector):
            temp = np.matmul(self.mat, tensor.arr)
            return Vector(temp[0].squeeze(), temp[1].squeeze(), temp[2].squeeze())
        
        elif isinstance(tensor, Matrix):
            temp = np.matmul(self.mat, tensor.mat)
            temp_obj = Matrix(None,None,None)
            temp_obj.mat = temp
            return temp_obj

    
class GaussRoll(Matrix):
    def __init__(self, theta:Angle):
        theta_, _ = theta.to_rad().get_value()
        self.mat = np.array([[1,0,0],
                             [0,math.cos(theta_), -math.sin(theta_)],
                             [0,math.sin(theta_), math.cos(theta_)]])


class GaussPitch(Matrix):
    def __init__(self, theta:Angle):
        theta_, _ = theta.to_rad().get_value()
        self.mat = np.array([[math.cos(theta_),0 ,math.sin(theta_)],
                             [0,1,0 ],
                             [-math.sin(theta_),0 ,math.cos(theta_)]])


class GaussYaw(Matrix):
    def __init__(self, theta:Angle):
        theta_, _ = theta.to_rad().get_value()
        self.mat = np.array([[math.cos(theta_),-math.sin(theta_),0],
                             [math.sin(theta_),math.cos(theta_),0],
                             [0,0,1]])


class OperatorMat():
    def __init__(self, rot:Matrix, mov:Vector=Vector(0,0,0)):
        self.mat = np.concatenate([rot.mat, mov.arr], axis=1)
        self.mat = np.concatenate([self.mat, np.array([[0,0,0,1]])])

    def _(self, vector):
        new_point = np.matmul(self.mat, np.concatenate([vector.arr,np.array([[1]])]))
        return Vector(new_point[0].squeeze(), new_point[1].squeeze(), new_point[2].squeeze())


class Frame():
    def __init__(self, origin:Vector, basis_x:Vector, basis_y:Vector, basis_z:Vector):
        self.origin = origin
        self.bx = basis_x.unify()
        self.by = basis_y.unify()
        self.bz = basis_z.unify()
        

if __name__ == "__main__":
    a = GaussRoll(Angle(30, 'deg'))
    b = GaussPitch(Angle(30, 'deg'))
    print(a._(b).mat)