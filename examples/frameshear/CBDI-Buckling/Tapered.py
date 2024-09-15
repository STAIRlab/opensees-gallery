import numpy as np
import matplotlib.pyplot as plt
from CBDI import hMatrix,gMatrix

plt.rc('font',family='serif')
plt.rc('mathtext',fontset='dejavuserif')
plt.rc('axes',labelsize=8)
plt.rc('axes',titlesize=8)
plt.rc('legend',fontsize=8)
plt.rc('xtick',labelsize=8)
plt.rc('ytick',labelsize=8)

## Tapered column
E = 1
Io = 1
L = 1

taperArray = [0.2,0.4,0.6,0.8]
psiExact = {}
psiExact[0.2] = 7.09
psiExact[0.4] = 4.69
psiExact[0.6] = 2.68
psiExact[0.8] = 1.09

Nparray = range(1,8+1)

fig = plt.figure(figsize=(3.5,3.5))
ax = fig.add_axes([0.13,0.12,0.84,0.85])

for it,taper in enumerate(taperArray):
    psiArray = []

    for Np in Nparray:
        # x,y = np.polynomial.legendre.leggauss(Np)
        # x = 0.5*(x+1)
        x = []
        for i in range(Np):
            x.append((0.5+i)/Np)
        # print(x)

        h = hMatrix(x,Np)
        g = gMatrix(x,Np)

        lstar = np.dot(h,np.linalg.inv(g))
        F = np.zeros((Np,Np))
        for i in range(Np):
            I = Io*(1-taper*x[i])**3
            F[i,i] = 1/(E*I)
        [v,d] = np.linalg.eig(np.dot(-L**2*lstar,F))

        psiArray.append(min(1/v))

    if it == len(taperArray)-1:
        plt.plot(Nparray,[psiExact[taper]]*len(psiArray),'k:',label=f'Darbandi et al. 2010')
        plt.plot(Nparray,psiArray,'-kx',label='CBDI')
    else:
        plt.plot(Nparray,[psiExact[taper]]*len(psiArray),'k:')
        plt.plot(Nparray,psiArray,'-kx')

plt.text(5,6.5,'$\eta=$0.2',fontsize=8)
plt.text(5,5.0,'$\eta=$0.4',fontsize=8)
plt.text(5,3.0,'$\eta=$0.6',fontsize=8)
plt.text(5,1.3,'$\eta=$0.8',fontsize=8)

plt.ylim([0,9])
plt.xlabel('Number of interpolation points, $N_p$')
plt.ylabel('Stability variable, $\psi^2$')
plt.legend(loc='upper right')

plt.savefig('Figure_8_Tapered.png',dpi=300)
plt.show()

