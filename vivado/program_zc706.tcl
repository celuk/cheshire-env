open_hw_manager
connect_hw_server
open_hw_target

if { $argc > 0 } {
    set bitstream_file [lindex $argv 0]
} else {
    puts "No bitstream file specified, using default."
    set bitstream_file "/home/shc/projects/cheshire-env/vivado/cheshire_zc706/cheshire_zc706.runs/impl_1/cheshire_soc_wrap.bit"
}

current_hw_device [get_hw_devices xc7z045_1]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices xc7z045_1] 0]
set_property PROBES.FILE {} [get_hw_devices xc7z045_1]
set_property FULL_PROBES.FILE {} [get_hw_devices xc7z045_1]
set_property PROGRAM.FILE $bitstream_file [get_hw_devices xc7z045_1]
program_hw_devices [get_hw_devices xc7z045_1]
refresh_hw_device [lindex [get_hw_devices xc7z045_1] 0]

close_hw_manager
