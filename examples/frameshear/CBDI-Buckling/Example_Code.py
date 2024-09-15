
if __name__ == "__main__":

    import numpy as np
    L  = 10.0
    xi = [0.1,0.3,0.5,0.7,0.9] # xi = x/L
    EI = [100.0,100.0,100.0,100.0,100.0]
    Np = len(xi)

    # Form h matrix
    h = np.zeros((Np,Np))
    for j in range(Np):
        for i in range(Np):
            h[i,j] = (xi[i]**(j+2)-xi[i])/((j+1)*(j+2))

    # Form g matrix
    g = np.zeros((Np,Np))
    for j in range(Np):
        for i in range(Np):
            g[i,j] = xi[i]**j

    # Form flexibility matrix
    F = np.zeros((Np,Np))
    for i in range(Np):
        F[i,i] = 1/EI[i]

    lstar = np.dot(h,np.linalg.inv(g))
    [v,d] = np.linalg.eig(np.dot(-L*L*lstar,F))

    Pcr = 1/max(v)


    from math import pi
    print(f'Pcr (CBDI)  = {Pcr}')
    print(f'Pcr (Exact) = {pi**2*EI[0]/L**2}')

