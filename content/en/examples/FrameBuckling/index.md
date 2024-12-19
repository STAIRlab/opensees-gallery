---
title: "Linearized Buckling"
tags: ["Python", "Tcl", "Frame"]
render: ./model.glb
description: Corotational frame elements are used to approximate Euler's buckling load.
---


## Problem

Corotational frame elements are used to approximate Euler's buckling load
which is given by:
$$
P_{\mathrm{euler}} = \frac{\pi^2 EI}{L^2}
$$
This example is adapted from https://github.com/denavit/OpenSees-Examples .
The files for the problem are [`buckling.py`](buckling.py) for
Python, and [`buckling.tcl`](buckling.tcl) for Tcl.

## Theory

### Buckling Analysis

Loosely speaking, buckling happens when there are multiple shapes that a structure can deform into that will be in equilibrium with it's applied loads. This implies that at the point of buckling, there are multiple independent displacement increments $\bm{u}$ which will be mapped to the same resisting load by the tangent $\bm{K}$. In otherwords, The buckling load is the point at which $\bm{K}$ becomes singular. If we consider $\bm{K}$ as a function of the load factor $\bm{\lambda}$, this condition can be expressed as the nonlinear root-finding problem:
$$
\operatorname{det}\bm{K}(\lambda) = 0
$$
For many classical models, the dependence of $\bm{K}$ on $\lambda$ is linear, and in this case the problem is equivalent to a generalized eigenvalue problem which is computationally much more tractable. However, even if $\bm{K}$ is nonlinear in $\lambda$, one may still investigate the *linearized buckling problem*, where an eigenvalue problem is obtained by learizing $\bm{K}(\lambda)$:
$$
\bm{K}(\lambda) \approx \bm{K}(0) + \bm{K}^{\prime}(0) \lambda
$$
where $\bm{K}^{\prime}$ is the derivative of $\bm{K}$ with respect to $\lambda$.


#### Timoshenko Column Buckling
$$
\begin{gathered}
\lambda=\sqrt{\frac{P L^2}{E I\left[1-P /\left(k_{\mathrm{s}} G A\right)\right]}}=\sqrt{\frac{P L^2}{\chi E I}} \\
\chi=1-P /\left(k_{\mathrm{s}} G A\right) \\
P=\chi \lambda^2 E I / L^2 .
\end{gathered}
$$

$$
\begin{gathered}
\chi=\frac{1}{1+\lambda^2 E I /\left(k_{\mathrm{s}} G A L^2\right)}=\frac{1}{1+\lambda^2 \varphi / 12} \\
P=\frac{\lambda^2 E I / L^2}{1+\lambda^2 \varphi / 12} .
\end{gathered}
$$

$$
\tan \lambda_{\text {cr }}=\chi \lambda_{\text {cr }}=\frac{\lambda_{\text {cr }}}{1+\lambda_{\text {cr }} 2 \varphi / 12}
$$
