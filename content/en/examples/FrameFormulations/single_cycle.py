from math import cos,sin,sqrt,pi


def single_cycle(umax, n running):

    rate = 0.01
    N =  (4*n-3)
    dt =  4.0*umax/rate/(N-1)
    m =  (umax/(n-1)/dt)

    tval, uval = np.zeros((2, N))

    for i in range(N):
           tval[i] = ((i-1)*dt)
           if   i >=  (3*n-2) :
                uval[i] =   m*tval[i]-4.0*umax

           elif   i >=  n+1:
                uval[i] =  -m*tval[i]+2.0*umax

           else:
                uval[i] = (m*tval[i])

           tout[i] = tval[i]
           tval[i] = (tval[i] + running)


    return tval, uval


