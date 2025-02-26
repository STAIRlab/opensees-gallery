---
title: "013 - Asymmetric Section: Post-buckling"
draft: false
description: Post-buckling curve with an asymmetric cross section
bibliography: references.json
downloads:
  Python: ["e0013.py"]
---

A transverse load induces twisting of a cantilever with an asymmetric channel section.
This example demonstrates the behavior of asymmetric sections.
In particular, we investigate the effects that arise when the
reference point is taken somewhere other than the shear center.

Cantilever channel. uniform torsion. 
Elastic by <cite keys="gruttmann1998geometrical,battini2002corotational"></cite>
plastic by <cite keys="gruttmann2000theory,battini2002plastic"></cite> .

$$
T = -GA s_z \gamma_y + GAs_y \gamma_z
$$

- J. Chróścielewski; J. Makowski; H. Stumpf. (1992). Genuinely resultant shell finite elements accounting for geometric and material non-linearity. , 35(1), 63–94. doi:10.1002/nme.1620350105 
- P. Betsch; F. Gruttmann; E. Stein. (1996). A 4-node finite shell element for the implementation of general hyperelastic 3D-elasticity at finite strains. , 130(1-2), 57–79. doi:10.1016/0045-7825(95)00920-5 

Beams:
- Hsiao KM, Lin W Y (2000) A co-rotational formulation for thin-walled beams with monosymmetric open section. DOI: 10.1016/S0045-7825(99)00471-5
- D Manta, R Goncalves (2016) A geometrically exact Kirchhoff beam model including torsion warping.


# References

<div id="bibliography-list"></div>

