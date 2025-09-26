---
title: Rigid Offsets
meta:
  title: "A verification example for frame element offset handling in OpenSees"
draft: true
tags: ["Frame", "Offset"]
weight: 30
draft: false
description: >-
  This example tests the effect of rigid joint offsets in a diamond-shaped frame.
  The analytical solution is known, and the test is used to verify the correct
  treatment of offset geometry in a 3D frame element.
downloads:
  Python: ["diamond.py"]
  Tcl: ["diamond.tcl"]
---


This test case consists of a simple two-node frame element arranged in a diamond pattern.
Rigid offsets at both ends rotate the element relative to the applied force direction.
This configuration is highly sensitive to geometric assumptions, making it ideal
for verifying the implementation of joint offsets in 3D frame elements.


## Model

We begin by importing necessary libraries and defining a function that computes the analytical solution using a transformation approach:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
import xara
import veux
```
{{% /tab %}}
{{< /tabs >}}

Next, the model is built using the `xara` API, which mirrors OpenSeesRT's structured syntax:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
def create_diamond():
    m = xara.Model(ndm=3, ndf=6)

    L   = 5
    off = 0.1 * L
    X   = L / np.sqrt(2)
    E   = 30
    I   = 1
    A   = 500 * I

    m.node(1, (0, 0, 0))
    m.node(2, (X, X, 0))
    m.fix(1, (0, 1, 1, 1, 1, 1))
    m.fix(2, (1, 0, 1, 1, 0, 0))
```
{{% /tab %}}
{{< /tabs >}}

The rigid offsets are defined by passing an `offset` dictionary to the `geomTransf` command:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
m.geomTransf("Linear", 1, (0, 0, 1),
             offset={
                1: ( off/np.sqrt(2), off/np.sqrt(2), 0),
                2: (-off/np.sqrt(2),-off/np.sqrt(2), 0),
             }
)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
geomTransf Linear 1  0 0 1  -offset {
  1  0.35355339059327373  0.35355339059327373 0
  2 -0.35355339059327373 -0.35355339059327373 0
}
```
{{% /tab %}}
{{< /tabs >}}


{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
    m.section("ElasticFrame", 1, E=E, A=A, Iy=I, Iz=I, G=1, J=3/2*I)
    m.element("ForceFrame", 1, (1, 2), transform=1, section=1, shear=0)
```
{{% /tab %}}
{{< /tabs >}}

A vertical unit load is applied at the free end, and a single analysis step is performed:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
    m.pattern("Plain", 1, "Linear", loads={2: (0, 1, 0, 0, 0, 0)})

    P = -4 * L**2 / (E * I)
    m.integrator("LoadControl", P)
    m.analysis("Static")
    m.test("NormDispIncr", 1e-8, 2)
    m.analyze(1)

    print(P / diamond_solution(E*I, E*A, L, off=off) / L)
    print(m.nodeDisp(1))
    print(m.nodeDisp(2))
    print(m.nodeDisp(2, 2) / L)
    return m
```
{{% /tab %}}
{{< /tabs >}}

## Validation

Recall the stiffness $\boldsymbol{K}_e$ of a linear 2D Euler-Bernoulli beam:

$$
\boldsymbol{K}_e = \begin{bmatrix}
EA/L_e &       0 &       0 \\
    0 & 4 EI/L_e & 2 EI/L_e \\
    0 & 2 EI/L_e & 4 EI/L_e \\
\end{bmatrix}
$$

This is transformed into the angled configuration using the transformation:

$$
\boldsymbol{A}_v = \begin{bmatrix}
-dX/L_e   &  dY/L_e   & 0 &  dX/L_e   \\
-dY/L_e^2 & -dX/L_e^2 & 0 &  dY/L_e^2 \\
-dY/L_e^2 & -dX/L_e^2 & 1 &  dY/L_e^2 \\
\end{bmatrix}
$$

and joint offsets are similarly applied with:

$$
\boldsymbol{A}_o = 
\begin{bmatrix}
0 & 1 &               0 \\
1 & 0 & -L_o/\sqrt{2}   \\
0 & 0 &               1 \\
0 & 0 &  L_o/\sqrt{2}   \\
\end{bmatrix}
$$

```python
import numpy as np
def diamond_solution(EI, EA, L, off=0):
    Le = L - 2*off
    dX = dY = Le/np.sqrt(2)
    Ag = np.array([[-dX/Le   ,  dY/Le   , 0,  dX/Le   ],
                   [-dY/Le**2, -dX/Le**2, 0,  dY/Le**2],
                   [-dY/Le**2, -dX/Le**2, 1,  dY/Le**2]])
    Ao = np.array([[0, 1,              0],
                   [1, 0,-off/np.sqrt(2)],
                   [0, 0,              1],
                   [0, 0, off/np.sqrt(2)]])
    A  = Ag @ Ao
    Ke = np.array([[EA/Le,       0,       0],
                   [    0, 4*EI/Le, 2*EI/Le],
                   [    0, 2*EI/Le, 4*EI/Le]])
    K = A.T @ Ke @ A
    return 1 / np.linalg.solve(K, [1, 0, 0])
```

## Visualization

The resulting deformed shape is plotted using `veux`, with the displacement field applied:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
if __name__ == "__main__":
    model = create_diamond()
    a = veux.create_artist(model)
    a.draw_outlines()
    a.draw_origin()
    a.draw_outlines(state=model.nodeDisp)
    a.draw_axes()
    veux.serve(a)
```
{{% /tab %}}
{{< /tabs >}}
