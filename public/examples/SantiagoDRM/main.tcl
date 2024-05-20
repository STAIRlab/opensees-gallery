wipe

# =================================================================================
# STKO COMMON VARIABLES (STKO_VAR_***)
# =================================================================================

# The current process id (from 0 to NP-1)
set STKO_VAR_process_id [getPID]
# A boolean flag for parallel processing (True if NP > 1)
set STKO_VAR_is_parallel 0
# The result from analyze command  (0 if succesfull)
set STKO_VAR_analyze_done 0
# The increment counter in the current stage
set STKO_VAR_increment 0
# The current time
set STKO_VAR_time 0.0
# The current time increment
set STKO_VAR_time_increment 0.0
# The current stage percentage
set STKO_VAR_percentage 0.0
# The last number of iterations
set STKO_VAR_num_iter 0
# The last error norm
set STKO_VAR_error_norm 0.0
# A list of custom functions called before solving the current time step
set STKO_VAR_OnBeforeAnalyze_CustomFunctions {}
# A list of custom functions called after solving the current time step
set STKO_VAR_OnAfterAnalyze_CustomFunctions {}
# A list of monitor functions
set STKO_VAR_MonitorFunctions {}
# for backward compatibility (STKO version < 3.1.0).
# It is now deprecated and will be removed in future versions.
set all_custom_functions {}
# Call functions before the analyze command.
proc STKO_CALL_OnBeforeAnalyze {} {
	global STKO_VAR_OnBeforeAnalyze_CustomFunctions
	foreach item $STKO_VAR_OnBeforeAnalyze_CustomFunctions {
		$item
	}
}
# Call functions after the analyze command.
proc STKO_CALL_OnAfterAnalyze {} {
	global STKO_VAR_analyze_done
	global STKO_VAR_OnAfterAnalyze_CustomFunctions
	global all_custom_functions
	global STKO_VAR_MonitorFunctions
	foreach item $STKO_VAR_OnAfterAnalyze_CustomFunctions {
		$item
	}
	if {$STKO_VAR_analyze_done == 0} {
		foreach item $all_custom_functions {
			$item
		}
		foreach item $STKO_VAR_MonitorFunctions {
			$item
		}
	}
}

# =================================================================================
# SOURCING
# =================================================================================


model basic -ndm 3 -ndf 3
# source definitions
source definitions.tcl
# source materials
source materials.tcl
# source sections
source sections.tcl
# source node
source nodes.tcl
# source element
source elements.tcl
# source analysis_steps
source analysis_steps.tcl

wipe
