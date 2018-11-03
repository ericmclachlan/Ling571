universe        	= vanilla
executable      	= hw6_run.sh
getenv          	= true
output				= condor.out
error           	= condor.err
log             	= condor.log
#notification		= complete
arguments       	=  "'hw6_semantic_grammar.fcfg' \
						'/dropbox/18-19/571/hw4/data/sentences.txt'  \
						'hw6_output.txt'"
transfer_executable	= false
#request_cpus		= 8
queue
