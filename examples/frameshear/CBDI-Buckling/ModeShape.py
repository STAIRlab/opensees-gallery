import numpy as np
import matplotlib.pyplot as plt
from CBDI import hMatrix,gMatrix
from math import pi

## Prismatic column
# Only need to compute eigenvalues of l*
# i.e., setting EI = L = 1
Nparray = [1,2,3,8]
line_styles = {1:'-xb',2:'-^g',3:'-<r',8:'-oc'}

m1o = 0.0
m2o = 2.5
m3o = 5.0

# Create Figure 
plt.rc('font',family='serif')
plt.rc('mathtext',fontset='dejavuserif')
plt.rc('axes',labelsize=8)
plt.rc('axes',titlesize=8)
plt.rc('legend',fontsize=8)
plt.rc('xtick',labelsize=8)
plt.rc('ytick',labelsize=8)
  
fig = plt.figure(figsize=(7.0,3.5))
ax = fig.add_axes([0.08,0.11,0.90,0.85])

x_exact = np.linspace(0.0, 1.0, num=100)
m1_exact = np.sin(1*pi*x_exact)
m2_exact = np.sin(2*pi*x_exact)
m3_exact = np.sin(3*pi*x_exact)

plt.plot(m1_exact+m1o,x_exact,'k:',linewidth=3,label='Exact')
plt.plot(m2_exact+m2o,x_exact,'k:',linewidth=3)
plt.plot(m3_exact+m3o,x_exact,'k:',linewidth=3)

plt.ylim([0.0,1.0])
plt.xlim([-1.5,6.5])
plt.ylabel('Normalized position along column, $x/L$')
plt.xticks([m1o,m2o,m3o], ['Mode 1', 'Mode 2', 'Mode 3'])

for Np in Nparray:
   
    # Equal
    x = []
    for i in range(Np):
        x.append((0.5+i)/Np)
    
    h = hMatrix(x,Np)
    g = gMatrix(x,Np)

    lstar = np.dot(h,np.linalg.inv(g))
    [v,d] = np.linalg.eig(-lstar)   
    sort_index = np.flip(np.argsort(v))

    # Add end points for plotting
    x_plot = x.copy()
    x_plot = np.insert(x_plot,0,0)
    x_plot = np.append(x_plot,1)

    # Plot Mode 1
    fact = np.median(np.divide(np.sin(1*pi*np.array(x)),d[:,sort_index[0]]))
    m_plot = fact*d[:,sort_index[0]]
    m_plot = np.insert(m_plot,0,0)
    m_plot = np.append(m_plot,0)

    plt.plot(m_plot+m1o,x_plot,line_styles[Np],linewidth=1.5,markersize=6,label=f'$N_p$ = {Np}')

    # Plot Mode 2
    if Np >= 2:
        fact = np.median(np.divide(np.sin(2*pi*np.array(x)),d[:,sort_index[1]]))
        m_plot = fact*d[:,sort_index[1]]
        m_plot = np.insert(m_plot,0,0)
        m_plot = np.append(m_plot,0)

        plt.plot(m_plot+m2o,x_plot,line_styles[Np],linewidth=1.5,markersize=6)
    
    # Plot Mode 3
    if Np >= 3:
        fact = np.median(np.divide(np.sin(3*pi*np.array(x)),d[:,sort_index[2]]))
        m_plot = fact*d[:,sort_index[2]]
        m_plot = np.insert(m_plot,0,0)
        m_plot = np.append(m_plot,0)

        plt.plot(m_plot+m3o,x_plot,line_styles[Np],linewidth=1.5,markersize=6)  
    
plt.legend(loc='center left')

plt.savefig('Figure_6_ModeShape.png',dpi=300)
plt.show()