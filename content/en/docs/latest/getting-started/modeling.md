---
title: Modeling
aliases:
  - "/docs/modeling/"
  - "/modeling/"
layout: docs
---

## Modeling in Python

The best practice for modeling in Python is to create a model class
by calling the `opensees.openseespy.Model(...)` constructor (note the capital "M").
All standard OpenSees functions, as documented [here](https://opensees.github.io/OpenSeesDocumentation)
can be called as methods on the object that is retured. For example:
```python
import opensees.openseespy as ops
model = ops.Model(ndm=2, ndf=3)
model.node(1, 2.0, 3.0)
```

## Evaluate Tcl models from Python

The first scripting interface to OpenSees used a programming language
called Tcl, which continues to be supported. 
To execute Tcl commands from a Python script, just create an instance
of the `opensees.openseespy.Model` class and call its `eval()` method:
```python
import opensees.openseespy as ops
model = ops.Model()
model.eval("model Basic -ndm 2")
model.eval("print -json")
```
Full Tcl files can be conveniently executed in this way. For example,
if a Tcl file called `model.tcl` exists in the current working directory:
```python
import opensees.openseespy as ops
model = ops.Model()
with open("model.tcl", "r") as f:
    model.eval(f.read())
```
