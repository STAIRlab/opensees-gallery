##################################################################################################################
# Generate_lognrmrand.tcl
#
# SubRoutine to generate a log-normally distributed random variable for a specified mean and standard deviation.
#
##################################################################################################################
#
# Input Arguments:
#------------------
# meanX 		Mean value of the variable X
# stdlnX 		Standard deviation of the logarithmic values of the variable X 
# xRandom		The subroutine output --> random variable
#
# Written by: Dr. Ahmed Elkady, University of Southampton, UK
#
##################################################################################################################

proc random-normal { mean stdev number } {
    set twopi [expr 2*acos(-1)]

    if { $stdev <= 0.0 } {
	return -code error -errorcode ARG \
		-errorinfo "Standard deviation must be positive" \
		"Standard deviation must be positive"
    }

#    set result {}
#    for { set i 0 }  {$i < $number } { incr i } {
#        lappend result [Inverse-cdf-normal $mean $stdev [expr {rand()}]]
#    }

    set result {}

    for { set i 0 }  {$i < $number } { incr i 2 } {
        set angle [expr {$twopi * rand()}]
        set rad   [expr {sqrt(-2.0*log(rand()))}]
        set xrand [expr {$rad * cos($angle)}]
        set yrand [expr {$rad * sin($angle)}]
        lappend result [expr {$mean + $stdev * $xrand}]
        if { $i < $number-1 } {
            lappend result [expr {$mean + $stdev * $yrand}]
        }
    }

    return $result
}

proc Generate_lognrmrand {meanX stdlnX} {

	# package require math::statistics
	global xRandom
		
	set meanlnX  [expr log($meanX)];
	set number 1;
	
	#set y [::math::statistics::random-normal $meanlnX $stdlnX $number];
	set y [random-normal $meanlnX $stdlnX $number];
	
	set xRandom [expr exp($y)];

}
