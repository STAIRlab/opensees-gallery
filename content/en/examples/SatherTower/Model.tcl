set dataDir .
# Define units
set kip 1
set inch 1
set sec 1

# Secondary units
set sq_in [expr $inch * $inch]
set quad_in [expr $sq_in * $sq_in]
set ksi [expr $kip / $sq_in]
set ft [expr 12 * $inch]
set g [expr 32.2 * $ft / ($sec * $sec)]
set slug [expr 1 / 1000]

# Remove previous models
wipe

# Start Model Builder
model basic -ndm 3 -ndf 6

# Set the path to your CSV file
set csvFilePath "$dataDir/ModifiedElemNodes.csv"

# Open the CSV file for reading
set csvFile [open $csvFilePath r]

# Skip the header line if present
gets $csvFile

# puts "Imported Nodes:"
# puts "Node Number  X  Y  Z"

# Loop through the CSV data and create nodes in OpenSees
while {[gets $csvFile line] != -1} {
    set nodeData [split $line ","]
    set node_num [lindex $nodeData 0]
    set x_ft [lindex $nodeData 1]
    set y_ft [lindex $nodeData 2]
    set z_ft [lindex $nodeData 3]
	
	# Convert from ft to inches
	set x [expr $x_ft * $ft]
    set y [expr $y_ft * $ft]
    set z [expr $z_ft * $ft]

    # Create the node in OpenSees
    node $node_num $x $y $z
	
	# puts "$node_num $x $y $z"
}
close $csvFile

# Import element definition from the modified sheet
set csvFilePath "$dataDir/ModifiedElemDef_cladding_updated.csv"
set csvFile_ElemDef [open $csvFilePath r]
gets $csvFile_ElemDef

# Geometry Def and Coordinate Transformation
geomTransf Linear 1 -1.0 0.0 0.0
geomTransf Linear 2 0.0 -1.0 0.0

uniaxialMaterial Elastic 1 [expr {29000 * $ksi}]

set csvFilePath "$dataDir/Section_df.csv"
set csvFile_Section_df [open $csvFilePath r]
gets $csvFile_Section_df

# Create empty dictionaries to store section/element data
array set sectionData {}
set elemData {}

# Read section data from section_df.csv
while {[gets $csvFile_Section_df line] != -1} {
    set section_df [split $line ","]
    set id_int [lindex $section_df 8]
    set sectionData($id_int) $section_df
}

# foreach key [array names sectionData] {
    # set value $sectionData($key)
    # puts "Key: $key, Value: $value"
# }
# set value $sectionData(1)
# puts $value

# Read element data from elemDef.csv and create elements
while {[gets $csvFile_ElemDef line] != -1} {
    set elemtData [split $line ","]
    set elem_tag [lindex $elemtData 0]
    set node_i [lindex $elemtData 1]
    set node_j [lindex $elemtData 2]
    set sect_id [lindex $elemtData 3]
    set transFlag [lindex $elemtData 4]
    set mass_addl [lindex $elemtData 5]
    set location_tracker [lindex $elemtData 6]
    set elem_type [lindex $elemtData 7]
    set material [lindex $elemtData 8]
	set Index [lindex $elemtData 9]

	# puts "$elemtData $elem_tag $node_i $node_j $sect_id $transFlag $mass_addl $location_tracker $elem_type $material $Index"
    set section_df $sectionData($Index)
	
	set A [lindex $section_df 1]
    set E [lindex $section_df 2]
    set G [lindex $section_df 3]
    set Jxx [lindex $section_df 4]
    set Ixt [lindex $section_df 5]
    set Iyt [lindex $section_df 6]
    set Mass [lindex $section_df 7]
	
	# puts "$elem_tag $node_i $node_j $A $material $E $G $Jxx $Ixt $Iyt $Mass"
	
	if {$elem_type eq "elasticBeamColumn"} {
		element elasticBeamColumn $elem_tag $node_i $node_j [expr $A * $sq_in] [expr $E * $ksi] [expr $G * $ksi] \
    [expr $Jxx * $quad_in] [expr $Ixt * $quad_in] [expr $Iyt * $quad_in] $transFlag '-mass' [expr ($Mass+$mass_addl) * $slug / $ft] '-lmass'
	} elseif {$elem_type eq "Truss"} {
		element truss $elem_tag $node_i $node_j [expr $A * $sq_in] $material -rho [expr $Mass * $slug / $ft] -cMass 1 -doRayleigh 1
	} else {
		puts "Warning: Unsupported element type: $elem_type"
	}			
}
close $csvFile_ElemDef
close $csvFile_Section_df

# Fixing the base of the structure
for {set n 100001} {$n <= 100016} {incr n} {
    fix $n 1 1 1 1 1 1
}

# Fixing the beam-column connections
set csvFilePath "$dataDir/joints.csv"
set csvFile_joints [open $csvFilePath r]
gets $csvFile_joints



while {[gets $csvFile_joints line] != -1} {

	set joints [split $line ","]
	array set cNodeTag {}
	set filtered_joints [list]
	
	foreach comp $joints {
		if {$comp ne ""} {
			lappend filtered_joints $comp
		}
	}
	
	set num_nodes [llength $filtered_joints]
	# puts $num_nodes
	
	set rNodeTag [lindex $joints 0]
	for {set n 1} {$n <= [expr $num_nodes - 1]} {incr n} {
		set cNodeTag($n) [lindex $joints $n]
	}
	for  {set n 1} {$n <= [expr $num_nodes - 1]} {incr n} {
		equalDOF $rNodeTag $cNodeTag($n) 1 2 3 4 5 6
	}
}

# Define Rayleigh Damping
set Lambda_list [eigen 10]  ;# eigenvalue mode 1
# set Lambda1 [lindex $Lambda_list 0]
# set Omega1 [expr {sqrt($Lambda1)}]
# set Lambda3 [lindex $Lambda_list 6]
# set Omega3 [expr {sqrt($Lambda3)}]
# set xDamp 0.05  ;# 5% damping ratio
# set alphaM [expr {($xDamp * 2 * $Omega1 * $Omega3) / ($Omega1 + $Omega3)}]
# set betaKcomm [expr {2 * $xDamp / ($Omega1 + $Omega3)}]
# set betaKcurr 0.0
# set betaKinit 0.0
# rayleigh $alphaM $betaKcurr $betaKinit $betaKcomm  ;# rayleigh damping
rayleigh 0.4566902904613236 0 0 0.003638674231699657  ;# rayleigh damping              



		# set b [lindex $joints 1]
		# set c [lindex $joints 2]
		# set d [lindex $joints 3]
		# set e [lindex $joints 4]
		# set f [lindex $joints 5]
		# set g [lindex $joints 6]
		# set h [lindex $joints 7]
		# set i [lindex $joints 8]
		# set j [lindex $joints 9]
		# set k [lindex $joints 10]
		# set l [lindex $joints 11]
# # Loop for element creation 
# while {[gets $csvFile_ElemDef line] != -1} {
	# set elemtData [split $line ","]
	# set elem_tag [lindex $elemtData 0]
	# set node_i [lindex $elemtData 1]
	# set node_j [lindex $elemtData 2]
	# set sect_id [lindex $elemtData 3]
	# set transFlag [lindex $elemtData 4]
	# set mass_addl [lindex $elemtData 5]
	# set location_tracker [lindex $elemtData 6]
	# set elem_type [lindex $elemtData 7]
	# set material [lindex $elemtData 8]
# }

# while {[gets $csvFile_Section_df line] != -1} {
	# set section_df [split $line ","]
	# set A [lindex $section_df 0]
	# set E [lindex $section_df 1]
	# set G [lindex $section_df 2]
	# set Jxx [lindex $section_df 3]
	# set Ixt [lindex $section_df 4]
	# set Iyt [lindex $section_df 5]
	# set Mass [lindex $section_df 6]
# }
















# # Importing element definitions from the modified sheet
# set elemDefFile "ModifiedElemDef_cladding.csv"
# set elemDefHandle [open $elemDefFile r]
# set elemDefData [read $elemDefHandle]
# close $elemDefHandle

# # Split the CSV data into lines
# set elemDefLines [split $elemDefData "\n"]

# # Geometry Def and Coordinate Transformation
# geomTransf Linear 1 -1.0 0.0 0.0
# geomTransf Linear 2 0.0 -1.0 0.0

# uniaxialMaterial Elastic 1 [expr {29000 * $ksi}]

# # Iteration for element creation
# foreach line $elemDefLines {
    # set fields [split $line ","]
    # if {[llength $fields] == 9} {
        # set elem_tag [lindex $fields 0]
        # set node_i [lindex $fields 1]
        # set node_j [lindex $fields 2]
        # set A [lindex $fields 3]
        # set mass [lindex $fields 4]
        # set elem_type [lindex $fields 5]

        # # Adding additional mass to element mass
        # if {[string is double -strict [lindex $fields 4]] && [lindex $fields 4] > 0} {
            # set mass [expr {$mass + [lindex $fields 4]}]
        # }

        # # Creating Beam/Column Elements
        # if {$elem_type == "elasticBeamColumn"} {
            # set E [lindex $fields 6]
            # set G [lindex $fields 7]
            # set Jxx [lindex $fields 8]
            # set Ixt [lindex $fields 9]
            # set Iyt [lindex $fields 10]
            # set transFlag [lindex $fields 11]

            # element $elem_type $elem_tag $node_i $node_j $A $E $G $Jxx $Ixt $Iyt $transFlag -mass [expr {$mass * $slug / $ft}] -lmass
        # }

        # # Creating Truss Elements
        # elseif {$elem_type == "Truss"} {
            # set matTag [lindex $fields 6]
            # element $elem_type $elem_tag $node_i $node_j $A $matTag -rho [expr {$mass * $slug / $ft}] -cMass 1
        # }
    # }
# }

# # Fixing the beam-column connections
# set joints_df [list]
# foreach n [list 0 1 2 3 4] {
    # set joint_group [list]
    # foreach row $elemDefLines {
        # set fields [split $row ","]
        # set node_num [lindex $fields 1]

        # # Check if node_num is a valid integer and a non-empty string
        # if {[string is integer -strict $node_num] && $node_num ne "" && ($node_num % 1000) == $n} {
            # lappend joint_group $node_num
        # }
    # }

    # if {[llength $joint_group] == 0} {
        # puts "joint_group is empty for node_num [expr {$n * 1000}]"
        # break
    # } elseif {[llength $joint_group] == 1} {
        # puts "Joint group for node [expr {$n * 1000}] only has one node."
    # } else {
        # set master_col_node [lindex $joint_group 0]
        # for {set i 1} {$i < [llength $joint_group]} {incr i} {
            # equalDOF $master_col_node [lindex $joint_group $i] 1 2 3 4 5 6
        # }
    # }
    # lappend joints_df "---Joint [expr {$n + 1}]"
    # lappend joints_df $joint_group
# }


