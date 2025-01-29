---
title: "Ex4 - Portal Frame"
thumbnail: img/ExampleFigure_FiberSection.GIF
draft: true
---

## Introduction

To all the demonstrations that Example 3 has done, Example 4 adds the use of previously-defined Tcl procedures (a procedure is a Tcl command that is created by the proc command) or scripts.
This example also introduces new kinds of static and dynamic analyses.

<h2><span class="mw-headline" id="Input">Input</span></h2>
<h3><span class="mw-headline" id="Model_Building">Model Building</span></h3>
<p>The following tasks are performed when building the model
</p>
<blockquote>
<ul><li>define units</li>
<li>define model</li>
<li>define recorders for output</li>
<li>define &amp; apply gravity</li></ul>
</blockquote>
<table style="margin:0; background:none;">
<tbody><tr>
<td style="margin:0; width:25%; border:3px solid #ccc; background:#white; vertical-align:top;">
<h4><span class="mw-headline" id="Elastic_Element">Elastic Element</span></h4><hr /><table style="width:100%; vertical-align:top;background:#white;">


<tbody><tr>
<td style="color:#000;"><div>
<p><a href="/wiki/index.php/OpenSees_Example_4._Portal_Frame" title="OpenSees Example 4. Portal Frame">
<img alt="ExampleFigure ElasticSection.GIF" src="ExampleFigure_ElasticSection.GIF" width="270" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex4.Portal2D.build.ElasticElement.tcl" class="internal" title="Ex4.Portal2D.build.ElasticElement.tcl">Ex4.Portal2D.build.ElasticElement.tcl</a></li>
<li><a href="LibUnits.tcl" class="internal" title="LibUnits.tcl">LibUnits.tcl</a></li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>Effective axial and flexural stiffnesses are defined at the element level</li>
<li>elasticBeamColumn elements</li></ul>
</div>
</td></tr></tbody></table>
</td>
<td style="margin:0; width:25%; border:3px solid #ccc; background:#white; vertical-align:top;">
<h4><span id="Distributed_Plasticity_Element,_Uniaxial_Section"></span><span class="mw-headline" id="Distributed_Plasticity_Element.2C_Uniaxial_Section">Distributed Plasticity Element, Uniaxial Section</span></h4><hr /><table style="width:100%; vertical-align:top;background:#white;">


<tbody><tr>
<td style="color:#000;"><div>
<p><a href="/wiki/index.php/OpenSees_Example_4._Portal_Frame" title="OpenSees Example 4. Portal Frame"><img alt="ExampleFigure uniaxialSection.GIF" src="ExampleFigure_uniaxialSection.GIF" width="267" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex4.Portal2D.build.InelasticSection.tcl" class="internal" title="Ex4.Portal2D.build.InelasticSection.tcl">Ex4.Portal2D.build.InelasticSection.tcl</a></li>
<li><a href="LibUnits.tcl" class="internal" title="LibUnits.tcl">LibUnits.tcl</a></li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>Axial and flexural stiffnesses/strength are defined independently at the section level</li>
<li>uniaxial inelastic section (moment-curvature)</li>
<li>nonlinear beam-column elements</li></ul>
</div>
</td></tr></tbody></table>
</td>
<td style="margin:0; width:25%; border:3px solid #ccc; background:#white; vertical-align:top;">
<h4><span id="Distributed_Plasticity_Element,_Fiber_Section"></span><span class="mw-headline" id="Distributed_Plasticity_Element.2C_Fiber_Section">Distributed Plasticity Element, Fiber Section</span></h4><hr /><table style="width:100%; vertical-align:top;background:#white;">


<tbody><tr>
<td style="color:#000;"><div>
<p><a href="/wiki/index.php/OpenSees_Example_4._Portal_Frame" title="OpenSees Example 4. Portal Frame"><img alt="ExampleFigure FiberSection.GIF" src="ExampleFigure_FiberSection.GIF" width="299" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex4.Portal2D.build.InelasticFiberSection.tcl" class="internal" title="Ex4.Portal2D.build.InelasticFiberSection.tcl">Ex4.Portal2D.build.InelasticFiberSection.tcl</a></li>
<li><a href="LibUnits.tcl" class="internal" title="LibUnits.tcl">LibUnits.tcl</a></li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>The section is broken down into fibers where uniaxial materials are defined independently.</li>
<li>The program calculates flexural and axial stiffnesses/strength by integrating strains across the section.</li>
<li>fiber section</li>
<li>nonlinear beam-column elements</li></ul>
</div>
</td></tr></tbody></table>
</td></tr></tbody></table>
<p><br />
</p>
<h3><span class="mw-headline" id="Lateral-Load_Analysis">Lateral-Load Analysis</span></h3>
<p>The following tasks are performed in the analysis
</p>
<blockquote>
<ul><li>define lateral-load parameters</li>
<li>analyze</li></ul>
</blockquote>
<table style="margin:0; background:none;">
<tbody><tr>
<td style="margin:0; width:25%; border:3px solid #ccc; background:#white; vertical-align:top;">
<h4><span class="mw-headline" id="Static">Static</span></h4>
<table style="width:100%; border:1px solid #ddcef2; vertical-align:top;background:#white;">

<tbody><tr>
<td style="color:#000;"><div>
<h5><span class="mw-headline" id="Static_Pushover">Static Pushover</span></h5>
<p><a href="/wiki/index.php/OpenSees_Example_4._Portal_Frame" title="OpenSees Example 4. Portal Frame"><img alt="Example4 Push.GIF" src="Example4_Push.GIF" width="352" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex4.Portal2D.analyze.Static.Push.tcl" class="internal" title="Ex4.Portal2D.analyze.Static.Push.tcl">Ex4.Portal2D.analyze.Static.Push.tcl</a></li>
<li><a href="LibAnalysisStaticParameters.tcl" class="internal" title="LibAnalysisStaticParameters.tcl">LibAnalysisStaticParameters.tcl</a></li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>One-directional monotonic displacement-controlled static loading</li></ul>
</div>
</td></tr></tbody></table>
<hr />
<table style="width:100%; border:1px solid #ddcef2; vertical-align:top;background:#white;">

<tbody><tr>
<td style="color:#000;"><div>
<h5><span class="mw-headline" id="Static_Reversed_Cyclic">Static Reversed Cyclic</span></h5>
<p><a href="/wiki/index.php/OpenSees_Example_4._Portal_Frame" title="OpenSees Example 4. Portal Frame"><img alt="Example4 Cyclic.GIF" src="Example4_Cyclic.GIF" width="360" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex4.Portal2D.analyze.Static.Cycle.tcl" class="internal" title="Ex4.Portal2D.analyze.Static.Cycle.tcl">Ex4.Portal2D.analyze.Static.Cycle.tcl</a></li>
<li><a href="LibAnalysisStaticParameters.tcl" class="internal" title="LibAnalysisStaticParameters.tcl">LibAnalysisStaticParameters.tcl</a></li>
<li><a href="LibGeneratePeaks.tcl" class="internal" title="LibGeneratePeaks.tcl">LibGeneratePeaks.tcl</a></li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>One-directional displacement-controlled static loading</li>
<li>Displacement cycles are imposed in positive and negative direction</li></ul>
</div>
</td></tr></tbody></table>
</td>
<td style="margin:0; width:25%; border:3px solid #ccc; background:#white; vertical-align:top;">
<h4><span class="mw-headline" id="Dynamic_EQ_Ground_Motion">Dynamic EQ Ground Motion</span></h4>
<table style="width:100%; border:1px solid #ddcef2; vertical-align:top;background:#white;">

<tbody><tr>
<td style="color:#000;"><div>
<h5><span class="mw-headline" id="Dynamic_Uniform_Sine-Wave_Ground_Motion">Dynamic Uniform Sine-Wave Ground Motion</span></h5>
<p><a href="/wiki/index.php/OpenSees_Example_4._Portal_Frame" title="OpenSees Example 4. Portal Frame"><img alt="Example4 UniformSine.GIF" src="Example4_UniformSine.GIF" width="294" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex4.Portal2D.analyze.Dynamic.sine.Uniform.tcl" class="internal" title="Ex4.Portal2D.analyze.Dynamic.sine.Uniform.tcl">Ex4.Portal2D.analyze.Dynamic.sine.Uniform.tcl</a></li>
<li><a href="LibAnalysisDynamicParameters.tcl" class="internal" title="LibAnalysisDynamicParameters.tcl">LibAnalysisDynamicParameters.tcl</a></li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>Sine-wave acceleration input</li>
<li>Same acceleration input at all nodes restrained in specified direction</li></ul>
</div>
</td></tr></tbody></table>
<hr />
<table style="width:100%; border:1px solid #ddcef2; vertical-align:top;background:#white;">

<tbody><tr>
<td style="color:#000;"><div>
<h5><span id="Dynamic_Uniform_Earthquake_Ground_Motion_(typical)"></span><span class="mw-headline" id="Dynamic_Uniform_Earthquake_Ground_Motion_.28typical.29">Dynamic Uniform Earthquake Ground Motion (typical)</span></h5>
<p><a href="/wiki/index.php/OpenSees_Example_4._Portal_Frame" title="OpenSees Example 4. Portal Frame"><img alt="Example4 UniformEQ.GIF" src="Example4_UniformEQ.GIF" width="289" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex4.Portal2D.analyze.Dynamic.EQ.Uniform.tcl" class="internal" title="Ex4.Portal2D.analyze.Dynamic.EQ.Uniform.tcl">Ex4.Portal2D.analyze.Dynamic.EQ.Uniform.tcl</a></li>
<li><a href="LibAnalysisDynamicParameters.tcl" class="internal" title="LibAnalysisDynamicParameters.tcl">LibAnalysisDynamicParameters.tcl</a></li>
<li><a href="ReadSMDFile.tcl" class="internal" title="ReadSMDFile.tcl">ReadSMDFile.tcl</a></li>
<li><a href="H-E12140.zip" class="internal" title="H-E12140.zip">H-E12140.AT2</a></li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>Earthquake (from file) acceleration input</li>
<li>Same acceleration input at all nodes restrained in specified direction</li></ul>
</div>
</td></tr></tbody></table>
<hr />
<table style="width:100%; border:1px solid #ddcef2; vertical-align:top;background:#white;">

<tbody><tr>
<td style="color:#000;"><div>
<h5><span class="mw-headline" id="Dynamic_Multiple-Support_Sine-Wave_Ground_Motion">Dynamic Multiple-Support Sine-Wave Ground Motion</span></h5>
<p><a href="/wiki/index.php/OpenSees_Example_4._Portal_Frame" title="OpenSees Example 4. Portal Frame"><img alt="Example4 MultiSupportSine.GIF" src="Example4_MultiSupportSine.GIF" width="329" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex4.Portal2D.analyze.Dynamic.sine.multipleSupport.tcl" class="internal" title="Ex4.Portal2D.analyze.Dynamic.sine.multipleSupport.tcl">Ex4.Portal2D.analyze.Dynamic.sine.multipleSupport.tcl</a> (this file may need to be corrected for displacement input)</li>
<li><a href="LibAnalysisDynamicParameters.tcl" class="internal" title="LibAnalysisDynamicParameters.tcl">LibAnalysisDynamicParameters.tcl</a></li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>Sine-wave displacement input</li>
<li>Different displacements are specified at particular nodes in specified directions</li></ul>
</div>
</td></tr></tbody></table>
<hr />
<table style="width:100%; border:1px solid #ddcef2; vertical-align:top;background:#white;">

<tbody><tr>
<td style="color:#000;"><div>
<h5><span class="mw-headline" id="Dynamic_Multiple-Support_Earthquake_Ground_Motion">Dynamic Multiple-Support Earthquake Ground Motion</span></h5>
<p><a href="/wiki/index.php/OpenSees_Example_4._Portal_Frame" title="OpenSees Example 4. Portal Frame"><img alt="Example4 MultiSupportEQ.GIF" src="Example4_MultiSupportEQ.GIF" width="342" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex4.Portal2D.analyze.Dynamic.EQ.multipleSupport.tcl" class="internal" title="Ex4.Portal2D.analyze.Dynamic.EQ.multipleSupport.tcl">Ex4.Portal2D.analyze.Dynamic.EQ.multipleSupport.tcl</a> (this file needs to be corrected for displacement input)</li>
<li><a href="LibAnalysisDynamicParameters.tcl" class="internal" title="LibAnalysisDynamicParameters.tcl">LibAnalysisDynamicParameters.tcl</a></li>
<li><a href="ReadSMDFile.tcl" class="internal" title="ReadSMDFile.tcl">ReadSMDFile.tcl</a></li>
<li><a href="H-E12140D.zip" class="internal" title="H-E12140D.zip">H-E12140.DT2</a> (Displacement recording)</li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>Earthquake (from file) displacement input</li>
<li>Different displacements are specified at particular nodes in specified directions</li></ul>
</div>
</td></tr></tbody></table>
<hr />
<table style="width:100%; border:1px solid #ddcef2; vertical-align:top;background:#white;">

<tbody><tr>
<td style="color:#000;"><div>
<h5><span id="Dynamic_Bidirectional_Earthquake_Ground_Motion_(typical)"></span><span class="mw-headline" id="Dynamic_Bidirectional_Earthquake_Ground_Motion_.28typical.29">Dynamic Bidirectional Earthquake Ground Motion (typical)</span></h5>
<p><a href="/wiki/index.php/OpenSees_Example_4._Portal_Frame" title="OpenSees Example 4. Portal Frame"><img alt="Example4 BidirectEQ.GIF" src="Example4_BidirectEQ.GIF" width="289" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex4.Portal2D.analyze.Dynamic.EQ.bidirect.tcl" class="internal" title="Ex4.Portal2D.analyze.Dynamic.EQ.bidirect.tcl">Ex4.Portal2D.analyze.Dynamic.EQ.bidirect.tcl</a></li>
<li><a href="LibAnalysisDynamicParameters.tcl" class="internal" title="LibAnalysisDynamicParameters.tcl">LibAnalysisDynamicParameters.tcl</a></li>
<li><a href="ReadSMDFile.tcl" class="internal" title="ReadSMDFile.tcl">ReadSMDFile.tcl</a> (need to modify ReadSMDFile.tcl for displacement data)</li>
<li><a href="H-E12140.zip" class="internal" title="H-E12140.zip">H-E12140.AT2</a></li>
<li><a href="H-E01140.zip" class="internal" title="H-E01140.zip">H-E01140.AT2</a> (acceleration recording in perpendicular direction)</li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>Earthquake (from file) acceleration input</li>
<li>Different ground motion in two directions</li>
<li>Same acceleration input at all nodes restrained in specified direction</li></ul>
</div>
</td></tr></tbody></table>
</td></tr></tbody></table>
<h2><span class="mw-headline" id="Run">Run</span></h2>
<p>The model and analysis combinations for this example are numerous. The following are an small subset, for demonstration purposes:
</p>
<ul><li>To run Elastic Mode, Static Pushover Analysis:</li></ul>
<blockquote><div class="mw-highlight mw-content-ltr" dir="ltr"><pre><span></span><span class="nb">puts</span> <span class="s2">&quot; -------------Elastic Model -------------&quot;</span>
<span class="nb">puts</span> <span class="s2">&quot; -------------Static Pushover Analysis -------------&quot;</span>
<span class="nb">source</span> Ex4.Portal2D.build.ElasticElement.tcl
<span class="nb">source</span> Ex4.Portal2D.analyze.Static.Push.tcl
</pre></div></blockquote>
<ul><li>To run Uniaxial Inelastic Section, Nonlinear Model, Uniform Earthquake Excitation</li></ul>
<blockquote><div class="mw-highlight mw-content-ltr" dir="ltr"><pre><span></span><span class="nb">puts</span> <span class="s2">&quot; -------------Uniaxial Inelastic Section, Nonlinear Model -------------&quot;</span>
<span class="nb">puts</span> <span class="s2">&quot; -------------Uniform Earthquake Excitation -------------&quot;</span>
<span class="nb">source</span> Ex4.Portal2D.build.InelasticSection.tcl 
source Ex4.Portal2D.analyze.Dynamic.EQ.Uniform.tcl
</pre></div></blockquote>
<ul><li>To run Uniaxial Inelastic Material, Fiber Section, Nonlinear Model, Dynamic Bidirectional Earthquake Ground Motion</li></ul>
<blockquote><div class="mw-highlight mw-content-ltr" dir="ltr"><pre><span></span><span class="nb">puts</span> <span class="s2">&quot; -------------Uniaxial Inelastic Material, Fiber Section, Nonlinear Model -------------&quot;</span>
<span class="nb">puts</span> <span class="s2">&quot; -------------Dynamic Bidirectional Earthquake Ground Motion  -------------&quot;</span>
<span class="nb">source</span> Ex4.Portal2D.build.InelasticFiberSection.tcl
<span class="nb">source</span> Ex4.Portal2D.analyze.Dynamic.EQ.bidirect.tcl
</pre></div></blockquote>
<p><br />
</p>


