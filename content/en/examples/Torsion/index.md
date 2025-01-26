---
title: Torsion
render: girder.glb
#thumbnail: img/examples/Torsion.png
thumbnail: img/examples/torsion_girder.png
description: The Laplace problem is solved for St. Venant's warping function.
tags: ["CE222", "Section"]
draft: false
---

<!--
![Cross section of a bridge girder deformed by St. Venant warping.](img/girder.png)
-->

Here we consider the St. Venant's torsion problem. Beginning from the three-dimensional boundary value problem of solid mechanics:

$$
\begin{aligned}
\operatorname{div} \bm{S} &= \bm{0} \\
\bm{S}\mathbf{n} &= \bm{0} \qquad\forall\quad \partial \Omega_{\xi} \\
\end{aligned}
$$

one arrives at a pure Neumann problem of the Laplace operator:

$$
\begin{array}{rll}
\Delta \varphi &=0 & \text { in } \Omega, \\
\nabla_{\mathbf{n}} \varphi  &=-\mathbf{i} \times \bm{\zeta} \cdot \mathbf{n} & \text { on } \partial \Omega
\end{array}
$$
for a given point of rotation $\bm{\zeta}$.

For this problem, `ndm=2` and `ndf=1`. Rendering is performed with the [`veux`](https://veux.stairlab.io) library.

{{< fold steel.py >}}

