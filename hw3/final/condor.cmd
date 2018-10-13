universe        	= vanilla
executable      	= hw3_parser.sh
getenv          	= true
output				= condor.out
error           	= condor.err
log             	= condor.log
#notification		= complete
arguments       	= "'/dropbox/18-19/571/hw3/grammar_cnf.cfg' '/dropbox/18-19/571/hw3/sentences.txt' 'grammar_cnf_output.txt'"
transfer_executable	= false
#request_cpus		= 8
queue
