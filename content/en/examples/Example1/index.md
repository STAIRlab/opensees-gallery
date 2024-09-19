---
title: "Example 1: Linear Truss"
weight: 10
tags: ["Truss", "Python", "Tcl"]
categories: ["Basic", "Elastic"]
thumbnail:  img/BasicTruss.png
description: >-
  A finite element model of a simple truss is created,
  and static analysis is performed.

keywords: ["structural analysis", "structural engineering"]
---


![Example 1.1](img/Example1.svg)

This example is of a linear-elastic three bar truss, as shown in
the figure above, subject to static loads. The purpose of this
example is to develop the basic requirements for performing
finite element analysis with OpenSees.
This includes the definition of nodes,
materials, elements, loads and constraints. 

Scripts for this example can be downloaded for either
Python or Tcl:

- [`Example1.py`](./Example1.py)
- [`Example1.tcl`](./Example1.tcl)



## Model

We begin the simulation by creating a `Model`, which will manage
the nodes, elements, loading and state. This is done through
either Python or Tcl as follows:

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
model -ndm 2 -ndf 2
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
import opensees.openseespy as ops

model = ops.Model(ndm=2, ndf=2)
```
{{% /tab %}}
{{< /tabs >}}
where we've specified `2` for the spatial dimension `ndm`, and
`2` for the number of degrees of freedom `ndf`.

Next we define the four nodes of the structural model by specifying
a tag which identifies the node, and coordinates in the $x-y$ plane.
In general, the `node` constructor must be passed `ndm` coordinates.

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
# Create nodes & add to domain
#   tag  X    Y
node 1   0.0  0.0;
node 2 144.0  0.0;
node 3 168.0  0.0;
node 4  72.0 96.0;
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
# Create nodes
#         tag   X     Y
model.node(1,   0.0,  0.0)
model.node(2, 144.0,  0.0)
model.node(3, 168.0,  0.0)
model.node(4,  72.0, 96.0)
```
{{% /tab %}}
{{< /tabs >}}

The restraints at the nodes with reactions (ie, nodes `1`, `2`, and `3`)
are then defined.

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
# Set the boundary conditions
#  tag  X  Y
fix 1   1  1;
fix 2   1  1;
fix 3   1  1;
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
# set the boundary conditions
#    nodeID xRestrnt? yRestrnt?
model.fix(1, 1, 1)
model.fix(2, 1, 1)
model.fix(3, 1, 1)
```
{{% /tab %}}
{{< /tabs >}}


Since the truss elements have the same elastic material,
a single Elastic material object is created. The first
argument assigns the tag `1` to the material, and the
second specifies a Young's modulus of `3000`.

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
# Create Elastic material prototype
uniaxialMaterial Elastic 1 3000;
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
# Create Elastic material prototype
model.uniaxialMaterial("Elastic", 1, 3000)
```
{{% /tab %}}
{{< /tabs >}}

Finally, define the elements. The syntax for creating
the truss element requires the following arguments:
1. the element name, in this case always `"Truss"`,
2. the element tag, in this case `1` through `3`,
3. the nodes that the element is connected to,
4. the cross-sectional area, in this case `10.0` for element `1` and `5.0` for elements `2` and `3`.
5. the tag of the material assigned to the element, in this case always `1`

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
element Truss 1 1 4 10.0 1;
element Truss 2 2 4  5.0 1;
element Truss 3 3 4  5.0 1;
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
#              Type   tag  nodes  Area  material
model.element("Truss", 1, (1, 4), 10.0,    1   )
model.element("Truss", 2, (2, 4),  5.0,    1   )
model.element("Truss", 3, (3, 4),  5.0,    1   )
```
{{% /tab %}}
{{< /tabs >}}

## Loads

The final step before we can configure and run the analysis is to define
some loading. In this case we have two point loads at the apex of
the truss (node `4`).
In OpenSees, loads are assigned to load *patterns*, which define how loads
are scaled with each load *step*.
In Python, the simplest way to represent a nodal load is by a dictionary with
node numbers as keys, and corresponding load vector as values. For the problem at
hand, we want to apply a load to node `4` with `100` units in the $x$ direction, and
`-50` units in the $y$ direction; the corresponding definition is:
{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
set loads {4 100 -50}
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
loads = {4: [100, -50]}
```
{{% /tab %}}
{{< /tabs >}}

We then add a `"Plain"` load pattern to the model with these loads, 
and use the `"Linear"` option
to specify that it should be increased linearly with each new load step.
{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
pattern Plain 1 "Linear" "load $loads"
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
model.pattern("Plain", 1, "Linear", load=loads)
```
{{% /tab %}}
{{< /tabs >}}

<blockquote>

Note that it is common to define the `load` data structure
*inside* the call to the `pattern` function. This looks like:

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
pattern Plain 1 "Linear" {
  load 4 100 -50
}
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
model.pattern("Plain", 1, "Linear", load={
  4: [100, -50]
})
```
{{% /tab %}}
{{< /tabs >}}

</blockquote>

## Analysis

Next we configure that analysis procedure.
The model is linear, so we use a solution Algorithm of type `Linear`. 

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
algorithm Linear;
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
model.algorithm("Linear")
```
{{% /tab %}}
{{< /tabs >}}

Even though the solution is linear, we have to select a procedure for
applying the load, which is called an `Integrator`. 
For this problem, a `LoadControl` integrator is selected, which
advances the solution by incrementing the applied loads by a
factor of `1.0` each time the `analyze` command is called.

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
integrator LoadControl 1.0;
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
model.integrator("LoadControl", 1.0)
```
{{% /tab %}}
{{< /tabs >}}

The equations are formed
using a banded system, so the System is `BandSPD` (banded, symmetric
positive definite). This is a good choice for most moderate size models.
The equations have to be numbered, so typically an RCM numberer object
is used (for Reverse Cuthill-McKee). 
The constraints are most easily represented with a `Plain` constraint handler.

Once all the components of an analysis are defined, the Analysis 
itself is defined. For this problem a `Static` analysis is used.

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
analysis Static;
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
model.analysis("Static")
```
{{% /tab %}}
{{< /tabs >}}

Finally, one analysis step is performed by invoking `analyze`:
{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
analyze 1
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
model.analyze(1)
```
{{% /tab %}}
{{< /tabs >}}

When the analysis is complete the state of node `4` and all three elements
may be printed to the screen:

{{< tabs tabTotal="2" >}}
{{% tab name="Tcl" %}}
```tcl
print node 4
print ele
```
{{% /tab %}}
{{% tab name="Python (RT)" %}}
```python
model.print(node=4)
model.print("ele")
```
{{% /tab %}}
{{< /tabs >}}

```
    Node: 4
            Coordinates  : 72 96 
            commitDisps: 0.530093 -0.177894 
            unbalanced Load: 100 -50 

    Element: 1 type: Truss  iNode: 1 jNode: 4 Area: 10 Total Mass: 0 
             strain: 0.00146451 axial load: 43.9352 
             unbalanced load: -26.3611 -35.1482 26.3611 35.1482 
             Material: Elastic tag: 1
             E: 3000 eta: 0

    Element: 2 type: Truss  iNode: 2 jNode: 4 Area: 5 Total Mass: 0 
             strain: -0.00383642 axial load: -57.5463 
             unbalanced load: -34.5278 46.0371 34.5278 -46.0371 
             Material: Elastic tag: 1
             E: 3000 eta: 0

    Element: 3 type: Truss  iNode: 3 jNode: 4 Area: 5 Total Mass: 0 
             strain: -0.00368743 axial load: -55.3114 
             unbalanced load: -39.1111 39.1111 39.1111 -39.1111 
             Material: Elastic tag: 1
             E: 3000 eta: 0
```

For the node, displacements and loads are given. For the truss elements,
the axial strain and force are provided along with the resisting forces
in the global coordinate system.

The file `example.out`, specified in the recorder command, provides
the nodal displacements for the \(x\) and \(y\) directions of node `4`. The file
consists of a single line:

    1.0 0.530093 -0.177894 

The \(1.0\) corresponds to the load factor (pseudo time) in the model at
which point the recorder was invoked. The \(0.530093\) and \(-0.177894\)
correspond to the response at node `4` for the 1 and 2
degree-of-freedom. Note that if more analysis steps had been performed,
the line would contain a line for every analysis step that completed
successfully.

