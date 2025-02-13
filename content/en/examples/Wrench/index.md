---
title: Wrench
render: model.glb
thumbnail: img/wrench.png
tags: ["Plane", "CE222"]
description: "Static analysis of a wrench"
downloads:
  Python: ["model.py", "render.py"]
---


This problem is adapted from Logan (2012), Problem 7–28.

The problem is implemented for both quadrilateral and triangular finite elements.
In both versions the `surface` method is used, but extra work is required for triangles.
For the triangular mesh, the [`Tri31`](https://opensees.stairlab.io/user/manual/model/elements/Tri31.html) element is used.

{{< tabs tabTotal="2" >}}
{{% tab name="Quadrilateral" %}}
```python
def create_quads():
    model = ops.Model(ndm=2, ndf=2)
    model.nDMaterial("ElasticIsotropic", 1, 200e3, 0.25)

    for num,block in blocks.items():
        model.surface(divs[num],
                      element="quad", args=(1, "PlaneStrain", 1),
                      points = block)

    return model

```
{{% /tab %}}
{{% tab name="Triangle" %}}
```python
def create_tris():
    model = ops.Model(ndm=2, ndf=2)
    model.nDMaterial("ElasticIsotropic", 1, 200e3, 0.25)

    elem = 1
    for num,block in blocks.items():
        # Because no element argument is passed, only nodes are created.
        # Next we will go back over the newly created cells and manually
        # create triangles.
        mesh = model.surface(divs[num], points = block)

        # For each new 4-node cell, create two triangles
        for cell in mesh.cells:
            nodes = mesh.cells[cell]
            model.element("tri31",   elem, (nodes[0], nodes[1], nodes[2]), 10, "PlaneStrain", 1)
            model.element("tri31", elem+1, (nodes[0], nodes[2], nodes[3]), 10, "PlaneStrain", 1)
            elem += 2

    return model
```
{{% /tab %}}
{{< /tabs >}}


{{< fold model.py >}}





# References

- Logan, D.L. (2012) A First Course in the Finite Element Method. 5th ed. Stamford, CT: Cengage Learning.

