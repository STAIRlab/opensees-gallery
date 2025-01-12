---
title: Simple Pendulum
thumbnail: img/pendulum.gif
description: This example investigates a simple pendulum using the corotational truss element.
render: pendulum.glb
---

This example investigates a simple pendulum using
the corotational truss element.


> For a simple pendulum of length $l$, take the angle $\theta$ as a generalized coordinate.

## (a) Generalized Momentum in $\theta$

> (a) What does the generalized momentum
> $$
  p_\theta=\frac{\partial T}{\partial \dot{\theta}}
> $$
> represent physically in this problem?

The velocity is
$$
\boldsymbol{v} = \dot{\theta} \ell \boldsymbol{e}_\theta
$$

and the kinetic energy follows:

$$
T = \frac{1}{2} m \boldsymbol{v} \cdot \boldsymbol{v} = \frac{1}{2} m \dot{\theta}^2 \ell^2
$$

This furnishes a generalized momentum:

$$
p_\theta=\frac{\partial T}{\partial \dot{\theta}} = m \dot{\theta} \ell^2
$$

This can be understood as an **angular momentum** (quantity with the form
$\boldsymbol{r}\times m \boldsymbol{v}$) where, by abusing the symbol $\times$:

$$
p_\theta = \ell \times m (\dot{\theta} \ell)
$$


## (b) Lagrange equation in $\theta$

> (b) Apply Lagrange's equation in the basic form
> $$
  \dot{p}_\theta-\frac{\partial T}{\partial \theta}=Q_\theta,
> $$
> and say what the generalized force $Q_\theta$ represents physically.

$$
%\Lagrange[T]{\theta} = m \ddot{\theta} \ell^2 = Q_\theta
$$

This is a moment equation, enforcing balance of angular momentum.
In general, the simple pendulum is not considered to sustain
point couple forces so that $Q_\theta=0$ and conservation
of angular momentum follows consequentially.



# 1.3 Gravitational Potentials

> 3. Consider a satellite of mass $m \mathrm{~kg}$ orbiting the earth. The motion is planar and the gravitational potential energy is
>
> $$
  V=-\frac{G M m}{r} \quad \mathrm{~J} .
> $$

## (a) Lagrange equations

> (a) Use Lagrange's equations in the form
> $$
  \frac{d}{d t}\left(\frac{\partial L}{\partial \dot{r}}\right)-\frac{\partial L}{\partial r}=0, \quad \frac{d}{d t}\left(\frac{\partial L}{\partial \dot{\theta}}\right)-\frac{\partial L}{\partial \theta}=0
> $$
> to obtain the equations of motion.

In polar coordinates one has:

$$
T = \frac{1}{2}m \left[\dot{r}^2 + (\dot{\theta}r)^2\right]
$$

The Lagrangian is:

$$
L = T - V = \frac{1}{2}m \left[\dot{r}^2 + (\dot{\theta}r)^2\right] + \frac{G M m}{r}
$$

Forming Lagrange's equations of $r$ yields:

$$
\begin{aligned}
0&=\frac{d}{d t}\left(\frac{\partial L}{\partial \dot{r}}\right)-\frac{\partial L}{\partial r} \\
 &= \frac{d}{dt}\left(m \dot{r}\right) - \left(m \dot{\theta}^2 r - GMm r^{-2}\right) \\
m \ddot{r} &= m \dot{\theta}^2 r - GMm r^{-2}
\end{aligned}
$$

Similarly, in $\theta$: 

$$
\frac{d}{dt}\left(mr^2\dot{\theta}\right) = 0 = m 2r \dot{r} \dot{\theta} + mr^2 \ddot{\theta}
$$


## (b) Momentum conservation

> (b) Show that the angular momentum is conserved.

The Lagrange equation for $\theta$ is

$$
\frac{d}{dt}\left(mr^2\dot{\theta}\right) = 0
$$

This implies that angular momentum must be a constant over time, and is therefore conserved.

## (c) Governing equation in $r$

> (c) Obtain the differential equation for the variable $r$.

<!-- 
From Lagrange's equation of $r$

$$
\ddot{r} + GM r^{-2} = \dot{\theta}^2 r \qquad \dot{\theta} = \sqrt{\frac{\ddot{r}}{r} + \frac{GM}{r^3}}
$$

$$
\begin{aligned}
0 &= m\frac{d}{dt}\left(r^2 \dot{\theta}\right) \\
&= m \, \frac{d}{dt} \sqrt{\ddot{r} + \frac{GM}{r^2}}
\end{aligned}
$$
-->

Manipulating the angular momentum, $p_\theta$ as follows

$$
\begin{aligned}
\frac{p_\theta^2}{m r^3}  = mr\dot{\theta}^2\\
\end{aligned}
$$

allows Lagrange's equation of $r$ to be written:

$$
\begin{aligned}
m \ddot{r} - m \dot{\theta}^2 r + \frac{GMm}{r^2} = 0 \\
\boxed{\ddot{r} - \frac{p_\theta^2}{m^2 r^3} + \frac{GM}{r^2} = 0}
\end{aligned}
$$


{{< fold pendulum.py "analysis script" >}}

