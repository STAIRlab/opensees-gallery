---
title: Force-based Element vs. Displacement-based Element
description: "An investigation of various frame formulations"
thumbnail: img/ForceDispl.png
tags: ["Frame"]
draft: true
---

Investigate the two most commonly used OpenSees elements for modeling beam-column
elements: the force-based element (FBE) and displacement-based element (DBE). 


Although the OpenSees command for defining these two elements has the
same arguments, a beam-column element needs to be modeled differently
using these two elements to achieve a comparable level of accuracy. The
intent of this seminar is to show users how to properly model
beam-column elements with both FBE and DBE. The theory behind these two
elements along with two examples will be presented to users to enhance
their understanding of the elements and assure their correct
application. This seminar covers:

<ol>
<li>
<p><strong>Model Generation:</strong></p>
<ul>
<li>The column is modeled using finite elements, with either force-based or displacement-based elements.</li>
<li>The column height (<code>HCol</code>) is 96 inches, and the diameter (<code>DCol</code>) is 24 inches.</li>
<li>The clear cover of concrete (<code>clearCover</code>) is 0.75 inches.</li>
<li>The column is divided into finite elements, each with a height of <code>HEle</code>.</li>
<li>The area of the column cross-section (<code>ACol</code>) is calculated based on the diameter.</li>
</ul>
</li>
<li>
<p><strong>Boundary Conditions:</strong></p>
<ul>
<li>Node 1 is fixed in both horizontal and vertical directions.</li>
<li>Coordinate transformation is applied using the Corotational method.</li>
</ul>
</li>
<li>
<p><strong>Materials:</strong></p>
<ul>
<li>Longitudinal reinforcement:
<ul>
<li>Bar area (<code>barArea</code>) is 0.31 square inches (for bar #5).</li>
<li>Bar diameter (<code>db</code>) is 0.625 inches.</li>
<li>Yield strength (<code>fy</code>) of longitudinal bars is 70 ksi.</li>
<li>Modulus of elasticity (<code>Es</code>) of steel is 29,000 ksi.</li>
<li>Tangent at initial strain hardening (<code>Esf</code>) is calibrated from coupon tests.</li>
</ul>
</li>
<li>Transverse reinforcement:
<ul>
<li>Spiral diameter (<code>dh</code>) is 0.25 inches.</li>
<li>Number of hoops (<code>NoHoops</code>) is 1.</li>
<li>Area of transverse reinforcement bar (<code>Asp1</code>) is 0.0491 square inches.</li>
<li>Centerline distance between spirals (<code>stran</code>) is 1.25 inches.</li>
<li>Yield strength of the hoop (<code>fyh</code>) is 96.6 ksi.</li>
</ul>
</li>
</ul>
</li>
<li>
<p><strong>Steel Model:</strong></p>
<ul>
<li>The Menegotto-Pinto uniaxial steel model is used with specific coefficients.</li>
<li>MinMax limits are set for the steel model.</li>
</ul>
</li>
<li>
<p><strong>Concrete Model:</strong></p>
<ul>
<li>Unconfined concrete:
<ul>
<li>Compressive strength (<code>fc</code>) is 4.4 ksi.</li>
<li>Strain corresponding to <code>fc</code> is <code>eps0</code>.</li>
<li>Ultimate strain for unconfined concrete is <code>epss</code>.</li>
<li>Elastic modulus (<code>Ec</code>) is calculated based on ACI building code.</li>
</ul>
</li>
<li>Confined concrete:
<ul>
<li>Compressive strength and strain are determined using Mander’s equations.</li>
</ul>
</li>
</ul>
</li>
</ol>

<p><strong>PPT presentation of the seminar can be found
here:</strong></p>
<ul>
<li><a href="Media:_FBEvsDBE_final.pdf" title="wikilink">FBE vs.
DBE</a></li>
</ul>
<p><strong>Video of the seminar can be found here:</strong></p>
<ul>
<li><a href="http://www.youtube.com/watch?v=yk-1k2aF53E">FBE vs.
DBE</a></li>
</ul>
<p><strong>OpenSees files used to demonstrate the effect of rigid
constraints can be found here:</strong></p>
<ul>
<li>The main file that is to be sourced from the OpenSees interpreter:
<ul>
<li><a href="ConventionalColumn_Cyclic.tcl"
title="wikilink">ConventionalColumn_Cyclic.tcl</a></li>
</ul></li>
<li>Supporting files to be stored in the same folder with the main file:
<ul>
<li><a href="LibUnits.tcl" title="wikilink">LibUnits.tcl</a> (define
system of units)</li>
<li><a href="SingleCycle.tcl" title="wikilink">SingleCycle.tcl</a>
(procedure for writing one cycle of displacement history)</li>
<li><a href="Media:_leh415.xls" title="wikilink">leh415.xls</a>
(experimental force-displacement response)</li>
</ul></li>
</ul>
