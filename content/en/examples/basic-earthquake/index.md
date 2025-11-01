---
title: "Linear Dynamic analysis of ground shaking"
meta:
  title: "Dynamic analysis of a basic building model combining frame and shell elements in OpenSees"
weight: 15
tags: ["Frame", "Shell", "Dynamic"]
categories: ["Basic", "Elastic", "Earthquake"]
description: >-
  A finite element model of a single-story structure composed of frame columns and a shell roof is constructed and subjected to dynamic earthquake excitation.
keywords: ["structural analysis", "earthquake engineering"]
downloads:
  Python: ["main.py", "tabasFN.txt", "tabasFP.txt"]
---

This example shows how to realize a simple three-dimensional finite element model in OpenSees, combining frame and shell elements, and performing dynamic analysis under earthquake excitation. 
The model consists of four columns supporting a flat roof, which is represented by a quadrilateral shell. 
It serves as a minimal working example to introduce dynamic loading procedures and the handling of multiple element types.

## Model Setup

We begin by creating a {{< link model_class >}}Model{{< /link >}} configured for three-dimensional analysis, specifying six degrees of freedom per node. 
Each node will have three translational and three rotational degrees of freedom.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
import xara

model = xara.Model(ndm=3, ndf=6)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
```
{{% /tab %}}
{{< /tabs >}}

### Geometry and Nodes

Nodes are placed at the corners of a square plan, with base nodes at ground level and roof nodes elevated by the story height. 
The coordinates are given directly when constructing the nodes.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
# Define node coordinates
base = [1, 2, 3, 4]
roof = [5, 6, 7, 8]

coords = {
    1: (-12.0,  12.0,  0.0),
    2: ( 12.0,  12.0,  0.0),
    3: ( 12.0, -12.0,  0.0),
    4: (-12.0, -12.0,  0.0),
    5: (-12.0,  12.0, 12.0),
    6: ( 12.0,  12.0, 12.0),
    7: ( 12.0, -12.0, 12.0),
    8: (-12.0, -12.0, 12.0),
}

for tag, xyz in coords.items():
    model.node(tag, xyz)

# Fully fix the base nodes
for tag in base:
    model.fix(tag, (1, 1, 1, 1, 1, 1))
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
```
{{% /tab %}}
{{< /tabs >}}

The base nodes are fully constrained, preventing any movement or rotation.

### Materials and Sections

Frame and shell elements in OpenSees rely on section objects to supply cross-sectional stiffness and mass properties.
Here, two types of sections are created: an *ElasticFrame* section for the columns, and an *ElasticShell* section for the roof.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
E = 29500.0 * ksi
poisson = 0.3
density = 490.0 * pcf
depth = 20 * inch
area = depth ** 2
i_zz = i_yy = depth ** 4 / 12.0
j_tors = 10 * i_zz

# Frame section for columns
model.section("ElasticFrame", 1, E=E, G=E/(2*(1+poisson)), A=area, Iz=i_zz, Iy=i_yy, J=j_tors)

# Shell section for roof
thickness = 6 * inch
model.section("ElasticShell", 2, E, poisson, thickness, density)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
```
{{% /tab %}}
{{< /tabs >}}

The *ElasticFrame* section groups the basic elastic stiffness properties of the columns, including axial, bending, and torsional stiffness. 
The *ElasticShell* section defines both in-plane (membrane) and out-of-plane (bending) behavior for the roof.

### Elements

Elements are now created to connect the nodes. 
Each column is modeled with a *PrismFrame* element, while the roof diaphragm is modeled using a *ASDShellQ4* shell element.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
model.geomTransf("Linear", 1, (0, 1, 0))

for tag, (ni, nj) in enumerate(zip(base, roof), start=1):
    model.element("PrismFrame", tag, (ni, nj), section=1, transform=1)

model.element("ASDShellQ4", 5, roof, section=2)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
```
{{% /tab %}}
{{< /tabs >}}

The geometric transformation assigned to the frame elements ensures proper orientation of the local axes, aligning the local $z$-axis with the global $y$-axis.

## Loads and Gravity Analysis

Gravity loads are applied at the roof nodes to represent the weight of the roof. 
A *Plain* load pattern with "Constant" scaling is used.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
p = density * (24.0 * foot)**2 * thickness

model.pattern("Plain", 1, "Constant")
for i in roof:
    model.load(i, (0.0, 0.0, -p, 0.0, 0.0, 0.0), pattern=1)

# Apply Rayleigh damping
model.rayleigh(0.0, 0.0, 0.0, 0.0018)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
```
{{% /tab %}}
{{< /tabs >}}

A small amount of Rayleigh mass-proportional damping is added to stabilize the dynamic response without significantly altering the system behavior.

## Dynamic Excitation

### Ground Motions

Earthquake excitations are applied using the Tabas fault-normal and fault-parallel ground motion records. 
Each component is assigned to a different translational degree of freedom.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
dt = 0.02
model.timeSeries("Path", 2, filePath="tabasFN.txt", dt=dt, factor=gravity)
model.timeSeries("Path", 3, filePath="tabasFP.txt", dt=dt, factor=gravity)

model.pattern("UniformExcitation", 2, 1, accel=2)
model.pattern("UniformExcitation", 3, 2, accel=3)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
```
{{% /tab %}}
{{< /tabs >}}

### Analysis Configuration

The transient dynamic analysis is configured using standard procedures. 
Newmark time integration is used with parameters \( \gamma = 0.5 \) and \( \beta = 0.25 \), corresponding to the average acceleration method.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
model.system("UmfPack")
model.numberer("RCM")
model.constraints("Plain")
model.test("EnergyIncr", 1.0e-8, 20)
model.algorithm("Newton")
model.integrator("Newmark", 0.5, 0.25)
model.analysis("Transient")
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
```
{{% /tab %}}
{{< /tabs >}}

The system of equations is solved directly using a sparse solver. An energy increment test is used to determine convergence.

## Running the Analysis

The analysis is performed over 2500 time steps, each of 0.01 seconds. Roof displacements are recorded at each time step.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
roof = [node for node in model.getNodeTags() if model.nodeCoord(node)[2] != 0.0]

displacements = {node: [model.nodeDisp(node)] for node in roof}

for i in range(2500):
    status = model.analyze(1, 0.01)
    if status != ops.successful:
        raise RuntimeError(f"analysis failed at time {model.getTime()}")

    for node in roof:
        displacements[node].append(model.nodeDisp(node))
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
```
{{% /tab %}}
{{< /tabs >}}

## Post-Processing

After the analysis, displacements can be plotted to visualize the structural response.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
import matplotlib.pyplot as plt

plt.plot(displacements[5])
plt.xlabel("Time Step")
plt.ylabel("Displacement (inches)")
plt.title("Roof Node Displacement History")
plt.grid(True)
plt.show()
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
```
{{% /tab %}}
{{< /tabs >}}



