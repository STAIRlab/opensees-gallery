# ----------------------------------------------------------------------------------
# Modeled by Chrystal Chern, UC Berkeley, cchern@berkeley.edu.  Date: April 20, 2023.
# ----------------------------------------------------------------------------------

#
# #+# HARD-CODED CONFIGURATION ----------------------------------------------------------------
set debug "--debug"; 												# print the specified options
# model configuration
set transformation PDelta; 											# geometric transformation linearity for element deformations
set column_linearity nonlinear; 										# column element material linearity
set column_pins 3; 													# 1 - all rigid; 2 - all pinned; 3 - mixed rigid/pinned; 4 - all zerolength fiber sections; 5 - all integration point fiber sections
set column_capbeam_joint none; 										# rigid offsets between tops of columns and column-cap beam joints
set abutment_model linear; 											# abutment model ("none", "linear", "simplified", or "complex")
set hinge_model linear; 											# in-span hinge model ("none", "linear", "simplified", or "complex")
set Ec 3530.5; 														# concrete modulus of elasticity (ksi)
set Ecol 3530.5; 													# column concrete modulus of elasticity (ksi)
set Es 29000.0; 													# steel tensile modulus of elasticity (initial elastic tangent, ksi)
set CGa 50.0; 														# abutment shear stiffness coefficient
set CGh 60.0; 														# in-span hinge shear stiffness coefficient
# analysis settings
set dynamic_on 1; 													# turn the dynamic analysis on (1) or off (0)
set dynamic_truncated 0; 											# truncate the dynamic analysis to the first t timesteps (1)
set dynamic_timesteps 100;											# the t timesteps to which the the dynamic analysis is truncated
set input_location "401"; 											# locations (node numbers) corresponding to ground motion input. 0 for multiple support excitation.
set dynamic_integrator Newmark; 									# numerical integration method
set damping_type rayleigh;        									# damping strategy
set damping_modes "1,2"; 											# damping modes
set damping_modes [split $damping_modes {,}];
set damping_ratios "0.015,0.015"; 									# damping ratios
set damping_ratios [split $damping_ratios {,}];
set rayleigh_zerolength_on 1;      									# turn rayleigh damping on (1) for zerolength elements (abutment, hinge, and column pin springs)
set dynamic_scale_factor 1.0;										# scale factor applied to input ground motion
set record_zip [lindex $argv 1]; 									# path to zip file containing the recorded motions for ground motion input
set output_directory [lindex $argv 2]; 								# Set data output directory
file mkdir $output_directory;  										# Create data output directory if it doesn't exist
# results output
set model_name "hwd_model"
set modeling_matrix 1
set runtime 1
set eigen_modal_tracking 0
set ssid_modal_tracking 0
set compare_response_history 1

set override 2

source hwd.tcl