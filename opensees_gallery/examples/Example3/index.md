---
title: "Example 3: Portal Frame Examples"
tags: ["Frame", "Python", "Tcl", "Concrete"]
categories: ["Basic"]
image: ConcretePortal.png
description: Nonlinear analysis of a concrete portal frame.
---

![Example 3.1](Example2.svg)

This set of examples investigates the nonlinear analysis of a reinforced
concrete frame. The nonlinear beam column element with a fiber
discretization of the cross section is used in the model.
The files for this example are:
{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
1. [`portal.py`](portal.py)
{{% /tab %}}
{{% tab name="Tcl" %}}
1. [`portal.tcl`](portal.tcl)
{{% /tab %}}
{{< /tabs >}}

These files define the following functions:

| Function             | Description         |
|----------------------|---------------------|
| `create_portal`      | Creates a model of a portal frame
| `gravity_analysis`   | Performs a gravity analysis on a model
| `pushover_analysis`  | Performs a pushover analysis on a model
| `transient_analysis` | Performs a transient analysis on a model

## `create_portal`

The function `create_portal` creates a model representing the portal
frame in the figure above.
The model consists of four nodes, two
nonlinear beam-column elements modeling the columns and an
elastic beam element to model the girder. For the column elements a
section, identical to the section used in [Example 2](../example2/), 
is created using steel and concrete fibers.


## `gravity_analysis`

We now implement a function called `gravity_analysis`
which takes the instance of `Model` returned by `create_portal`,
and proceeds to impose gravity loads and perform a static analysis.
Its use will look like:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
# Create the model
model = create_portal()

# perform analysis under gravity loads
status = gravity_analysis(model)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
create_portal;
gravity_analysis;
```
{{% /tab %}}
{{< /tabs >}}

A single load pattern with a linear time series, two vertical nodal
loads acting at nodes 3 and 4, and single point constraints to constrain
nodes 1 and 2 are created.

The model contains material non-linearities, so a solution algorithm of
type `Newton` is used. The solution algorithm uses a `ConvergenceTest` which
tests convergence of the equilibrium solution with the norm of the
displacement increment vector. 
For this nonlinear problem, the gravity
loads are applied incrementally until the full load is applied. To
achieve this, a `LoadControl` integrator which advances the solution with
an increment of `0.1` at each load step is used. The equations are formed
using a banded storage scheme, so the System is `BandGeneral`.
The
equations are numbered using an RCM (reverse Cuthill-McKee) numberer.
The constraints are enforced with a Plain constraint handler.

Once all the components of an analysis are defined, the Analysis object
itself is created. For this problem a Static Analysis object is used. To
achieve the full gravity load, 10 load steps are performed.

At end of analysis, the state at nodes 3 and 4 is output. The state of
element 1 is also output.


For the two nodes, displacements and loads are given. For the
beam-column elements, the element end forces in the local system are
provided.

The `nodeGravity.out` file contains ten lines, each line containing 7
entries. The first entry is time in the domain at end of the load step.
The next 3 entries are the displacements at node 3, and the final 3
entries the displacements at node 4.

## `pushover_analysis`

In this example the nonlinear reinforced concrete portal frame which has
undergone the gravity load analysis of Example 3.1 is now subjected to a
pushover analysis.

After performing the gravity load analysis on the model, the time in the
domain is reset to 0.0 and the current value of all loads acting are
held constant. A new load pattern with a linear time series and
horizontal loads acting at nodes 3 and 4 is then added to the model.

The static analysis used to perform the gravity load analysis is
modified to take a new DisplacementControl integrator. At each new step
in the analysis the integrator will determine the load increment
necessary to increment the horizontal displacement at node 3 by 0.1 in.
60 analysis steps are performed in this new analysis.

For this analysis the nodal displacements at nodes 3 and 4 will be
stored in the file nodePushover.out for post-processing. In addition,
the end forces in the local coordinate system for elements 1 and 2 will
be stored in the file elePushover.out. At the end of the analysis, the
state of node 3 is printed to the screen.


In addition to what is displayed on the screen, the file `node32.out` and
`ele32.out` have been created by the script. Each line of `node32.out`
contains the time, DX, DY and RZ for node 3 and DX, DY and RZ for node 4
at the end of an iteration. Each line of eleForce.out contains the time,
and the element end forces in the local coordinate system. A plot of the
load-displacement relationship at node 3 is shown in
the figure below.


![Load displacement curve for node 3](ExampleOut3.2.svg)


## `transient_analysis`

<!-- 3.3 -->

In this example the reinforced concrete portal frame which has undergone
the gravity load analysis of Example 3.1 is now subjected to a uniform
earthquake excitation.

After performing the gravity load analysis, the time in the domain is
reset to 0.0 and the current value of all active loads is set to
constant. Mass terms are added to nodes 3 and 4. A new uniform
excitation load pattern is created. The excitation acts in the
horizontal direction and reads the acceleration record and time interval
from the file `ARL360.g3`. The file `ARL360.g3` is created from the PEER
Strong Motion Database (http://peer.berkeley.edu/smcat/) record
`ARL360.at2` using the Tcl procedure `ReadSMDFile` contained in the file
`ReadSMDFile.tcl`.

The static analysis object and its components are first deleted so that
a new transient analysis object can be created.

A new solution Algorithm of type `Newton` is then created. The solution
algorithm uses a `ConvergenceTest` which tests convergence on the norm of
the displacement increment vector. The integrator for this analysis will
be of type Newmark with a \(\gamma = 0.25\) and \(\beta = 0.5\). 

The
integrator will add some stiffness proportional damping to the system,
the damping term will be based on the last committed stifness of the
elements, i.e. \(C = a_c K_{\text{commit}}\) with \(a_c = 0.000625\). 

The equations are formed using a banded storage scheme, so the System is
BandGeneral. The equations are numbered using an RCM (reverse Cuthill-McKee)
numberer. The constraints are enforced with a Plain constraint handler.

Once all the components of an analysis are defined, the Analysis object
itself is created. For this problem a Transient Analysis object is used.
`2000` time steps are performed with a time step of `0.01`.

In addition to the transient analysis, two eigenvalue analysis are
performed on the model. The first is performed after the gravity
analysis and the second after the transient analysis.

For this analysis the nodal displacenments at Nodes 3 and 4 will be
stored in the file `nodeTransient.out` for post-processing. In addition
the section forces and deformations for the section at the base of
column 1 will also be stored in two seperate files. The results of the
eigenvalue analysis will be displayed on the screen.



```
Gravity load analysis completed
eigen values at start of transient: 2.695422e+02  1.750711e+04  
Transient analysis completed SUCCESSFULLY
eigen values at start of transient: 1.578616e+02  1.658481e+04  


 Node: 3
     Coordinates  : 0 144 
     commitDisps: -0.0464287 -0.0246641 0.000196066 
     Velocities   : -0.733071 1.86329e-05 0.00467983 
     commitAccels: -9.13525 0.277302 38.2972 
     unbalanced Load: -3.9475 -180 0 
     Mass : 
       0.465839 0 0 
       0 0.465839 0 
       0 0 0 

     Eigenvectors: 
       -1.03587 -0.0482103 
       -0.00179081 0.00612275 
       0.00663473 3.21404e-05 
```

The two eigenvalues for the eigenvalue analysis are printed to the
screen. The state of node 3 at the end of the analysis is also printed.
The information contains the last committed displacements, velocities
and accelerations at the node, the unbalanced nodal forces and the nodal
masses. In addition, the eigenvector components of the eigenvector
pertaining to the node 3 is also displayed.

In addition to the contents displayed on the screen, three files have
been created. Each line of `nodeTransient.out` contains the domain time,
and DX, DY and RZ for node 3. Plotting the first and second columns of
this file the lateral displacement versus time for node 3 can be
obtained as shown in the figure below. Each line of the files `ele1secForce.out` 
and `ele1secDef.out` contain the domain time and the forces and deformations
for section 1 (the base section) of element 1. These can be used to
generate the moment-curvature time history of the base section of column
1 as shown below.


![Lateral displacement at node 3](newNode3.3.svg)


![Column section moment-curvature results](newElement1MK.svg)


