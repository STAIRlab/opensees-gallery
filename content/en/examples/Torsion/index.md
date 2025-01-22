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

![alt text](image.png)

Here we consider the St. Venant's torsion problem. 

$$
\begin{aligned}
\operatorname{div} \bm{S} &= \bm{0} \\
\bm{S}\mathbf{n} &= \bm{0} \qquad\forall\quad \partial \Omega_{\xi} \\
\end{aligned}
$$

$$
\begin{array}{rll}
(\nabla \cdot \nabla) \varphi &=0 & \text { in } \Omega, \\
\nabla_{\mathbf{n}} \varphi  &=-\mathbf{i} \times \bm{\zeta} \cdot \mathbf{n} & \text { on } \partial \Omega
\end{array}
$$

For this problem, `ndm=2` and `ndf=1`.

{{< fold steel.py >}}

