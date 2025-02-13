---
title: Truss Domes
description: Several periodic truss domes are generated using OpenSeesRT.
thumbnail: img/examples/dome1180.png
bibliography: references.json
draft: false
---

A variety of periodic truss structures are investigated. This class of
models was investigated by <cite key="kaveh2010optimum"></cite>.
All figures have been produced with [`veux`](https://veux.io).

{{< nav type="tabs" id="tabs-1" >}}
  {{< nav-item header="120" show="true" >}}
   ![3D rendering of the 120-bar truss model.](dome120.png)
   This model is investigated by <cite keys="kaveh2010optimum, lieu2018adaptive"></cite>.

   ```python
   model = create_dome("120")
   ```

  {{< /nav-item >}}
  {{< nav-item header="600" >}}

   ![3D rendering of the 600-bar truss model.](dome600.png)
   This model is investigated by <cite key="kaveh2022optimal"></cite>

  {{< /nav-item >}}
  {{< nav-item header="1410">}}
  This model is investigated by <cite key="kaveh2010optimum"></cite>
  {{< /nav-item >}}
  {{< nav-item header="1180">}}
![3D rendering of the 1180-bar truss model.](dome1180.png)

This model is investigated by <cite key="kaveh2022optimal"></cite>
  {{< /nav-item >}}

{{< /nav >}}

The following code block contains the source code used to generate these
models. In particular, the function `revolve()` takes a representative segment
and generates a full model by revolving the nodes and elements.

{{< fold revolve.py >}}

# References

<div id="bibliography-list"></div>

