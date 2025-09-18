---
title: Plane Tapered Cantilever
thumbnail: img/examples/plane_taper.png
tags: ["CE222"]
description: A finite element analysis is performed of a plane tapered cantilever using constant-strain triangles.
render: model.glb
draft: true
downloads:
  Python: ["plane_taper.py"]
---

A finite element analysis is performed of a plane tapered cantilever using constant-strain triangles. 
Visualization is performed in the script [`render.py`](render.py) using the [`veux`](https://pypi.org/project/veux) library.

## Model

We begin by setting up a 2D model:
```python
import xara
model = xara.Model(ndm=3, ndf=3)
```
The [ElasticIsotropic](https://xara.so/user/manual/material/ndMaterials/ElasticIsotropic.html) material model is employed.

```python
model.material("ElasticIsotropic", 1, 10_000.0, 0.25, 0)
```

The material is added to a `"PlaneStress"` section, which enforces the plane stress constraint.
```python
model.section("PlaneStress", 1, 1, thickness)
```

Once again the `surface` method is used to generate the finite element mesh. However, in the present study we omit the `element` argument so that only nodes are generated:
```python
mesh = model.surface((nx, ny),
              points={
                1: [  0.0,   0.0],
                2: [   L,    L*r],
                3: [   L,  b-L*r],
                4: [  0.0, b    ]
              })
```
The resulting `mesh` variable is then used to manually construct the triangular elements:
```python
elem = 1
for cell in mesh.cells:
    nodes = mesh.cells[cell]
    model.element("tri31",   elem, [nodes[0], nodes[1], nodes[2]], section=1)
    model.element("tri31", elem+1, [nodes[0], nodes[2], nodes[3]], section=1)
    elem += 2
```

## Loads

Note that care must be taken to apply the distributed load at the tip in a consistent manner. For elements with linear interpolation at the boundary one has:
```python
from xara.helpers import find_node, find_nodes

tip = list(find_nodes(model, x=L))
for node in tip:
    px = load/len(tip)

    # Divide load at edges by two
    if abs(model.nodeCoord(node, 2)) in {7.5, 22.5}:
        px /= 2
    model.load(node, (px, 0.0), pattern=1)
```
where we've used the `find_nodes` helper function from the `xara.helpers` module.

The stress field looks like:

{{< render stress.glb >}}

The full script is given below:
{{< fold plane_taper.py "analysis script" >}}
