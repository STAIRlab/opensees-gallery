---
title: Concrete Frame Pushover Analysis
#title: Plane Concrete Frame
tags: ["Python", "Tcl", "Frame"]
---


In this example the reinforced concrete portal frame which has
undergone the gravity load analysis is now be subjected to a pushover
analysis.

<p>Files Required:</p>
<ol>
<li><a href="RCFrameGravity.tcl" title="wikilink">RCFrameGravity.tcl</a></li>
<li><a href="RCFramePushover.tcl" title="wikilink">RCFramePushover.tcl</a></li>
</ol>

The Python version is adapted from https://openseespydoc.readthedocs.io/en/latest/src/RCFrameGravity.html

<p>NOTES: This example demonstrates the use of Tcl programming in order
to perform the nonlinear analysis. When dealing with nonlinear problems,
the models do not always converge for the analysis options of choice.
For this reason it is sometimes necessary to step through the analysis,
checking for convergence at each step and trying different options if
the analysis fails at any particular step. This script makes use of the
fact that many OpenSees commands actually return values that can be used
in the script.</p>

<h4 id="model">Model</h4>

<p>The `RCFrameGravity` script is first run using the "source" command.
The model is now under gravity and the pseudo-time in the model is 1.0
[= 10 * 0.1 load steps]. The existing loads in the model are now set to
constant and the time is reset to 0.0. A new load pattern with a linear
time series and horizontal loads of magnitude 10.0 acting at nodes 3 and
4 is then added to the model.</p>
<p>It should be noted that when using a displacement control strategy,
as we will employ in the pushover analysis, these horizontal loads are
the reference loads that are being applied. The actual loads that are
applied will equal these values multiplied by the load factor that the
displacement control integration scheme determines is necessary to
enforce the requested displacement.</p>
<p><pre></p>
<ol>
<li>Do operations of RCFrameGravity by sourcing in the tcl file</li>
</ol>
<p>source RCFrameGravity.tcl</p>
<ol>
<li>Set the gravity loads to be constant &amp; reset the time in the
domain</li>
</ol>
<p>loadConst -time 0.0</p>
<ol>
<li>Define reference lateral loads for Pushover Analysis</li>
<li><hr /></li>
</ol>
<ol>
<li>Set some parameters</li>
</ol>
<p>set H 10.0; # Reference lateral load</p>
<ol>
<li>Set lateral load pattern with a Linear TimeSeries</li>
</ol>
<p>pattern Plain 2 "Linear" {</p>
<ol>
<li>Create nodal loads at nodes 3 &amp; 4</li>
<li>nd FX FY MZ</li>
</ol>
<p>load 3 $H 0.0 0.0 load 4 $H 0.0 0.0 } </pre></p>

<h4 id="recorder">Recorder</h4>
<p>After the model as been created, but before the analysis is performed
we will create two recorder objects. The first will record and write the
nodal displacements and nodes 3 and 4 to a file named node34.out. The
second recorder is an envelope element recorder that will write the
envelope (max, min and abs max) of element forces at the 3 elements to a
file ele32.out.</p>
<p><pre></p>
<ol>
<li>Create a recorder to monitor nodal displacements</li>
</ol>
<p>recorder Node -file node32.out -time -node 3 4 -dof 1 2 3 disp</p>
<ol>
<li>Create a recorder to monitor element forces in columns</li>
</ol>
<p>recorder EnvelopeElement -file ele123.out -time -ele 1 2 forces
</pre></p>

<h4 id="analysis">Analysis</h4>
<p>For the Pushover analysis we will use a displacement control
strategy. In displacement control we specify a incremental displacement
that we would like to see at a nodal dof and the strategy iterates to
determine what the pseudo-time (load factor if using a linear time
series) is required to impose that incremental displacement. For this
example, at each new step in the analysis the integrator will determine
the load increment necessary to increment the horizontal displacement at
node 3 by 0.1 in. A target displacement of $maxU (15.0 inches) is
sought.

As the example is nonlinear and nonlinear models do not always
converge the analysis is carried out inside a while loop. The loop will
either result in the model reaching it's target displacement or it will
fail to do so. At each step a single analysis step is performed. If the
analysis step fails using standard Newton solution algorithm, another
strategy using initial stiffness iterations will be attempted.

```tcl
# set some parameters
set maxU 15.0; # Max displacement set ok 0 set currentDisp 0.0

# perform the analysis
while {$ok == 0 &amp;&amp; $currentDisp < $maxU} {
    set ok [analyze 1]

    # if the analysis fails try initial tangent iteration
    if {$ok != 0} { 
        puts "regular newton failed .. lets try an initial stiffness for this step" 
        test NormDispIncr 1.0e-12 1000 
        algorithm ModifiedNewton -initial 
        set ok [analyze 1] 
        if {$ok == 0} {
            puts "that worked .. back to regular newton"
        }
        test NormDispIncr 1.0e-12 10 algorithm Newton 
    }
}
set currentDisp [nodeDip 3 1]
}

# print out a SUCCESS or FAILURE MESSAGE
if {$ok == 0} { 
    puts "Pushover analysis completed SUCCESSFULLY"; }
else {
    puts "Pushover analysis FAILED"; 
}
```

<h4 id="running_the_script">Running the Script</h4>
When the script is run the following will appear.

<figure>
<img src="/OpenSeesRT/contrib/static/RCFramePushoverRun.png" title="RCFramePushoverRun.png"
alt="RCFramePushoverRun.png" />
<figcaption aria-hidden="true">RCFramePushoverRun.png</figcaption>
</figure>
<p>NOTES:</p>
<ol>
<li>In the ouput you will notice the results of the print commands in
the previous file.</li>
<li>You will also see a lot of warning messages. These are times within
the analysis script that the analysis step has failed and the
alternative initial step iterations are being performed.</li>
<li>The puts messgae at the end indicates that the pushover analysis was
succesfull.</li>
</ol>
<figure>
<img src="/OpenSeesRT/contrib/static/RCFramePushoverCurve.png" title="RCFramePushoverCurve.png"
alt="RCFramePushoverCurve.png" />
<figcaption aria-hidden="true">RCFramePushoverCurve.png</figcaption>
</figure>


