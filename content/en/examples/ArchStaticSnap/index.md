---
title: Arch Instability
tags: ["Python", "Static", "CE221"]
thumbnail: img/examples/ClarkeHancock.png
keywords: ["snap through", "instability", "buckling", "nonlinear geometry", "incremental", "arc length"]
weight: 40
render: solution.glb
description: >-
 Several nonlinear static analysis methods are used to investigate
 instabilities in a shallow arch.
downloads:
  Python: ["arch3D.py", "requirements.txt"]
  Exercise: ["Exercise.ipynb", "requirements.txt"]
---


![Shallow arch](img/ClarkeHancock.png)

{{< ipynb "IncrementalAnalysis.ipynb" >}}

The source code for creating the arch structure is given below:

{{< fold arch.py >}}

