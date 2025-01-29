---
title: Plane Tapered Cantilever
thumbnail: img/examples/plane_taper.png
tags: ["CE222"]
description: A finite element analysis is performed of a plane tapered cantilever using constant-strain triangles.
render: model.glb
downloads:
  Python: ["plane_taper.py"]
---

A finite element analysis is performed of a plane tapered cantilever using constant-strain triangles. 
The [ElasticIsotropic](https://opensees.stairlab.io/user/manual/material/ndMaterials/ElasticIsotropic.html) material model is employed.
Visualization is performed in the script [`render.py`](render.py) using the [`veux`](https://pypi.org/project/veux) library.

{{< fold plane_taper.py "analysis script" >}}


The stress field looks like:

{{< render stress.glb >}}

