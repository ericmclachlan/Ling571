universe        	= vanilla
executable      	= run.sh
getenv          	= true
output				= condor.out
error           	= condor.err
log             	= condor.log
#notification		= complete
arguments       	= "'grammar.cfg' '/dropbox/18-19/571/hw9/coref_sentences.txt' 'hw9_output.txt'"
transfer_executable	= false
#request_cpus		= 8
queue
