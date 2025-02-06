"""
Adapted from https://adamdempsey90.github.io/python/double_pendulum/double_pendulum.html
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

g = 9.8

class DoublePendulum:
    pass 

class Node:
    """ This class holds all of pendulum variables such as
    position, velocity, length, mass, and energy.
    """
    def __init__(self,length, mass, initial_angle):
        self.l = length
        self.m = mass
        self.theta = initial_angle
        self.v = 0
        self.x = 0
        self.y = 0
        self.p = 0
        self.a = 0
        self.energy = 0
        self.ke = 0
        self.pe = 0

def _initialize(l1,l2,m1,m2,theta1,theta2):
    """ Initialize the simulation,
        see evolve function for descripton of inputs.
    """
    b1 = Node(l1,m1,theta1)
    b2 = Node(l2,m2,theta2)
    chain = b1, b2
    junk = _get_positions(chain)
    junk = _get_energies(chain)
    b1.a, b2.a = _kick(chain)

    return chain

def _kick(chain):
    """ This calculates the acceleration on each bob."""
    b1, b2 = chain 

    m1 = b1.m
    l1 = b1.l
    v1 = b1.v
    v12 = v1*v1
    t1 = b1.theta

    m2  = b2.m
    l2  = b2.l
    v2  = b2.v
    v22 = v2*v2
    t2  = b2.theta

    c  = np.cos(t1-t2)
    c1 = np.cos(t1)
    c2 = np.cos(t2)
    s  = np.sin(t1-t2)
    s1 = np.sin(t1)
    s2 = np.sin(t2)
    ss = s*s


    norm = (m1 + m2*ss)

    a1  = -0.5*m2*np.sin(2*(t1-t2))*v12/norm - l2*m2*s*v22/(l1*norm)
    a1 += (-0.5*g/l1)*((2*m1+m2)*s1 + m2*np.sin(t1-2*t2))/norm

    a2  = l1*(m1+m2)*v12*s/(l2*norm) + m2*np.sin(2*(t1-t2))*v22/(2*norm)
    a2 += (g/l2)*(m1+m2)*c1*s/norm

    return a1, a2

def _get_positions(chain):
    """ Calculate the x,y positions of each bob. """
    b1,b2 = chain 

    x1   =  b1.l*np.sin(b1.theta)
    y1   = -b1.l*np.cos(b1.theta)
    b1.x = x1
    b1.y = y1

    x2   = x1 + b2.l*np.sin(b2.theta)
    y2   = y1 - b2.l*np.cos(b2.theta)

    b2.x = x2
    b2.y = y2

    return x1,y1,x2,y2


def _get_energies(chain):
    """ Calculate the kinetic and potential energies of each bob."""
    x1,y1,x2,y2 = _get_positions(chain)
    b1, b2 = chain

    vx1 = -y1*b1.v
    vy1 = x1*b1.v
    vx2 = vx1 + (y1-y2)*b2.v
    vy2 = vy1 + (x2-x1)*b2.v

    b1.ke = .5*b1.m*(vx1**2 + vy1**2)
    b1.pe = b1.m*g*y1
    b1.energy = b1.ke + b1.pe
    b2.ke = .5*b2.m*(vx2**2 + vy2**2)
    b2.pe = b2.m*g*y2
    b2.energy = b2.ke + b2.pe
    return b1.energy,b2.energy

def _kick_wrapper(y0,t,chain):
    """ This is a wrapper to the kick function"""
    b1,b2 = chain
    b1.theta,b2.theta,b1.v,b2.v = y0
    a1,a2 = _kick(chain)
    res = np.array([b1.v, b2.v, a1, a2])
    return res


def _integrate(chain, dt):
    """ This is a wrapper to the odeint integrator. """
    b1, b2 = chain
    y0 = np.array([b1.theta,b2.theta,b1.v,b2.v])

    res = odeint(_kick_wrapper,y0,[0,dt],args=(chain,))
    b1.theta,b2.theta,b1.v,b2.v = res[1]
    if b1.theta > np.pi:
        while b1.theta > np.pi:
            b1.theta -= 2*np.pi
    if b1.theta < -np.pi:
        while b1.theta < -np.pi:
            b1.theta += 2*np.pi
    if b2.theta > np.pi:
        while b2.theta > np.pi:
            b2.theta -= 2*np.pi
    if b2.theta < -np.pi:
        while b2.theta < -np.pi:
            b2.theta += 2*np.pi
    return


#
# Plotting
#

def _initialize_plots(b1,b2):
    """ Set up the plots that will be used by the animation. """

    fig,axes = plt.subplots(2,2,figsize=(15,10))    # Opens up a figure with four subplots

    total_l = b1.l + b2.l
    data =[]

    xlist = [0,b1.x,b2.x]       # Grab the locations of the bobs.
    ylist = [0,b1.y,b2.y]

    axes[0,0].plot([-.5,.5],[0,0],'-k',linewidth=5)

    line, = axes[0,0].plot(xlist, ylist, '-bo', markersize=10, linewidth=3)

    line1, = axes[0,0].plot(b1.x,b1.y,'-b',linewidth=2)
    line2, = axes[0,0].plot(b2.x,b2.y,'-r',linewidth=2)
    axes[0,0].set_xlim(-total_l,total_l)


    axes[0,0].set_ylim(-total_l,total_l)
    axes[0,0].set_title('t = 0',fontsize=20)
    axes[0,0].set_xlabel('x',fontsize=20)
    axes[0,0].set_ylabel('y',fontsize=20)
    data.append([line,line1,line2])

    line2, = axes[1,0].plot(0,b1.theta,'-b')
    line3, = axes[1,0].plot(0,b2.theta,'-r')
    axes[1,0].set_ylim(-np.pi,np.pi)
    axes[1,0].set_xlabel('t',fontsize=20)
    axes[1,0].set_ylabel('$\\theta$',fontsize=20)
    data.append([line2,line3])

    line1, = axes[0,1].plot(b1.theta,b1.v,'b.')

    axes[0,1].set_xlabel('$\\theta$',fontsize=20)
    axes[0,1].set_ylabel('$\\dot{\\theta}$',fontsize=20)
    axes[0,1].set_xlim(-4,4)
    axes[0,1].set_ylim(-6,6)


    line2, = axes[0,1].plot(b2.theta,b2.v,'r.')

    axes[1,1].set_xlabel('t',fontsize=20)
    axes[1,1].set_ylabel('Energies',fontsize=20)

    data.append([line1,line2])

    line1, = axes[1,1].plot(0,b1.energy,'-b')
    line2, = axes[1,1].plot(0,b2.energy,'-r')
    line3, = axes[1,1].plot(0,b1.energy+b2.energy,'-m')
    data.append([line1,line2,line3])
    axes[0,0].plot(xlist,ylist,'-o',color='grey',linewidth=3,markersize=10)

    plt.show()
    return fig,axes,data



def _update_plots(chain,t,fig,axes,data):
    """ Update all of the plots. """

    axes[0,0].set_title('t = %f' % t)
    line,line1,line2 = data[0]

    b1,b2 = chain
    line.set_xdata([0,b1.x,b2.x])
    line.set_ydata([0,b1.y,b2.y])
    line1.set_xdata( np.append(line1.get_xdata(),b1.x))
    line1.set_ydata(np.append(line1.get_ydata(),b1.y))
    line2.set_xdata( np.append(line2.get_xdata(),b2.x))
    line2.set_ydata(np.append(line2.get_ydata(),b2.y))

    line1,line2 = data[1]
    line1.set_xdata( np.append(line1.get_xdata(), t))
    line1.set_ydata(np.append(line1.get_ydata(),b1.theta))
    line2.set_xdata( np.append(line2.get_xdata(), t))
    line2.set_ydata(np.append(line2.get_ydata(),b2.theta))
    if t > axes[1,0].get_xlim()[1]:
        axes[1,0].set_xlim(0,2*t)



    line1,line2 = data[2]
    line1.set_xdata( np.append(line1.get_xdata(), b1.theta))
    line1.set_ydata(np.append(line1.get_ydata(),b1.v))
    line2.set_xdata( np.append(line2.get_xdata(), b2.theta))
    line2.set_ydata(np.append(line2.get_ydata(),b2.v))


    line1,line2,line3 = data[3]
    line1.set_xdata( np.append(line1.get_xdata(), t))
    line1.set_ydata(np.append(line1.get_ydata(),b1.energy))
    line2.set_xdata( np.append(line2.get_xdata(), t))
    line2.set_ydata(np.append(line2.get_ydata(),b2.energy))
    line3.set_xdata( np.append(line3.get_xdata(), t))
    line3.set_ydata(np.append(line3.get_ydata(),b1.energy+b2.energy))
    if t > axes[1,1].get_xlim()[1]:
        axes[1,1].set_xlim(0,2*t)


    plt.pause(1e-5)
    plt.show()
    return


def evolve(l1,l2,m1,m2,p1,p2,tend,dt):
    """ Entry point for the simulation.
    l1 = Length of the first bob.
    l2 = Length of the second bob.
    m1 = Mass of the first bob.
    m2 = Mass of the second bob.
    p1 = Angle of the first bob with respect to the vertical.
    p2 = Angle of the second bob with respect to the first bob.

    tend = Total length of the simulation.
    dt = Time between plot updates.
    """
    chain = _initialize(l1,l2,m1,m2,p1,p2)
    fig,axes,data = _initialize_plots(chain)

    t = np.arange(int(tend/dt) + 1)*dt

    for i,ti in enumerate(t[1:],start=1):
        _integrate(chain,dt)
        _get_positions(chain)
        _get_energies(chain)
        _update_plots(chain,ti,fig,axes,data)

    return

if __name__ == "__main__":
    dt = 0.001
    evolve
