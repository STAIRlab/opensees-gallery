---
title: Curved Cantilever Beam Under Point Force
draft: true
---

## Curved Cantilever Beam

The curved cantilever in Figure [1](#fig:bathe){reference-type="ref"
reference="fig:bathe"} was first studied by [@bathe1979large], and has
become a staple in the literature on geometrically nonlinear rods. This
example is selected to demonstrate the path-independence of the `Init`
interpolation. The undeformed centerline of the cantilever follows a
$45^\circ$ arc with radius $R$ given by:
$$\boldsymbol{x}_0(\xi) = R \sin \xi \frac{\pi}{4L}\, \mathbf{E}_1 
                      + R \left(1 - \cos \xi \frac{\pi}{4L}\right)\, \mathbf{E}_3.$$
A point load $\boldsymbol{F} = 600 \, \mathbf{E}_2$ is applied at the
tip, i.e. at $\xi = R$. There is no closed-form solution to the problem,
and it is customary to present the final displacements at the tip:
$$\Delta x_i \triangleq \mathbf{E}_i \cdot \left(\boldsymbol{x}(L) - \boldsymbol{x}_0(L)\right).$$
The following parameters are used for the simulations:
$$\begin{array}{lr}
% Hockling
    R  =& 100 \\ %   ,& A  &= 10 \\
    E  =& 1000 \\ %   ,& I  &= 0.0833 \\
    G  =& 500 \\ %   ,& J  &= 2.16 \\
\end{array}
\qquad\qquad
\begin{array}{ll}
% Hockling
    A  =& 10^4    \\
    I  =& 10^4/12 \\
    J  =& 10^4/6  \\
\end{array}$$ The analysis uses a discretization with 8 linear (2-node)
elements. The analysis is performed twice for each formulation under
consideration, first with 8 equal load increments and then with 10. The
results are presented in
Table [\[tab:bathe\]](#tab:bathe){reference-type="ref"
reference="tab:bathe"}. Only the formulations with the `Init`
interpolation produce the same tip displacement in both load cases,
indicating an artificial path dependence for all other variants.

![Deformed shape of curved cantilever by
[@bathe1979large].](Figures/Figure_3){#fig:bathe width="60%"}

