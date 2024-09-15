import numpy as np
import matplotlib.pyplot as plt
from CBDI import hMatrix,gMatrix

## Prismatic column
# Only need to compute eigenvalues of l*
# i.e., setting EI = L = 1

Nparray = range(1,8+1)
psiArray1_gauss = []
psiArray2_gauss = []
psiArray3_gauss = []
psiArray1_equal = []
psiArray2_equal = []
psiArray3_equal = []
# psiArray1_cheby = []
# psiArray2_cheby = []
# psiArray3_cheby = []
# psiArray1_clenshaw = []
# psiArray2_clenshaw = []
# psiArray3_clenshaw = []


for Np in Nparray:
    # Gauss
    x,y = np.polynomial.legendre.leggauss(Np)
    x = 0.5*(x+1)

    h = hMatrix(x,Np)
    g = gMatrix(x,Np)

    lstar = np.dot(h,np.linalg.inv(g))
    [v,d] = np.linalg.eig(-lstar)
    v = sorted(v, reverse=True)

    psiArray1_gauss.append(1/v[0])
    if Np >= 2:
        psiArray2_gauss.append(1/v[1])
    if Np >= 3:
        psiArray3_gauss.append(1/v[2])

    # Equal
    x = []
    for i in range(Np):
        x.append((0.5+i)/Np)

    h = hMatrix(x,Np)
    g = gMatrix(x,Np)

    lstar = np.dot(h,np.linalg.inv(g))
    v,d   = np.linalg.eig(-lstar)
    v = sorted(v, reverse=True)

    psiArray1_equal.append(1/v[0])
    if Np >= 2:
        psiArray2_equal.append(1/v[1])
    if Np >= 3:
        psiArray3_equal.append(1/v[2])

    # # Chebyshev
    # x = []
    # for i in range(Np):
    #     z = np.cos(0.5*np.pi*(2*(i+1)-1.0)/Np)
    #     x.append(0.5*(z+1))
    # 
    # h = hMatrix(x,Np)
    # g = gMatrix(x,Np)
    # 
    # lstar = np.dot(h,np.linalg.inv(g))
    # [v,d] = np.linalg.eig(-lstar)
    # v = sorted(v, reverse=True)
    # 
    # psiArray1_cheby.append(1/v[0])
    # if Np >= 2:
    #     psiArray2_cheby.append(1/v[1])
    # if Np >= 3:
    #     psiArray3_cheby.append(1/v[2]) 

    # # Clenshaw
    # x = []
    # for i in range(Np):
    #     z = np.cos((i+1)*np.pi/(Np+1))
    #     x.append(0.5*(z+1))
    # 
    # h = hMatrix(x,Np)
    # g = gMatrix(x,Np)
    # 
    # lstar = np.dot(h,np.linalg.inv(g))
    # [v,d] = np.linalg.eig(-lstar)
    # v = sorted(v, reverse=True)
    # 
    # psiArray1_clenshaw.append(1/v[0])
    # if Np >= 2:
    #     psiArray2_clenshaw.append(1/v[1])
    # if Np >= 3:
    #     psiArray3_clenshaw.append(1/v[2]) 


# Create Figure 
plt.rc('font',family='serif')
plt.rc('mathtext',fontset='dejavuserif')
plt.rc('axes',labelsize=8)
plt.rc('axes',titlesize=8)
plt.rc('legend',fontsize=8)
plt.rc('xtick',labelsize=8)
plt.rc('ytick',labelsize=8)

fig = plt.figure(figsize=(3.5,5.0))
ax = fig.add_axes([0.15,0.11,0.82,0.25])
plt.plot([min(Nparray),max(Nparray)],[np.pi**2]*2,'k:',label='Exact')
plt.plot(Nparray,psiArray1_gauss,'-kx',label='Gauss')
# plt.plot(Nparray,psiArray1_cheby,'-b+',label='Chebyshev')
# plt.plot(Nparray,psiArray1_clenshaw,'-go',label='Clenshaw')
plt.plot(Nparray,psiArray1_equal,'-r^',label='Equally Spaced')
plt.ylim([7,13])
plt.text(1.0, 12.3,'1st Mode',fontsize=8)
plt.xlabel('Number of interpolation points, $N_p$')
plt.ylabel('Stability variable, $\psi^2$')

ax = fig.add_axes([0.15,0.41,0.82,0.25])
plt.plot([min(Nparray),max(Nparray)],[4*np.pi**2]*2,'k:',label='Exact')
plt.plot(Nparray[1:],psiArray2_gauss,'-kx',label='Gauss')
# plt.plot(Nparray[1:],psiArray2_cheby,'-b+',label='Chebyshev')
# plt.plot(Nparray[1:],psiArray2_clenshaw,'-go',label='Clenshaw')
plt.plot(Nparray[1:],psiArray2_equal,'-r^',label='Equally Spaced')
plt.ylim([30,70])
plt.text(1.0, 65.0,'2nd Mode',fontsize=8)
plt.ylabel('Stability variable, $\psi^2$')
plt.legend(loc='upper right')

ax = fig.add_axes([0.15,0.71,0.82,0.25])
plt.plot([min(Nparray),max(Nparray)],[9*np.pi**2]*2,'k:',label='Exact')
plt.plot(Nparray[2:],psiArray3_gauss,'-kx',label='Gauss')
# plt.plot(Nparray[2:],psiArray3_cheby,'-b+',label='Chebyshev')
# plt.plot(Nparray[2:],psiArray3_clenshaw,'-go',label='Clenshaw')
plt.plot(Nparray[2:],psiArray3_equal,'-r^',label='Equally Spaced')
plt.ylim([50,200])
plt.text(1.0, 180.0,'3rd Mode',fontsize=8)
plt.ylabel('Stability variable, $\psi^2$')

plt.savefig('Figure_5_Prismatic.png',dpi=300)
plt.show()

