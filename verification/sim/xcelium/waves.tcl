database -open waves -default
probe -create tb_cheshire_soc -all -memories -variables -depth all
run 1000000000ns
exit
