proc ReadSMDFile {inFilename outFilename numdatperln dt npts} {
	#########################################################
	# ReadSMDFile $inFilename $outFilename $dt			
	#########################################################
	# read gm input format and output to opensees file
	#
	# Written: MHS
	# Date: July 2000
	#
	# A procedure which parses a ground motion record from the PEER
	# strong motion database by finding dt in the record header, then
	# echoing data values to the output file.
	#
	# Formal arguments
	#	inFilename -- file which contains PEER strong motion record
	#	outFilename -- file to be written in format G3 can read
	#	dt -- time step determined from file header
	#
	# Assumptions
	#	The header in the PEER record is, e.g., formatted as follows:
	#	 PACIFIC ENGINEERING AND ANALYSIS STRONG-MOTION DATA
	#	  IMPERIAL VALLEY 10/15/79 2319, EL CENTRO ARRAY 6, 230					
	#	  ACCELERATION TIME HISTORY IN UNITS OF G							  
	#	  NPTS=  3930, DT= .00500 SEC
	
	upvar $dt DT;		# Pass dt by reference
      upvar $npts NPTS;
	# Open the input file and catch the error if it can't be read
      set NPTS 0;
	  set Nline 0;
	if [catch {open $inFilename r} inFileID] {
		puts stderr "Cannot open $inFilename for reading"
	} else {
		# Open output file for writing
		set outFileID [open $outFilename w]

		# Flag indicating dt is found and that ground motion
		# values should be read -- ASSUMES dt is on last line
		# of header!!!
		set flag 0
		# Look at each line in the file
		foreach line [split [read $inFileID] \n] {
		    set Nline [expr $Nline+1]
			if {$Nline < 4} {
				# Blank line --> do nothingat
				continue
			} elseif {$Nline == 4} {
			 foreach word [split $line] {
              if {$word !=""} {
               incr wordloop 1;
               if {$wordloop == 2 } {
                set NPTS $word; 
               }
               if {$wordloop == 4 } {
                set DT $word; 
			    break
               }
              }
             }			  
			} else {
			  puts $outFileID $line
			}
			
		}
            
		close $outFileID;	# Close the output file
		close $inFileID;	# Close the input file
	}
	}