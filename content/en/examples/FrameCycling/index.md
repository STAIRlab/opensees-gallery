---
title: Force vs. Displacement formulations
description: "An investigation of various frame formulations"
thumbnail: img/examples/lehman.png
tags: ["Frame"]
draft: true
downloads:
  Python: ["column_cycles.py", "leh415.txt"]
  Tcl: ["column_cycles.tcl", "SingleCycle.tcl", "LibUnits.tcl"]
---

Investigate the two most commonly used OpenSees elements for modeling beam-column
elements: the [force](https://xara.so/user/manual/model/elements/frame/ForceFrame.html)  and cubic [displacement](https://xara.so/user/manual/model/elements/frame/CubicFrame.html) formulations. 

<figure style="text-align: center;">
<img src="img/lehman.png" width="50%">
<figcaption>Schematic of the Lehman column experiment</figcaption>
</figure>

Although the parameters for defining these two elements are the same, a beam-column member needs to be modeled differently
using these two elements to achieve a comparable level of accuracy. 
The intent of this example is to show how to properly model inelastic beam-columns with both force and displacement formulations. 

|    |     |
| :--- | :--- |
| Diameter | 24 in. |
| Height | 96 in. |
| Longitudinal | $22 ~\# 5 \mathrm{~Gr} 60$ |
| Reinforcement | $\rho_{\ell}=1.5 \%$ |
|  | $f_y=70 \mathrm{~ksi}$ |
| Transverse | $\# 2 ~@~ 1.25 \mathrm{~in}$. |
| Reinforcement | $\left(\rho_{\mathrm{t}}=0.7 \%\right)$ |
|               | $f_y=96.6 \mathrm{~ksi}$ |
| Concrete | $f'_c=4.4 \mathrm{~ksi}$ |


## Model Generation

- The column is modeled using either force-based or displacement-based elements.
- The column height <code>H</code> is 96 inches

```python
import xara

# Create a 2D model with 3 DOFs per node
model = xara.Model(ndm=2, ndf=3)

H = 96.0 * inch  # Column height

# Define nodes
model.node(1, (0.0, 0.0))
for i in range(ne):
    model.node(i + 2, (0.0, (i + 1) * H/ne))
```


### Boundary Conditions

Node 1 is fixed in both horizontal and vertical directions.

```
model.fix(1, (1, 1, 1))
```

### Materials

#### Longitudinal reinforcement

- Bar area <code>barArea</code> is 0.31 square inches (for bar #5).
- Bar diameter <code>db</code> is 0.625 inches.
- Yield strength <code>fy</code> of longitudinal bars is 70 ksi.
- Modulus of elasticity <code>Es</code> of steel is 29,000 ksi.
- Tangent at initial strain hardening (<code>Esf</code>) is calibrated from coupon tests.

#### Transverse reinforcement

- Spiral diameter <code>dh</code> is 0.25 inches.
- Number of hoops <code>NoHoops</code> is 1.
- Area of transverse reinforcement bar (<code>Asp1</code>) is 0.0491 square inches.
- Centerline distance between spirals <code>stran</code> is 1.25 inches.
- Yield strength of the hoop (<code>fyh</code>) is 96.6 ksi.


#### Unconfined concrete

- Compressive strength $f'_c$ (<code>fc</code>) is 4.4 ksi.
- Strain corresponding to <code>fc</code> is <code>eps0</code>.
- Ultimate strain for unconfined concrete is <code>epss</code>.
- Elastic modulus <code>Ec</code> is calculated based on ACI 318.

```python
fc = 4.4 * ksi  # Compressive strength of plain concrete
eps0 = 0.002    # Strain corresponding to fc'
epss = 0.005    # Ultimate strain for unconfined concrete
Ec = 57000.0 * sqrt(fc * 1000.0) / 1000.0
```

#### Confined concrete

Compressive strength and strain are determined using Mander’s equations (Eq. 6 in Mander, 1988):

$$
ecr = \frac{E_c}{(E_c - f_{cc} / \epsilon_{cc})}
$$

### Section

- The diameter <code>D</code> is 24 inches.
- The clear cover of concrete <code>clearCover</code> is 0.75 inches.

```python
D = 24.0 * inch  # Column diameter
clearCover = 0.75 * inch  # Clear cover of concrete

theta = 360.0 / numBars
model.section("fiberSec", secnTag, GJ=1e8)
# Core patch
model.patch("circ", coreTag, nfCoreT, nfCoreR, 0, 0, 0, ri, 0.0, 360.0, section=secnTag)
# Cover patch
model.patch("circ", coverTag, nfCoverT, nfCoverR, 0, 0, ri, ro, 0.0, 360.0, section=secnTag)
# Reinforcing bars
model.layer("circ", steelTag, numBars, barArea, 0, 0, rl, theta / 2.0, 360.0 - theta / 2.0, section=secnTag)
```

### Elements

Coordinate transformation is applied using the Corotational method.

```python
# Define coordinate transformation
transfTag = 1
model.geomTransf("Corotational", transfTag)

for i in range(ne):
    if eleType == 1:
        model.element("forceBeamColumn", i + 1, (i+1, i+2), nIP, secTag, transfTag)
    elif eleType == 2:
        model.element("dispBeamColumn", i + 1, (i+1, i+2), nIP, secTag, transfTag)
```

## Analysis

### Gravity

### Cycling

```python
# Define recorders for displacement and force
model.recorder("Node", "disp", "-time", file="out/Disp.out", node=ne+1, dof=1)
model.recorder("Node", "reaction", "-time", file="out/Force.out", node=1, dof=1)
```

## Resources

The slides from the original presentation can be downloaded from <a href="https://opensees.berkeley.edu/wiki/images/c/c5/FFvsDF.pdf">here</a> 
and video of the seminar can be found here: <a href="http://www.youtube.com/watch?v=yk-1k2aF53E">http://www.youtube.com/watch?v=yk-1k2aF53E</a>


<ul>
<li>Supporting files to be stored in the same folder with the main file:
<ul>
<li><a href="leh415.txt">leh415.txt</a> : experimental force-displacement response
</ul>
</ul>
