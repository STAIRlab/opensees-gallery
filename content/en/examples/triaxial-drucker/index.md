---
title: "Drucker–Prager Triaxial Test"
meta:
  title: "A 3D triaxial compression simulation using the Drucker–Prager constitutive model"
thumbnail: img/examples/triaxial-drucker.png
tags: ["Solid"]
draft: true
description: >-
  This example simulates a conventional triaxial compression test
  using the Drucker–Prager model in a single 8-node brick element.
  Stress and strain response are recorded at the Gauss point.
downloads:
  Python: ["drucker.py"]
  Tcl: ["drucker.tcl"]
weight: 200
---


This model simulates the triaxial compression behavior of a soil-like material
subject to confining pressure and axial loading. The simulation is conducted using
a single 8-node `stdBrick` element with [Drucker–Prager plasticity](https://xara.so/user/manual/material/plastic/DruckerPrager.html). 
The goal is to evaluate material behavior under both hydrostatic and deviatoric loading paths.

## Model

We begin by defining the model builder and creating the nodes of the brick:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
import xara
model = xara.Model(ndm=3, ndf=3)

model.node(1, (1.0, 0.0, 0.0))
model.node(2, (1.0, 1.0, 0.0))
model.node(3, (0.0, 1.0, 0.0))
model.node(4, (0.0, 0.0, 0.0))
model.node(5, (1.0, 0.0, 1.0))
model.node(6, (1.0, 1.0, 1.0))
model.node(7, (0.0, 1.0, 1.0))
model.node(8, (0.0, 0.0, 1.0))
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
model BasicBuilder -ndm 3 -ndf 3

node 1 1.0 0.0 0.0
node 2 1.0 1.0 0.0
node 3 0.0 1.0 0.0
node 4 0.0 0.0 0.0
node 5 1.0 0.0 1.0
node 6 1.0 1.0 1.0
node 7 0.0 1.0 1.0
node 8 0.0 0.0 1.0
```
{{% /tab %}}
{{< /tabs >}}

The boundary conditions are applied to simulate triaxial constraints, fixing displacements appropriately on different node sets:

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
fix 1 0 1 1
fix 2 0 0 1
fix 3 1 0 1
fix 4 1 1 1
fix 5 0 1 0
fix 6 0 0 0
fix 7 1 0 0
fix 8 1 1 0
```
{{% /tab %}}
{{< /tabs >}}

The Drucker–Prager material is defined with specified parameters for elasticity, yield surface, and hardening behavior:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
model.nDMaterial("DruckerPrager", 2,
    K       = 27777.78 ,
    G       =  9259.26 ,
    Fy      =     5.0  ,
    Rvol    =     0.398,
    Rbar    =     0.398,
    Fs      =     0.0  ,
    Fo      =     0.0  ,
    Hsat    =     0.0  ,
    H       =     0.0  ,
    theta   =     1.0  ,
    delta2  =     0.0  ,
    density =   1.7
)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
nDMaterial DruckerPrager 2 \
   -K      27777.78  \
   -G       9259.26  \
   -Fy         5.0   \
   -Rvol       0.398 \
   -Rbar       0.398 \
   -Fs         0.0   \
   -Fo         0.0   \
   -Hsat       0.0   \
   -H          0.0   \
   -theta      1.0   \
   -delta2     0.0   \
   -density    1.7
```
{{% /tab %}}
{{< /tabs >}}

The model includes a single `stdBrick` element to represent the soil specimen:

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
element stdBrick 1 1 2 3 4 5 6 7 8 2 0.0 0.0 0.0
```
{{% /tab %}}
{{< /tabs >}}

## Recorders

Nodal displacements and Gauss point quantities such as stress, strain, and material state variables are recorded:

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
set step 0.1

recorder Node -file out/displacements1.out -time -dT $step -nodeRange 1 8 -dof 1 2 3 disp

recorder Element -ele 1 -time -file out/stress1.out  -dT $step material 2 stress
recorder Element -ele 1 -time -file out/strain1.out  -dT $step material 2 strain
recorder Element -ele 1 -time -file out/state1.out   -dT $step material 2 state
```
{{% /tab %}}
{{< /tabs >}}

## Loading

Two loading patterns are defined: the first applies hydrostatic pressure, and the second imposes axial deviatoric stress:

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
set p 10.0
set pNode [expr -$p * 0.25]

pattern Plain 1 {Series -time {0 10 100} -values {0 1 1} -factor 1} {
    load 1  $pNode    0.0 0.0
    load 2  $pNode $pNode 0.0
    load 3     0.0 $pNode 0.0
    load 5  $pNode    0.0 0.0
    load 6  $pNode $pNode 0.0
    load 7     0.0 $pNode 0.0
}

pattern Plain 2 {Series -time {0 10 100} -values {0 1 5} -factor 1} {
    load 5  0.0 0.0 $pNode
    load 6  0.0 0.0 $pNode
    load 7  0.0 0.0 $pNode
    load 8  0.0 0.0 $pNode
}
```
{{% /tab %}}
{{< /tabs >}}

## Analysis

The analysis uses standard OpenSees commands to control the solution procedure and apply the loads incrementally:

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
integrator LoadControl 0.1
numberer RCM
system SparseGeneral
constraints Transformation
test NormDispIncr 1e-5 1 1
algorithm Newton
analysis Static

puts "starting the hydrostatic analysis..."
set startT [clock seconds]
analyze 1000
set endT [clock seconds]

puts "triaxial shear application finished..., [getTime]"
```
{{% /tab %}}
{{< /tabs >}}

The output of the simulation should look as follows:

![](img/stdout.png)

The displacements over time are:

![Displacements over time](img/u.png)


