---
title: Modeling
aliases:
  - "/docs/modeling/"
  - "/modeling/"
layout: docs
---

To run multiple models simultaneously, use `openseespy.Model(...)` (capital M)
instead of the regular `openseespy.model(...)` (lowercase m) function, and invoke
all subsequent modeling functions (e.g. `node(...)`, `element(...)`, `fix(...)`, etc)
as methods on the object returned from `Model()` instead of the `openseespy` submodule
directly. For example, instead of:

```python
import opensees.openseespy as ops
ops.model("basic", "-ndm", 2, "-ndf", 3)
ops.node(1, 2.0, 3.0)
``` 
do
```python
import opensees.openseespy as ops
model = ops.Model(ndm=2, ndf=3)
model.node(1, 2.0, 3.0)
```


