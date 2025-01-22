---
title: Arch Instability
tags: ["Python", "Static", "CE221"]
thumbnail: img/examples/ClarkeHancock.png
keywords: ["snap through", "instability", "buckling", "nonlinear geometry", "incremental", "arc length"]
render: solution.glb
description: >-
 Several nonlinear static analysis methods are used to investigate
 instabilities in a shallow arch.
---


![Shallow arch](img/ClarkeHancock.png)

The files for this example are:
- [`arch.py`](./arch.py) - This file contains the function `arch_model` which is used construct the model
- [`IncrementalAnalysis.ipynb`](IncrementalAnalysis.ipynb) - This is the current Jupyter notebook file

{{< fold arch.py >}}

{{% ipynb "IncrementalAnalysis.ipynb" %}}
