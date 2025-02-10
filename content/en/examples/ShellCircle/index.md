---
title: Shell undergoing finite rotations
render: circle.glb
thumbnail: img/examples/ShellCircle.png
downloads:
  Python: ["circle.py",  "requirements.txt"]
  Tcl:    ["circle.tcl", "requirements.txt"]
---


Here we investigate the roll-up problem previously considered for [frames](../framecircle), now with corotational shells.

Next we create an [`ElasticShell`](https://opensees.stairlab.io/user/manual/section/ElasticShell.html) section.

{{< tabs tabTotal="2" >}}
{{% tab name="Python (RT)" %}}
```python
#                                           tag E   nu     h    rho
model.section("ElasticShell", 1, E, 0.25, 1.175, 1.27)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
# create the material
section ElasticShell  1   3.0e3  0.25  1.175  1.27
```
{{% /tab %}}
{{< /tabs >}}

After running the Python variant of the analysis, the following plot is generated:

![Nodal displacements and rotations](img/plot.png)
