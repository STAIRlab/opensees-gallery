---
title: Solid extrusions
thumbnail: img/examples/tetra-channel.png
tags: ["Solid"]
weight: 15
description: |
  Mesh generation utilities are used to create a 3D tetrahedron model of a cantilever beam with a channel cross section.
downloads:
  Python: ["tetra.py", "requirements.txt"]
  Tcl: ["tetra.tcl"]
---

This investigation begins with a plane triangle mesh of a channel cross section. Here we'll use the [`xsection`](https://peer-open-source.github.io/xsection/) library: 
```python
from xsection.library import Channel
shape = Channel(d=16, b=8, tf=1.0, tw=1.0)
```
Next we use the `ExtrudeTetrahedron` class which will generate node locations and connectivity for a tetrahedron mesh:
```python
from shps.frame.extrude import ExtrudeTetrahedron

ex = ExtrudeTetrahedron(shape.model)
```

Next we setup a `Model` instance for the 3D simulation:
```python
model = xara.Model(ndm=3, ndf=3)
model.material("ElasticIsotropic", 1, 29e3, 0.23)
model.pattern("Plain", 1, "Linear")
```
And finally we perform `n = 100` extrusions:

```python
n = 100
for i in range(n):
    for tag, coords in ex.nodes():
        model.node(tag, tuple(coords))
        if i==0 and coords[-1] == 0:
            model.fix(tag, (1, 1, 1))
        elif i == n-1:
            model.load(tag, (0, -1, 0), pattern=1)

    for tag, cell in ex.cells():
        model.element("FourNodeTetrahedron", tag, tuple(cell), 1)

    ex.advance()
```

This will create the following finite element model, which is rendered below with [veux](https://veux.io):
```python
import veux
veux.render(model)
```

![Channel section](img/channel.png)

Next we perform a basic static analysis:
```python
model.integrator("LoadControl", 2)
model.system("Umfpack")
model.analysis("Static")
model.analyze(1)
```

After performing the analysis the deformed shape is rendered with:
```python
artist = veux.create_artist(model, ndf=3)
artist.draw_outlines(state=model.nodeDisp)
artist.draw_surfaces(state=model.nodeDisp)
```

![Deformed cantilever](img/channel-deformed.png)
