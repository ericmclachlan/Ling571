universe        	= vanilla
executable      	= hw4_run.sh
getenv          	= true
output				= condor.out
error           	= condor.err
log             	= condor.log
#notification		= complete
arguments       	=  "'/dropbox/18-19/571/hw4/data/parses.train' \
						'hw4_trained.pcfg' \
						'/dropbox/18-19/571/hw4/data/sentences.txt'  \
						'parses_base.out' \
						'hw4_trained.pcfg' \
						'parses_improved.out' \
						'parses_base.eval'  \
						'parses_improved.eval'"
transfer_executable	= false
#request_cpus		= 8
queue
