---
title: "Nonlinear Geometry"
tags: ["Python", "Tcl", "Frame"]
render: ./model.glb
---


Corotational frame elements are used to approximate Euler's buckling load,
which is given by:
\[
P_{\mathrm{euler}} = \frac{\pi^2 EI}{L^2}
\]

This example is adapted from https://github.com/denavit/OpenSees-Examples .
The files for the problem are [`buckling.py`](buckling.py) for
Python, and [`buckling.tcl`](buckling.tcl) for Tcl.


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
