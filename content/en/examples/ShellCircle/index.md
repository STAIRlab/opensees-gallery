---
title: Shell undergoing finite rotations
render: circle.glb
thumbnail: img/examples/ShellCircle.png
description: Geometrically nonlinear analysis of a cantilever rolling up under the action of a point moment, performed with shell finite elements.
downloads:
  Python: ["circle.py",  "requirements.txt"]
  Tcl:    ["circle.tcl", "requirements.txt"]
---


Here we investigate the roll-up problem previously considered for [frames](../framecircle), now with corotational shells.

As always, we begin by creating a `Model` (see for example [this](../example7) problem).
{{< tabs tabTotal="2" >}}
{{% tab name="Python (RT)" %}}
```python
import opensees.openseespy as ops

model = ops.Model(ndm=3, ndf=6)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
model -ndm 3 -ndf 6
```
{{% /tab %}}
{{< /tabs >}}

Next we create an [`ElasticShell`](https://opensees.stairlab.io/user/manual/section/ElasticShell.html) section.

{{< tabs tabTotal="2" >}}
{{% tab name="Python (RT)" %}}
```python
E = 1e4
thickness = 1.0
nu = 0.0
model.section("ElasticShell", 1, E, nu, thickness)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
#                          E      nu  thick
section ElasticShell  1   1.0e4  0.0   1.0
```
{{% /tab %}}
{{< /tabs >}}

The loading will be applied in 40 increments.

In the Python version, we'll create a [`veux.Artist`](https://veux.io/library/artist/index.html) before starting the analysis
in order to draw snapshots of the deformed shape throughout the deformation.
```python
# Render the reference configuration
artist = veux.create_artist(model, vertical=3)
artist.draw_surfaces()
artist.draw_outlines()
```

Now we proceed to [`analyze`](https://opensees.stairlab.io/user/manual/analysis/analyze.html):
```python
u = []
r = []
load = []
for i in range(nsteps):
    print(f"step {i+1} of {nsteps}")
    if ops.analyze(1) != 0:
        break
    ctime += dt
    if ctime > dt_record:
        ctime = 0.0
        artist.draw_outlines(state=ops.nodeDisp)

    load[i+1] = ops.getTime()
    u[i+1]   =  ops.nodeDisp(CNode, 3)
    r[i+1]   = -ops.nodeDisp(CNode, 5)
```


After running the Python variant of the analysis, the following plot is generated:

![Nodal displacements and rotations](img/plot.png)

