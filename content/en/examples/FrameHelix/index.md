---
title: Helical Forms
description: A highly geometrically nonlinear problem is solved with the geometrically exact frame element formulation.
bibliography: references.json
render: spiral.glb
---

A cantilever beam is subjected to a *combined* point moment
$\boldsymbol{M}$ and a point force $F \, \mathbf{E}_3$ at its free end
$\xi=L$. 
This example is selected to demonstrate the ability of the
proposed formulations to naturally accommodate applied moments in
various reference frames. 
It also highlights the accuracy and
convergence characteristics of the formulations. 
Three common variations of this problem are considered with the following properties:

\[
\begin{array}{lcr}
    L  &=&    10\hphantom{..}    \\ % ,& A  &= 1 \\
    E  &=&    10^4  \\ % ,& I  &= 10^{-2} \\
    G  &=&    10^4  \\ % ,& J  &= 10^{-2} \\
\end{array}
\qquad\qquad
\begin{array}{lcr}
    A  &=& 1\hphantom{..} \\
    I  &=& 10^{-2} \\
    J  &=& 10^{-2} \\
\end{array}
\]

The [`ExactFrame`](https://opensees.stairlab.io/user/manual/model/elements/frame/ExactFrame.html) element formulation from OpenSees is employed.

### Simple Perturbation

Following <cite key="ibrahimbegović1995computational"></cite>, the problem of plane
flexure from Section [sec:circle](#sec:circle) is now altered by introducing the point load
$\boldsymbol{F} = 1/16 \, \mathbf{E}_3$ in addition to the moment
$\boldsymbol{M}$ so as to induce a three-dimensional response. A uniform
mesh of 10, 2-node elements is used, and the reference moment in
Equation ([eq:fref](#eq:fref)) for $\lambda = 1/8$ is applied in a single load
step. Because the deformation is no longer plane, each choice of nodal
parameterization essentially equilibriates the moment in a different
coordinate system. Results are reported in
Table [tab:helical-perturb01](#tab:helical-perturb01), where the `None/None/None` and
`Incr/None/Incr` variants match the values reported by
<cite key="ibrahimbegović1995computational"></cite> for the formulations by
<cite key="simo1986threedimensional"></cite> and <cite key="ibrahimbegović1995computational"></cite>,
respectively. 
Once again, the application of external isometry or
parameter transformations does not affect the convergence
characteristics of the solution.

### Consistent Perturbation

The problem is simulated again, but now the moment is consistently
applied with a spatial orientation. 
Formulations whose final residual
moment vector is conjugate to the spatial variations
$\boldsymbol{u}_{\scriptscriptstyle{\Lambda}}$ of the rotation
$\boldsymbol{\Lambda}$ do not need to be treated differently. 
This includes both elements with the `None` parameter transformation and
transformed elements with the Petrov-Galerkin formulation. For the
simulations with all other elements, a transformation of the nodal force
is necessary, as described in
<cite keys="ritto-corrêa2002differentiation ritto-corrêa2003workconjugacy"></cite>.
Table [tab:helical-perturb02](#tab:helical-perturb02) lists the tip displacements for the solution.

### Oscillating Spiral {#sec:helix}

To demonstrate the behavior of the proposed formulations under large
rotations, the reference moment value $M$ in
Equation ([eq:fref](#eq:fref)) is now increased to $\lambda=10$ with a large
out-of-plane force of $F=5 \lambda$. The model discretization uses 100
linear finite elements, and the loading is applied in `200` steps under
load factor control.
Figure [\[fig:helix\]](#fig:helix){reference-type="ref" reference="fig:helix"} shows the final deformed shape alongside a plot
of the tip displacement in the direction of the concentrated force.
These results are in agreement with the literature
<cite keys="zupan2003finiteelement, makinen2007total, ghosh2009frameinvariant, lolić2020consistent, harsch2023total"></cite>.
See also <cite key="zienkiewicz2014finite"></cite>

[^1]: These parameters were used by
    <cite keys="ritto-corrêa2002differentiation, ibrahimbegovic1997choice"></cite>.

    It is reported in <cite key="ibrahimbegović1995computational" ></cite> that an axial
    stiffness of $EA=2GA$ was used for simulation, but
    <cite key="ritto-corrêa2002differentiation"></cite> observe that this may be a
    reporting error. The authors believe that the simulations of
    <cite key="ibrahimbegović1995computational"></cite> have been performed with the
    parameters of the present study.

# References

<div id="bibliography-list"></div>

