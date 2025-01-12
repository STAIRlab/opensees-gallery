#!/usr/bin/env python
# coding: utf-8

# Double-Layer Shallow Dome

# #### March 2020, Amir Hossein Namadchi

# This is an OpenSeesPy simulation of one of the numerical examples in our
# previously [published paper](https://ascelibrary.org/doi/abs/10.1061/%28ASCE%29EM.1943-7889.0001329).
# The Core was purely written in *Mathematica*. This is my attempt to perform
# the analysis again via Opensees Core, to see if I can get the similar
# results.
#

import numpy as np
import opensees.openseespy as ops
import matplotlib.pyplot as plt
import veux

# Below, the base units are defined as python variables:

## Units
m = 1               # Meters
KN = 1              # KiloNewtons
s = 1               # Seconds

# ### Model Defintion

# The coordinates information for each node are stored `node_coords`. Each row
# represent a node with the corresponding coordinates. Elements configuration
# are also described in `connectivity`, each row representing an element with
# its node IDs. Elements cross-sectional areas are stored in `area_list`. This
# appraoch, offers a more pythonic and flexible code when building the model.
# Since this is a relatively large model, some data will be read from external
# `.txt` files to keep the code cleaner.



# Node Coordinates Matrix (size : nn x 3)
node_coords = np.loadtxt('assets/nodes.txt',
                         dtype = np.float64) * m

# Element Connectivity Matrix (size: nel x 2)
connectivity = np.loadtxt('assets/connectivity.txt',
                          dtype = np.int64).tolist()

# Loaded Nodes
loaded_nodes = np.loadtxt('assets/loaded_nodes.txt',
                          dtype = np.int64).tolist()

# Get Number of total Nodes
nn = len(node_coords)
# Get Number of total Elements
nel = len(connectivity)

# Cross-sectional area list (size: nel)
area_list = np.ones(nel)*(0.001)*(m**2)

# Modulus of Elasticity list (size: nel)
E_list = np.ones(nel)*(2.0*10**8)*(KN/m**2)

# Mass Density
rho = 7.850*((KN*s**2)/(m**4))

#Boundary Conditions (size: fixed_nodes x 4)
B_C = np.column_stack((np.arange(1,31),
                 np.ones((30,3), dtype = np.int64))
               ).tolist()

# ### Model Construction

model = ops.Model(ndm=3, ndf=3)

# Add nodes to the model
for n in range(nn):
    model.node(n+1, *node_coords[n])

# Apply boundary conditions
for n in range(len(B_C)):
    model.fix(B_C[n][0], *B_C[n][1:])

# Define Material
model.uniaxialMaterial('Elastic',1, E_list[0])

# Add Elements
for e in range(nel):
    model.element('corotTruss', e+1, *connectivity[e], area_list[e],
                    1,'-rho', rho*area_list[e], '-cMass', 1)

# ### Draw model
# The model can now be drawn using the `veux` Python package:



veux.render(model)

# * ### Eigenvalue Analysis
# Let's get the first 6 periods of the structure to see if they coincide with the ones in paper.

eigenvalues = model.eigen(6)

T_list = 2*np.pi/np.sqrt(eigenvalues)
print('The first 6 period of the structure are as follows:\n', T_list)

# ### Dynamic Analysis
# Great accordance is obtained in eigenvalue analysis. Now, let's do `wipeAnalysis()` and perform dynamic analysis. The Newmark time integration algorithm with $\gamma=0.5$ and $\beta=0.25$ (Constant Average Acceleration Algorithm) is used. Harmonic loads are applied vertically on the `loaded_nodes` nodes.
# 



model.wipeAnalysis()

# define load function
P = lambda t: 250*np.sin(250*t)

# Dynamic Analysis Parameters
dt = 0.00025
time = 0.2
time_domain = np.arange(0,time,dt)

# Adding loads to the domain beautifully
model.timeSeries('Path', 1,
                 dt=dt,
                 values=np.vectorize(P)(time_domain),
                 time=time_domain)

model.pattern('Plain', 1, 1)

for n in loaded_nodes:
    model.load(n, *[0,0,-1])

# Analysis
model.constraints('Plain')
model.numberer('Plain')
model.system('ProfileSPD')
model.test('NormUnbalance', 0.0000001, 100)
model.algorithm('ModifiedNewton')
model.integrator('Newmark', 0.5, 0.25)
model.analysis('Transient')



time_lst =[]           # list to hold time stations for plotting
d_apex_list = []       # list to hold vertical displacments of the apex

for i in range(len(time_domain)):
    is_done = model.analyze(1, dt)
    if is_done != 0:
        print('Failed to Converge!')
        break
    time_lst.append(model.getTime())
    d_apex_list.append(model.nodeDisp(362,3))

# ### Visualization

# Plot the time history of the vertical displacement of the apex


plt.figure(figsize=(12,4))
plt.plot(time_lst, np.array(d_apex_list), color = '#d62d20', linewidth=1.75)
plt.ylabel('Vertical Displacement (m)', {'fontstyle':'italic','size':14})
plt.xlabel('Time (sec)', {'fontstyle':'italic','size':14})
plt.xlim([0.0, time])
plt.grid()
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14);

# ### Closure
# Very good agreements with the paper are obtained.

# <blockquote>Namadchi, Amir Hossein, Farhang Fattahi, and Javad Alamatian. "Semiexplicit Unconditionally Stable Time Integration for Dynamic Analysis Based on Composite Scheme." Journal of Engineering Mechanics 143, no. 10 (2017): 04017119.</blockquote>
# 
