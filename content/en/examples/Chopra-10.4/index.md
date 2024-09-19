---
title: "Matrix Eigenvalue Analysis"
thumbnail: img/ShearFrame5.png
tags: ["Eigen", "Frame", "Python", "Tcl"]
layout: single
# authors: ["Vesna Terzic"]
description: >-
    This example demonstrates how to perform eigenvalue analysis and plot
    mode shapes. 
---

This example is adapted from the OpenSees Wiki page [Eigen analysis of a two-storey shear frame](https://opensees.berkeley.edu/wiki/index.php/Eigen_analysis_of_a_two-story_shear_frame).

<hr />

This example demonstrates how to perform eigenvalue analysis and plot
mode shapes. 

An idealized two-storey shear frame (Example 10.4 from
"Dynamic of Structures" book by Professor Anil K. Chopra) is used for
this purpose. In this idealization beams are rigid in flexure, axial
deformation of beams and columns are neglected, and the effect of axial
force on the stiffness of the columns is neglected. Geometry and
material characteristics of the frame structure are shown in Figure 1.
Node and element numbering is given in Figure 2.

<figure>
  <img src="./ShearFrame5.png" />
  <figcaption aria-hidden="true">ShearFrame5.png</figcaption>
</figure>

## Instructions on how to run this example

To execute this ananlysis in OpenSees the user has to download this
files:
<ul>
<li><a href="./EigenAnal_twoStoryShearFrame8.tcl"><tt>EigenAnal_twoStoryShearFrame.tcl</tt></a></li>
</ul>

Place `EigenAnal_twoStoryShearFrame.tcl` in the same folder with the
OpenSees.exe. By double clicking on OpenSees.exe the OpenSees
interpreter will pop out. To run the analysis the user should type:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```bash
python EigenAnal_twoStoryShearFrame8.py
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```bash
python -m opensees EigenAnal_twoStoryShearFrame8.tcl
```
{{% /tab %}}
{{< /tabs >}}

and hit enter. To create output files (stored in directory "data") 
the user has to exit OpenSees interpreter by typing "exit".

## Create the model

Spatial dimension of the model and number of degrees-of-freedom (DOF)
at nodes are defined using <a href="https://opensees.berkeley.edu/wiki/index.php/model_command">model</a> command. In this example we have 2D model
with 3 DOFs at each node. This is defined in the following way:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
import opensees.openseespy as ops

model = ops.Model(ndm=2, ndf=3)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```Tcl
model BasicBuilder -ndm 2 -ndf 3
```
{{% /tab %}}
{{< /tabs >}}


Note: geometry, mass, and material characteristics are assigned to
variables that correspond to the ones shown in Figure 1 (e.g., the
height of the column is set to be 144 in. and assigned to variable h;
the value of the height can be accessed by $h).

Nodes of the structure (Figure 2) are defined using the <a
href="https://opensees.berkeley.edu/wiki/index.php/node_command" title="wikilink">node</a> command: 

{{< tabs tabTotal="2" >}}
{{%  tab  name="Python"  %}}
```python
model.node(1, 0.,   0.)
model.node(2, L ,   0.)
model.node(3, 0.,   h )
model.node(4, L ,   h )
model.node(5, 0., 2*h )
model.node(6, L , 2*h )
```
{{%  /tab  %}}
{{%  tab  name="Tcl"  %}}
```tcl
node 1 0. 0. ;
node 2 $L 0. ;
node 3 0. $h ;
node 4 $L $h ;
node 5 0. [expr 2*$h];
node 6 $L [expr 2*$h];
```
{{%  /tab  %}}
{{< /tabs >}}

The boundary conditions are defined next using single-point
constraint command <a href="https://opensees.berkeley.edu/wiki/index.php/fix_command" title="wikilink">fix</a>. In
this example nodes 1 and 2 are fully fixed at all three DOFs:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
model.fix(1, 1, 1, 1)
model.fix(2, 1, 1, 1)
```
{{%  /tab  %}}
{{%  tab  name="Tcl"  %}}
```tcl
fix 1 1 1 1; 
fix 2 1 1 1; 
```
{{%  /tab  %}}
{{< /tabs >}}


Masses are assigned at nodes 3, 4, 5, and 6 using <a
href="https://opensees.berkeley.edu/wiki/index.php/Mass_Command" title="wikilink">mass</a> command. Since the
considered shear frame system has only two degrees of freedom
(displacements in x at the 1st and the 2nd storey), the masses have to
be assigned in x direction only.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
model.mass(3,  m  , 0., 0. ) 
model.mass(4,  m  , 0., 0. ) 
model.mass(5, m/2., 0., 0. ) 
model.mass(6, m/2., 0., 0. )
```
{{%  /tab  %}}
{{%  tab  name="Tcl"  %}}
```tcl
mass 3 $m 0. 0. ; 
mass 4 $m 0. 0. ; 
mass 5 [expr $m/2.] 0. 0. ; 
mass 6 [expr $m/2.] 0. 0. ;
```
{{%  /tab  %}}
{{< /tabs >}}

The <a href="https://opensees.berkeley.edu/wiki/index.php/Geometric_Transformation_Command">geometric transformation</a> with id tag 1 is defined
to be linear.

```tcl
set TransfTag 1; 
geomTransf Linear $TransfTag ; 
```

The beams and columns of the frame are defined to be elastic using <a
href="https://opensees.berkeley.edu/wiki/index.php/Elastic_Beam_Column_Element">elasticBeamColumn</a> element. In order to make beams
infinitely rigid moment of inertia for beams (Ib) is set to very high
value (10e+12).

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
model.element("ElasticBeamColumn", 1, 1, 3, Ac, Ec, 2.*Ic, TransfTag)
model.element("ElasticBeamColumn", 2, 3, 5, Ac, Ec,    Ic, TransfTag)
model.element("ElasticBeamColumn", 3, 2, 4, Ac, Ec, 2.*Ic, TransfTag)
model.element("ElasticBeamColumn", 4, 4, 6, Ac, Ec,    Ic, TransfTag)
model.element("ElasticBeamColumn", 5, 3, 4, Ab, E,     Ib, TransfTag)
model.element("ElasticBeamColumn", 6, 5, 6, Ab, E,     Ib, TransfTag)
```
{{%  /tab  %}}
{{%  tab  name="Tcl"  %}}
```tcl
element elasticBeamColumn 1 1 3 $Ac $Ec [expr 2.*$Ic] $TransfTag; 
element elasticBeamColumn 2 3 5 $Ac $Ec $Ic $TransfTag; 
element elasticBeamColumn 3 2 4 $Ac $Ec [expr 2.*$Ic] $TransfTag; 
element elasticBeamColumn 4 4 6 $Ac $Ec $Ic $TransfTag; 
element elasticBeamColumn 5 3 4 $Ab $E $Ib $TransfTag;
element elasticBeamColumn 6 5 6 $Ab $E $Ib $TransfTag; 
```
{{%  /tab  %}}
{{< /tabs >}}

To comply with the assumptions of the shear frame (no vertical
displacemnts and rotations at nodes) end nodes of the beams are
constrained to each other in the 2nd DOF (vertical displacement) and the
3rd DOF (rotation). <a href="https://opensees.berkeley.edu/wiki/index.php/EqualDOF_command">EqualDOF</a> command is used to imply these
constraints.

```tcl
equalDOF 3 4 2 3;
equalDOF 5 6 2 3;
```

## Define recorders

For the specified number of eigenvalues (numModes) (for this example
it is 2) the eigenvectors are recorded at all nodes in all DOFs using <a
href="https://opensees.berkeley.edu/wiki/index.php/Node_Recorder" title="wikilink"> node recorder</a> command.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
for k in range(numModes):
    model.recorder("Node", f"eigen {k}", file=f"modes/mode{k}.out", nodeRange=[1, 6], dof=[1, 2, 3])
```
{{%  /tab  %}}
{{%  tab  name="Tcl"  %}}
```tcl
foreach k [range $numModes] {
  recorder Node -file [format "modes/mode%i.out" $k] -nodeRange 1 6 -dof 1 2 3 "eigen $k" 
}
```
{{%  /tab  %}}
{{< /tabs >}}

## Perform eigenvalue analysis and store periods into a file

The eigenvalues are calculated using <a href="https://opensees.berkeley.edu/wiki/index.php/Eigen_Command">eigen commnad</a> and stored in lambda variable.

```tcl
set lambda [eigen $numModes];
```

The periods and frequencies of the structure are calculated next.

```tcl
set omega {} 
set f {}
set T {} 
set pi 3.141593
foreach lam $lambda { 
  lappend omega [expr sqrt($lam)];
  lappend f [expr sqrt($lam)/(2*$pi)];
  lappend T [expr (2*$pi)/sqrt($lam)];
}
```


The periods are stored in a `Periods.txt` file inside of directory
`modes/`.

```tcl
set period "modes/Periods.txt" 
set Periods [open $period "w"] 
foreach t $T {
  puts $Periods " $t" 
} 
close $Periods 
```

## Record the eigenvectors

For eigenvectors to be recorded <a href="https://opensees.berkeley.edu/wiki/index.php/Record_Command"> record</a> command has to be issued following the
eigen command.

```tcl
record
```

## Display mode shapes

TODO

Example Provided by: <span style="color:blue"> Vesna Terzic, UC Berkeley</span>

