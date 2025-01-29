import numpy as np
from numpy import pi, sin, cos, sqrt, exp, arcsin
from scipy import special

#  Elliptic functions
_m = lambda x: x; #x**2

def am(u_, m_):
    return special.ellipj(u_,_m(m_))[3]

def sn(u_, m_):
    return special.ellipj(u_,_m(m_))[0]

def cd(u_, m_):
    _, cn, dn, __ = special.ellipj(u_,_m(m_))
    return cn/dn

def dn(u_, m_):
    return special.ellipj(u_,_m(m_))[2]

def cn(u_, m_):
    return special.ellipj(u_,_m(m_))[1]

def K(k_):
    return special.ellipk(_m(k_))

def E(phi_, m_):
    return special.ellipeinc(phi_, _m(m_))




def small_pendulum(t, th0=0, c=1.0):
    return th0*cos(sqrt(c)*t)


def pendulum(t, th0=0, c=1.):
    k = sin(th0/2)
    return 2*arcsin(k*cd(sqrt(c)*t, k**2))



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    t = np.linspace(0, 4*pi, 1000)

    th0 = pi/1.002

    plt.plot(t, [small_pendulum(t, th0) for t in t], color='gray', alpha=0.4)
    plt.plot(t, [pendulum(t, th0) for t in t])
    plt.show()

