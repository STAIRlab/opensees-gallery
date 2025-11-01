---
title:  Cable Stayed
tags: ["Python", "Tcl"]
description: Model of a cable-stayed bridge imported from CSiBridge
thumbnail: img/examples/CableStayed02.png
render: model.glb
weight: 1000
draft: true
---

The example is composed of the following files:
- [`CableStayed.b2k`](CableStayed.b2k) is a CSiBridge input file defining a cable stayed bridge.
- [`analyze.py`](analyze.py) performs  an analysis using [`xara`](https://pypi.org/project/opensees) and the [xcsi](https://pypi.org/project/xcsi) library.
- [`render.py`](render.py) generates a rendering with the [`veux`](https://pypi.org/project/veux) library.


