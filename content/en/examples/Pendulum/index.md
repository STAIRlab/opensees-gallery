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

```{=tex}
\pagebreak
```

## (b) Lagrange equation in $\theta$

> (b) Apply Lagrange's equation in the basic form
> $$
\dot{p}_\theta-\frac{\partial T}{\partial \theta}=Q_\theta,
> $$
> and say what the generalized force $Q_\theta$ represents physically.

$$
\Lagrange[T]{\theta} = m \ddot{\theta} \ell^2 = Q_\theta
$$

This is a moment equation, enforcing balance of angular momentum.
In general, the simple pendulum is not considered to sustain
point couple forces so that $Q_\theta=0$ and conservation
of angular momentum follows consequentially.


```{=tex}
\pagebreak
```

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
L = T - V = \frac{1}{2}m \left[\dot{r}^2 + (\dot{\theta}r)^2\right]
+ \frac{G M m}{r}
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

```{=tex}
\pagebreak
```

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


```{=tex}
\pagebreak
```

# 1.4 Constraints (`Bead on expanding wire`)

> Suppose that a particle $P$ of mass $m$ is constrained to move on an expanding smooth circular wire lying on a horizontal plane:
> $$
\psi(x, y, t)=x^2+y^2-c^2 t^2=0 \quad(c=\text { const. })
> $$

## (a) System characterization

> (a) Identify the constraint type. How many degrees of freedom does $P$ have?

This is a holonomic, rheonomic constraint. The problem has $2-1=\boxed{1}$ degree of freedom.

## (b) Cartesian velocities

> (b) Using Cartesian coordinates, write the equations for the possible velocities, virtual velocities, and virtual displacements.

### Possible velocities

Differentiating the constraint equation yields

$$
\begin{aligned}
\dot{\psi} &= \nabla \psi \cdot \tilde{\boldsymbol{v}} \\
2 \ell \dot{\ell} &= 2x \dot{x} + 2y \dot{y} \\
\end{aligned}
$$

This can be written in terms of $\dot{x}$

$$
\begin{aligned}
\tilde{\boldsymbol{v}}\cdot \mathbf{e}_x &= \dot{x} \\
\tilde{\boldsymbol{v}}\cdot \mathbf{e}_y &= \frac{1}{y}(\ell \dot{\ell} - x \dot{x}) \\
&= \frac{1}{y}(c^2 t - x \dot{x})
\end{aligned}
$$

### Virtual velocities

Similarly, for the virtual velocities:

$$
\begin{aligned}
\delta \boldsymbol{v}\cdot \mathbf{e}_x &= \delta v_x \\
\delta \boldsymbol{v}\cdot \mathbf{e}_y &= \frac{-x}{y} \delta v_x \\
\end{aligned}
$$



### Virtual displacements

$$
\begin{aligned}
\delta \boldsymbol{r} &= \frac{d}{d\eta} \boldsymbol{r}(x+\delta x) \\
&= \delta x \mathbf{e}_x - \frac{x\delta x}{\sqrt{(ct)^2 x^2}}\mathbf{e}_y
\end{aligned}
$$

## (c) Polar velocities

> (c) Repeat Part (b) using polar coordinates.

### Possible velocities

The following possible velocities are parameterized by $\tilde{v}_\theta$:

$$
\tilde{\boldsymbol{v}} = c \mathbf{e}_{\text{r}} + \tilde{v}_\theta \mathbf{e}_\theta
$$

### Virtual velocities

$$
\delta \boldsymbol{v} =  \tilde{v}_\theta \mathbf{e}_\theta
$$

## (d) Constrained power

> (d) Calculate the power of the constraint force, and also its virtual power.

Constraint power expended:

$$
\begin{aligned}
\boldsymbol{F}^{(c)}&=\lambda \nabla \psi & \frac{\mathrm{F}}{\mathrm{L}}\times \mathrm{L} \\
&= \lambda r \, \mathbf{e}_{\text{r}} \\
&= \lambda ct \, \mathbf{e}_{\text{r}}
\end{aligned}
$$

$$
\begin{aligned}
\boldsymbol{F}^{(c)}\cdot \boldsymbol{v}  &= \lambda \ell  \, \dot{\ell}& \left[\frac{\mathrm{F}}{\mathrm{L}}\times \mathrm{L} \times \frac{\mathrm{L}}{\mathrm{T}}\right] \\
&= \lambda c^2 t\\
&= F^{(c)}_r c \\
\end{aligned}
$$

Constraint virtual power:
$$
\begin{aligned}
\boldsymbol{F}^{(c)}\cdot \delta\boldsymbol{v}  &= \lambda  \nabla \psi \cdot \delta \boldsymbol{v}  = 0\\
\end{aligned}
$$

## (e) Lagrange equation in $\theta$

> (e) Apply Lagrange's equation in the form
> $$
\frac{d}{d t}\left(\frac{\partial T}{\partial \dot{\theta}}\right)-\frac{\partial T}{\partial \theta}=Q_\theta .
> $$

$$
\begin{aligned}
Q_\theta &= \frac{d}{d t}\left(\frac{\partial T}{\partial \dot{\theta}}\right)-\frac{\partial T}{\partial \theta} \\
& =\frac{d}{d t}\left(m \ell^2 \dot{\theta}\right)-0 \\
& =\frac{d}{d t}\left(m (ct)^2 \dot{\theta}\right)=0
\end{aligned}
$$

## (f) Conservation interpretation

> (f) Interpret the resulting conservation equation.

The result of part (e) implies conservation of angular momentum is enforced.



{{< fold pendulum.py "analysis script" >}}

