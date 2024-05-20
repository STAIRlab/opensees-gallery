import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

g = 9.8

class DoublePendulum:
    """ This class holds all of pendulum variables such as
    position, velocity, length, mass, and energy.
    """
    def __init__(self,length, mass, initial_angle):
        self.l = length
        self.m =       # FIX ME!  Set this line to be equal to the mass variable
        self.theta = initial_angle
        self.v =        # FIX ME!  Set the v variable equal to 0
        self.x = 0
        self.y = 0
        self.p = 0
        self.a = 0
        self.energy = 0
        self.ke = 0
        self.pe = 0
        self.display_values()

    def display_values(self):
        # FIX ME!
        # Print out the initial length, mass, and angle on the lines below
        # Use the self.l, self.m, and self.theta variables
        print

def initialize_plots(b1,b2):
    """ Set up the plots that will be used by the animation. """

    fig,axes = plt.subplots(2,2,figsize=(15,10))    # Opens up a figure with four subplots

    total_l = b1.l + b2.l
    data =[]

    xlist = [0,b1.x,b2.x]       # Grab the locations of the bobs.
    ylist = [0,b1.y,b2.y]

    axes[0,0].plot([-.5,.5],[0,0],'-k',linewidth=5)

    # FIX ME!
    # On the line below pass the xlist and ylist variables to the plot function
    # Additionally, set the linewidth=3 by using the linewidth variable.
    line, = axes[0,0].plot(     ,      , '-bo', markersize=10,     ) # FIX ME!

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
    b1,b2 = initialize(l1,l2,m1,m2,p1,p2)
    fig,axes,data = initialize_plots(b1,b2)

    t = np.arange(int(tend/dt)+1)*dt


    i = 1
    for i,ti in enumerate(t[1:],start=1):
        pyode(b1,b2,dt)
        x1,y1,x2,y2 = get_positions(b1,b2)
        e1,e2 = get_energies(b1,b2)
        update_plots(b1,b2,ti,fig,axes,data)

    return

def initialize(l1,l2,m1,m2,theta1,theta2):
    """ Initialize the simulation,
        see evolve function for descripton of inputs.
    """
    b1 = DoublePendulum(l1,m1,theta1)
    b2 = DoublePendulum(l2,m2,theta2)
    junk = get_positions(b1,b2)
    junk = get_energies(b1,b2)
    b1.a,b2.a = kick(b1,b2)

    return b1,b2

def kick(b1,b2):
    """ This calculates the acceleration on each bob."""
    m1 = b1.m
    l1 = b1.l
    v1 = b1.v
    v12 = v1*v1
    t1 = b1.theta

    m2 = b2.m
    l2 = b2.l
    v2 = b2.v
    v22 = v2*v2
    t2 = b2.theta

    c = np.cos(t1-t2)
    c1 = np.cos(t1)
    c2 = np.cos(t2)
    s = np.sin(t1-t2)
    s1 = np.sin(t1)
    s2 = np.sin(t2)
    ss = s*s



    norm = (m1 +m2*ss)

    a1 = -.5*m2*np.sin(2*(t1-t2))*v12/norm - l2*m2*s*v22/(l1*norm)
    a1 += (-.5*g/l1)*((2*m1+m2)*s1 + m2*np.sin(t1-2*t2))/norm

    a2 = l1*(m1+m2)*v12*s/(l2*norm) + m2*np.sin(2*(t1-t2))*v22/(2*norm)
    a2 += (g/l2)*(m1+m2)*c1*s/norm

    return a1,a2

def get_positions(b1,b2):
    """ Calculate the x,y positions of each bob. """
    l1 = b1.l
    t1 = b1.theta

    l2 = b2.l
    t2 = b2.theta

    x1 = l1*np.sin(t1)
    y1 = -l1*np.cos(t1)

    x2 = x1 + l2*np.sin(t2)
    y2 = y1 - l2*np.cos(t2)

    b1.x = x1
    b1.y = y1
    b2.x = x2
    b2.y = y2

    return x1,y1,x2,y2

def get_energies(b1,b2):
    """ Calculate the kinetic and potential energies of each bob."""
    x1,y1,x2,y2 = get_positions(b1,b2)

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

def kick_wrapper(y0,t,b1,b2):
    """ This is a wrapper to the kick function"""

    b1.theta,b2.theta,b1.v,b2.v = y0
    a1,a2 = kick(b1,b2)
    res = np.array([b1.v,b2.v,a1,a2])
    return res


def pyode(b1,b2,dt):
    """ This is a wrapper to the odeint integrator. """
    y0 = np.array([b1.theta,b2.theta,b1.v,b2.v])

    res=odeint(kick_wrapper,y0,[0,dt],args=(b1,b2))
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





def update_plots(b1,b2,t,fig,axes,data):
    """ Update all of the plots. """
    axes[0,0].set_title('t = %f' % t)
    line,line1,line2 = data[0]
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

