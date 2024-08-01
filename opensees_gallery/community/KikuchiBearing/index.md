---
title: Kikuchi Bearing
tags: ["Other"]
image: KikuchiBearing_Model.png
---

<img src="400px-KikuchiBearing_Model.png" width="400" height="256" srcset="/wiki/images/thumb/2/26/KikuchiBearing_Model.png/600px-KikuchiBearing_Model.png 1.5x, /wiki/images/thumb/2/26/KikuchiBearing_Model.png/800px-KikuchiBearing_Model.png 2x">

## Examples

```tcl
element KikuchiBearing 1 1 2 -shape round -size 1.016 0.320 -nMSS 8 \
        -matMSS 1 -nMNS 30 -matMNS 2
```

<p><a href="Media:KikuchiBearing_Sample.tcl"
title="wikilink">KikuchiBearing_Sample.tcl</a>, <a
href="Media:KikuchiBearing_input_Z.tcl"
title="wikilink">KikuchiBearing_input_Z.tcl</a>, <a
href="Media:KikuchiBearing_input_X.tcl"
title="wikilink">KikuchiBearing_input_X.tcl</a></p>
<table>
<tbody>
<tr class="odd">
<td><p>case 1: P-Delta effect not considered (use -noPDInput -noTilt
option)</p></td>
</tr>
<tr class="even">
<td><p>case 2: P-Delta effect considered, uniform distribution of
compression modulus</p></td>
</tr>
<tr class="odd">
<td><p>case 3: P-Delta effect considered (use -lambda option)</p></td>
</tr>
</tbody>
</table>

<p><img 
  src="KikuchiBearing_ForceDeformation_case1_v2.png"
  title="KikuchiBearing_ForceDeformation_case1_v2.png" width="250"
  alt="KikuchiBearing_ForceDeformation_case1_v2.png" />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
<img
  src="KikuchiBearing_ForceDeformation_case2_v2.png"
  title="KikuchiBearing_ForceDeformation_case2_v2.png" 
  width="250"
  alt="KikuchiBearing_ForceDeformation_case2_v2.png" />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
<img
  src="KikuchiBearing_ForceDeformation_case3_v2.png"
  title="KikuchiBearing_ForceDeformation_case3_v2.png" width="250"
  alt="KikuchiBearing_ForceDeformation_case3_v2.png" /></p>

## References

<p>M. Kikuchi , I. D. Aiken and A. Kasalanati , "Simulation analysis for
the ultimate behavior of full-scale lead-rubber seismic isolation
bearings", <em>15th World Conference on Earthquake Engineering</em>, No.
1688, 2012.</p>
<hr />

<p>Code Developed by: <span style="color:blue"> mkiku
</span></p>

