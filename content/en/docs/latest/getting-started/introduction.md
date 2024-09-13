---
title: Introduction
description: Get started with OpenSees.
date: 2024-08-14
aliases:
  - "/docs/getting-started/"
  - "/getting-started/"
  - "/docs/"
layout: docs
---

`opensees` is a Python package that provides an intuitive API for nonlinear
finite element analysis, implemented in C++ through the OpenSees framework. 
OpenSees features state-of-the-art finite element formulations and solution 
algorithms, including mixed formulations for beams and solids, over 200 material models, and an
extensive collection of continuation algorithms to solve highly nonlinear
problems.

## Installation

In order to install `opensees` just run the command:

{{< command >}}
python -m pip install opensees
{{< /command >}}

## Running OpenSees

The `opensees` package can be used in three ways:

{{< accordion class="accordion-theme accordion-flush" >}}
  {{< accordion-item header="Python Module" >}}
    The `opensees.openseespy` Python module implements the API that has been developed by Oregon State.
  {{< /accordion-item >}}
  {{< accordion-item header="Command line interface" >}}
    An interactive Tcl interpreter can be started by invoking the module as follows from the command line:
    {{< command >}}
    python -m opensees --help
    {{< /command >}}
  {{< /accordion-item >}}
  {{< accordion-item header="Interactive Interpreter" >}}
    An interactive Tcl interpreter can be started by invoking the module as follows from the command line:
    {{< command >}}
    python -m opensees
    {{< /command >}}

  {{< /accordion-item >}}
{{< /accordion >}}


