import math
from scipy.integrate import quad

def r_0(d,O):
    b=d/(2*math.pi)
    r=b*O
    return r

def L_t(t):
    v=1
    L=v*t
    return L

def x_y_r_O(r,O):
    x=r*math.cos(O)
    y=r*math.sin(O)
    return x,y

def integrand(O, d):  # 新增积分函数
    b = d / (2 * math.pi)
    return math.sqrt(b**2 - (b*O)**2)

def L_inte(L, d, O_upper, O_lower):
    # 使用数值积分计算弧长
    result, error = quad(integrand, O_lower, O_upper, args=(d,))
    return result