'python3 call c shared lib demo'
__author__ = 'hawrk'
__date__ = '2016.11.28'

import ctypes
import os

import sample

_file = 'libsample.so'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))   #这什么 鬼？
_mod = ctypes.cdll.LoadLibrary(_path)

#call gcd(int,int)
#func name
gcd = _mod.gcd
#input param
gcd.argtypes = (ctypes.c_int,ctypes.c_int)
#return param
gcd.restype = ctypes.c_int


#call in_mandel(double,double,int)
in_mandel = _mod.in_mandel
in_mandel.argtypes = (ctypes.c_double,ctypes.c_double,ctypes.c_int)
in_mandel.restypes = ctypes.c_int

#call divede (int,int ,int*)
_divide = _mod.devide
_divide.argtypes = (ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_int))
_divide.restype = ctypes.c_int

def divide(x,y):
    rem = ctypes.c_int()
    quot = _divide(x,y,rem)
    return quot,rem.value

#call Point struct
class Point(ctypes.Structure):
    _fields_ = [('x',ctypes.c_double),
                ('y',ctypes.c_double)]
distince = _mod.distince
distince.argtypes = (ctypes.POINTER(Point),ctypes.POINTER(Point))
distince.restypes = ctypes.c_double


if __name__ == '__main__':
    print ('call c func begin')
    result = sample.gcd(35,42)
    print ('call gcd fun :result =',result)

    print ("-----------")
    in_result = sample.in_mandel(0,0,500)
    print ('call in_mandel :in_result = ',in_result)

    print ('---------')
    remainder,result = sample.divide(42,8)
    print('call divide,remainder = %d,reslut = %d' %(remainder,result))


    print ('--------')
    p1 = sample.Point(1,2)
    p2 = sample.Point(4,5)
    dresult = sample.distince(p1,p2)
    print ("point distince result = ", dresult)