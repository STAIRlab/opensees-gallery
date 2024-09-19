---
title: "Ex5 - 2D Frame, 3-story 3-bay, Reinforced-Concrete Section & Steel W-Section"
draft: true
---

<h2><span class="mw-headline" id="Introduction">Introduction</span></h2>
<p>This examples demonstrates how to build a 3-story,3-bay frame. The nodes and elements are specified one by one.
</p><p><br />
</p>
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

<div class="card mb-3" style="max-width: 540px;">
  <div class="row g-0">
    <div class="col-md-4">
      <img class="img-fluid rounded-start" src="ExampleFigure_Cyclic.GIF" width="142" height="347" />
    </div>
    <div class="col-md-8">
      <div class="card-body">
        <h5 class="card-title">Card title</h5>
        <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
        <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
      </div>
    </div>
  </div>
</div>

<div class="card mb-3" style="max-width: 540px;">
  <div class="row g-0">
    <div class="col-md-4">
      <img class="img-fluid rounded-start" src="ExampleFigure_Cyclic.GIF" width="142" height="347" />
    </div>
    <div class="col-md-8">
      <div class="card-body">
        <h5 class="card-title">Card title</h5>
        <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
        <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
      </div>
    </div>
  </div>
</div>

<table style="margin:0; background:none;">
<tbody>
<tr>
<td style="margin:0; width:25%; border:3px solid #ccc; background:#white; vertical-align:top;">
  <h4><span class="mw-headline" id="Elastic_Element">Elastic Element</span></h4><hr />
    <table style="width:100%; vertical-align:top;background:#white;">
    <tbody>
<tr>
<td style="color:#000;"><div>
<p><a href="/wiki/index.php/OpenSees_Example_5._2D_Frame,_3-story_3-bay,_Reinforced-Concrete_Section_%26_Steel_W-Section" title="OpenSees Example 5. 2D Frame, 3-story 3-bay, Reinforced-Concrete Section &amp; Steel W-Section"><img alt="ExampleFigure ElasticSection.GIF" src="ExampleFigure_ElasticSection.GIF" width="270" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex5.Frame2D.build.ElasticSection.tcl" class="internal" title="Ex5.Frame2D.build.ElasticSection.tcl">Ex5.Frame2D.build.ElasticSection.tcl</a></li>
<li><a href="LibUnits.tcl" class="internal" title="LibUnits.tcl">LibUnits.tcl</a></li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>Effective axial and flexural stiffnesses are defined at the element level</li>
<li>elasticBeamColumn elements</li></ul>
</div>
</td>
</tr>
</tbody>
</table>

</td>
<td style="margin:0; width:25%; border:3px solid #ccc; background:#white; vertical-align:top;">
<h4><span id="Distributed_Plasticity_Element,_Uniaxial_Section"></span><span class="mw-headline" id="Distributed_Plasticity_Element.2C_Uniaxial_Section">Distributed Plasticity Element, Uniaxial Section</span></h4><hr /><table style="width:100%; vertical-align:top;background:#white;">


<tbody><tr>
<td style="color:#000;"><div>
<p><a href="/wiki/index.php/OpenSees_Example_5._2D_Frame,_3-story_3-bay,_Reinforced-Concrete_Section_%26_Steel_W-Section" title="OpenSees Example 5. 2D Frame, 3-story 3-bay, Reinforced-Concrete Section &amp; Steel W-Section"><img alt="ExampleFigure uniaxialSection.GIF" src="ExampleFigure_uniaxialSection.GIF" width="267" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex5.Frame2D.build.InelasticSection.tcl" class="internal" title="Ex5.Frame2D.build.InelasticSection.tcl">Ex5.Frame2D.build.InelasticSection.tcl</a></li>
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
<h4><span id="Distributed_Plasticity_Element,_Fiber_Section"></span><span class="mw-headline" id="Distributed_Plasticity_Element.2C_Fiber_Section">Distributed Plasticity Element, Fiber Section</span></h4><table style="width:100%; vertical-align:top;background:#white;">

</table><table style="width:100%; border:1px solid #ddcef2; vertical-align:top;background:#white;">

<tbody><tr>
<td style="color:#000;"><div>
<h5><span class="mw-headline" id="FiberSection_--_Standard_AISC_W-Section">FiberSection -- Standard AISC W-Section</span></h5>
<p><a href="/wiki/index.php/OpenSees_Example_5._2D_Frame,_3-story_3-bay,_Reinforced-Concrete_Section_%26_Steel_W-Section" title="OpenSees Example 5. 2D Frame, 3-story 3-bay, Reinforced-Concrete Section &amp; Steel W-Section"><img alt="ExampleFigure FiberSection W.GIF" src="ExampleFigure_FiberSection_W.GIF" width="299" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex5.Frame2D.build.InelasticFiberWSection.tcl" class="internal" title="Ex5.Frame2D.build.InelasticFiberWSection.tcl">Ex5.Frame2D.build.InelasticFiberWSection.tcl</a></li>
<li><a href="LibUnits.tcl" class="internal" title="LibUnits.tcl">LibUnits.tcl</a></li>
<li><a href="Wsection.tcl" class="internal" title="Wsection.tcl">Wsection.tcl</a></li></ul>
<hr />


<p><strong>Notes</strong>
</p>
<ul><li>The section is broken down into fibers where uniaxial materials are defined independently.</li>
<li>The program calculates flexural and axial stiffnesses/strength by integrating strains across the section.</li>
<li>Standard AISC W-section</li></ul>
</div>
</td></tr></tbody></table>
<hr />
<table style="width:100%; border:1px solid #ddcef2; vertical-align:top;background:#white;">

<tbody><tr>
<td style="color:#000;"><div>
<h5><span class="mw-headline" id="FiberSection_--_Reinforced_Concrete_Section">FiberSection -- Reinforced Concrete Section</span></h5>
<p><a href="/wiki/index.php/OpenSees_Example_5._2D_Frame,_3-story_3-bay,_Reinforced-Concrete_Section_%26_Steel_W-Section" title="OpenSees Example 5. 2D Frame, 3-story 3-bay, Reinforced-Concrete Section &amp; Steel W-Section"><img alt="ExampleFigure FiberSection RC.GIF" src="ExampleFigure_FiberSection_RC.GIF" width="299" height="263" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex5.Frame2D.build.InelasticFiberRCSection.tcl" class="internal" title="Ex5.Frame2D.build.InelasticFiberRCSection.tcl">Ex5.Frame2D.build.InelasticFiberRCSection.tcl</a></li>
<li><a href="LibUnits.tcl" class="internal" title="LibUnits.tcl">LibUnits.tcl</a></li>
<li><a href="LibMaterialsRC.tcl" class="internal" title="LibMaterialsRC.tcl">LibMaterialsRC.tcl</a></li>
<li><a href="BuildRCrectSection.tcl" class="internal" title="BuildRCrectSection.tcl">BuildRCrectSection.tcl</a></li></ul>
<hr />
<p><strong>Notes</strong>
</p>
<ul><li>The section is broken down into fibers where uniaxial materials are defined independently.</li>
<li>The program calculates flexural and axial stiffnesses/strength by integrating strains across the section.</li>
<li>Rectangular Reinforced-Concrete Section</li></ul>
</div>
</td></tr></tbody></table>
</td></tr><tr><td></td></tr></tbody></table>
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
<p><a href="/wiki/index.php/OpenSees_Example_5._2D_Frame,_3-story_3-bay,_Reinforced-Concrete_Section_%26_Steel_W-Section" title="OpenSees Example 5. 2D Frame, 3-story 3-bay, Reinforced-Concrete Section &amp; Steel W-Section"><img alt="ExampleFigure Push.GIF" src="ExampleFigure_Push.GIF" width="142" height="347" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex5.Frame2D.analyze.Static.Push.tcl" class="internal" title="Ex5.Frame2D.analyze.Static.Push.tcl">Ex5.Frame2D.analyze.Static.Push.tcl</a></li>
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
<p>
<img alt="ExampleFigure Cyclic.GIF" src="ExampleFigure_Cyclic.GIF" width="142" height="347" />
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex5.Frame2D.analyze.Static.Cycle.tcl" class="internal" title="Ex5.Frame2D.analyze.Static.Cycle.tcl">Ex5.Frame2D.analyze.Static.Cycle.tcl</a></li>
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
</tr>

<tr>
<td style="margin:0; width:25%; border:3px solid #ccc; background:#white; vertical-align:top;">
<h4><span class="mw-headline" id="Dynamic_EQ_Ground_Motion">Dynamic EQ Ground Motion</span></h4>
<table style="width:100%; border:1px solid #ddcef2; vertical-align:top;background:#white;">

<tbody><tr>
<td style="color:#000;"><div>
<h5><span class="mw-headline" id="Dynamic_Uniform_Sine-Wave_Ground_Motion">Dynamic Uniform Sine-Wave Ground Motion</span></h5>
<p><a href="/wiki/index.php/OpenSees_Example_5._2D_Frame,_3-story_3-bay,_Reinforced-Concrete_Section_%26_Steel_W-Section" title="OpenSees Example 5. 2D Frame, 3-story 3-bay, Reinforced-Concrete Section &amp; Steel W-Section"><img alt="ExampleFigure UniformSine.GIF" src="ExampleFigure_UniformSine.GIF" width="294" height="202" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex5.Frame2D.analyze.Dynamic.sine.Uniform.tcl" class="internal" title="Ex5.Frame2D.analyze.Dynamic.sine.Uniform.tcl">Ex5.Frame2D.analyze.Dynamic.sine.Uniform.tcl</a></li>
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
<p><a href="/wiki/index.php/OpenSees_Example_5._2D_Frame,_3-story_3-bay,_Reinforced-Concrete_Section_%26_Steel_W-Section" title="OpenSees Example 5. 2D Frame, 3-story 3-bay, Reinforced-Concrete Section &amp; Steel W-Section"><img alt="ExampleFigure UniformEQ.GIF" src="ExampleFigure_UniformEQ.GIF" width="294" height="202" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex5.Frame2D.analyze.Dynamic.EQ.Uniform.tcl" class="internal" title="Ex5.Frame2D.analyze.Dynamic.EQ.Uniform.tcl">Ex5.Frame2D.analyze.Dynamic.EQ.Uniform.tcl</a></li>
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
<p><a href="/wiki/index.php/OpenSees_Example_5._2D_Frame,_3-story_3-bay,_Reinforced-Concrete_Section_%26_Steel_W-Section" title="OpenSees Example 5. 2D Frame, 3-story 3-bay, Reinforced-Concrete Section &amp; Steel W-Section"><img alt="ExampleFigure MultiSupportSine.GIF" src="ExampleFigure_MultiSupportSine.GIF" width="294" height="202" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex5.Frame2D.analyze.Dynamic.sine.multipleSupport.tcl" class="internal" title="Ex5.Frame2D.analyze.Dynamic.sine.multipleSupport.tcl">Ex5.Frame2D.analyze.Dynamic.sine.multipleSupport.tcl</a> (this file may need to be corrected for displacement input)</li>
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
<p><a href="/wiki/index.php/OpenSees_Example_5._2D_Frame,_3-story_3-bay,_Reinforced-Concrete_Section_%26_Steel_W-Section" title="OpenSees Example 5. 2D Frame, 3-story 3-bay, Reinforced-Concrete Section &amp; Steel W-Section"><img alt="ExampleFigure MultiSupportEQ.GIF" src="ExampleFigure_MultiSupportEQ.GIF" width="294" height="202" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex5.Frame2D.analyze.Dynamic.EQ.multipleSupport.tcl" class="internal" title="Ex5.Frame2D.analyze.Dynamic.EQ.multipleSupport.tcl">Ex5.Frame2D.analyze.Dynamic.EQ.multipleSupport.tcl</a> (this file needs to be corrected for displacement input)</li>
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
<p><a href="/wiki/index.php/OpenSees_Example_5._2D_Frame,_3-story_3-bay,_Reinforced-Concrete_Section_%26_Steel_W-Section" title="OpenSees Example 5. 2D Frame, 3-story 3-bay, Reinforced-Concrete Section &amp; Steel W-Section"><img alt="ExampleFigure BidirectEQ.GIF" src="ExampleFigure_BidirectEQ.GIF" width="294" height="202" /></a>
</p>
<hr />
<p><strong>Files</strong>
</p>
<ul><li><a href="Ex5.Frame2D.analyze.Dynamic.EQ.bidirect.tcl" class="internal" title="Ex5.Frame2D.analyze.Dynamic.EQ.bidirect.tcl">Ex5.Frame2D.analyze.Dynamic.EQ.bidirect.tcl</a></li>
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
<span class="nb">source</span> Ex5.Frame2D.build.ElasticSection.tcl
<span class="nb">source</span> Ex5.Frame2D.analyze.Static.Push.tcl
</pre></div></blockquote>
<ul><li>To run Uniaxial Inelastic Section, Nonlinear Model, Uniform Earthquake Excitation</li></ul>
<blockquote><div class="mw-highlight mw-content-ltr" dir="ltr"><pre><span></span><span class="nb">puts</span> <span class="s2">&quot; -------------Uniaxial Inelastic Section, Nonlinear Model -------------&quot;</span>
<span class="nb">puts</span> <span class="s2">&quot; -------------Uniform Earthquake Excitation -------------&quot;</span>
<span class="nb">source</span> Ex5.Frame2D.build.InelasticSection.tcl 
source Ex5.Frame2D.analyze.Dynamic.EQ.Uniform.tcl
</pre></div></blockquote>
<ul><li>To run Uniaxial Inelastic Material, Fiber Section, Nonlinear Model, Dynamic Bidirectional Earthquake Ground Motion</li></ul>
<blockquote><div class="mw-highlight mw-content-ltr" dir="ltr"><pre><span></span><span class="nb">puts</span> <span class="s2">&quot; -------------Uniaxial Inelastic Material, Fiber Section, Nonlinear Model -------------&quot;</span>
<span class="nb">puts</span> <span class="s2">&quot; -------------Dynamic Bidirectional Earthquake Ground Motion  -------------&quot;</span>
<span class="nb">source</span> Ex5.Frame2D.build.InelasticFiberSection.tcl
<span class="nb">source</span> Ex5.Frame2D.analyze.Dynamic.EQ.bidirect.tcl
</pre></div></blockquote>
<p><br />
</p>
<h2><span class="mw-headline" id="Notes">Notes</span></h2>
<hr />
<p>Return to <a href="/wiki/index.php/OpenSees_Examples_Manual_--_Structural_Models_%26_Analyses" class="mw-redirect" title="OpenSees Examples Manual -- Structural Models &amp; Analyses">OpenSees Examples Manual -- Structural Models &amp; Analyses</a>
</p><p>Return to <a href="/wiki/index.php/OpenSees_User" title="OpenSees User">OpenSees User</a>
</p>




