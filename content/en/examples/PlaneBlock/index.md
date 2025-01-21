---
title: Built-in mesh tools
thumbnail: img/examples/plane_block.png
tags: ["CE222"]
description: A finite element analysis is performed of a plane tapered cantilever using constant-strain triangles.
render: model.glb
---

![alt text](img/image.png)

A finite element analysis is performed of a plane tapered cantilever using constant-strain triangles. 
Visualization is performed in the script [`render.py`](render.py) using the [`veux`](https://pypi.org/project/veux) library.

Each node of the analysis has two displacement degrees of freedom. Thus the model is defined with
`ndm = 2` and `ndf = 2`. 

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

As with the example of a [tapered beam](../planetaper/), the [ElasticIsotropic](https://opensees.stairlab.io/user/manual/material/ndMaterials/ElasticIsotropic.html) material model is employed.

```python
E = 4e3
nu = 0.25 # Poisson's ratio
model.material("ElasticIsotropic", 1, E, nu, 0, "-plane-strain")
```

{{< fold plane_block.py "analysis script" >}}

