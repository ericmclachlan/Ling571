universe        	= vanilla
executable      	= hw5_parser.sh
getenv          	= true
output				= condor.out
error           	= condor.err
log             	= condor.log
#notification		= complete
arguments       	=  "'hw5_feature_grammar.fcfg' \
						'/dropbox/18-19/571/hw5/sentences.txt' \
						'hw5_output.txt'"
transfer_executable	= false
#request_cpus		= 8
queue
