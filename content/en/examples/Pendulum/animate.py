# https://scipython.com/book2/chapter-7-matplotlib/problems/p77/animating-a-pendulum/
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import ellipk
import matplotlib.animation as animation


def integrate(model, dt, u0=0, v0=0):
    m, L, g = model
    Tharm = 2 * np.pi * np.sqrt(L / g)
    # Initial angular position and tangential velocity.
    theta, v = [u0], [v0]
    old_theta = u0
    i = 0
    while True:
        # Forward Euler method for numerical integration of the ODE.
        i += 1
        t = i * dt
        # Update the bob position using its updated angle.
        old_theta, old_v = theta[-1], v[-1]
        omega = old_v / L
        new_theta = old_theta - omega * dt

        # Tangential acceleration.
        acc = g * np.sin(old_theta)
        # Update the tangential velocity.
        new_v = old_v + acc * dt

        if t > Tharm and new_v * old_v < 0:
            # At the second turning point in velocity we're back where we started,
            # i.e. we have completed one period and can finish the simulation.
            break

        theta.append(new_theta)
        v.append(new_v)

    return theta, v

def animate(theta, L):
    def get_coords(th):
        """Return the (x, y) coordinates of the bob at angle th."""
        return L * np.sin(th), -L * np.cos(th)

    # Initialize the animation plot. Make the aspect ratio equal so it looks right.
    fig = plt.figure()
    ax = fig.add_subplot(aspect='equal')

    # The pendulum rod, in its initial position.
    x0, y0 = get_coords(theta[0])
    line, = ax.plot([0, x0], [0, y0], lw=3, c='k')
    # The pendulum bob: set zorder so that it is drawn over the pendulum rod.
    bob_radius = 0.08
    circle = ax.add_patch(plt.Circle(get_coords(u0), bob_radius,
                        fc='r', zorder=3))

    # Set the plot limits so that the pendulum has room to swing!
    ax.set_xlim(-L*1.2, L*1.2)
    ax.set_ylim(-L*1.2, L*1.2)

    def update(i):
        """Update the animation at frame i."""
        x, y = get_coords(theta[i])
        line.set_data([0, x], [0, y])
        circle.set_center((x, y))

    nframes = nsteps
    interval = dt * 1000
    ani = animation.FuncAnimation(fig, update, frames=nframes, repeat=True,
                                interval=interval)

    # To save the animation using Pillow as a gif
    writer = animation.PillowWriter(fps=15,
                                    metadata=dict(artist='Me'))#,
                                    #bitrate=1800)
    ani.save('pendulum.gif', writer=writer)

    # ani.save('pendulum.mp4', fps=30)
    #plt.show()

if __name__ == "__main__":
    # Bob mass (kg), pendulum length (m), acceleration due to gravity (m.s-2).
    m, L, g = 1, 1, 9.81

    # Initial angular displacement (rad), tangential velocity (m.s-1)
    u0, v0 = np.radians(60), 0

    # Estimate of the period using the harmonic (small displacement) approximation.
    # The real period will be longer than this.

    # Time step for numerical integration of the equation of motion (s).
    dt = 0.01

    theta, v = integrate((m, L, g), dt, u0, v0)
    # Calculate the estimated pendulum period, T, from our numerical integration,
    # and the "exact" value in terms of the complete elliptic integral of the
    # first kind.
    nsteps = len(theta)
    T = nsteps * dt
    Ts = 2 * np.pi * np.sqrt(L / g)
    print('Integration period, Ti = {} s'.format(nsteps*dt))
    print('Estimated small-displacement angle period, Ts = {} s'.format(Ts))

    print('Elliptic period, Te = {} s'
                    .format(2 * Ts / np.pi * ellipk(np.sin(u0/2)**2)))

    animate(theta, L)