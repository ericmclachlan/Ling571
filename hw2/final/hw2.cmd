universe        	= vanilla
executable      	= hw2_tocnf.sh
getenv          	= true
output				= condor.out
error           	= condor.err
log             	= condor.log
#notification		= complete
arguments       	= "'/dropbox/18-19/571/hw2/atis.cfg' 'hw2_grammar_cnf.cfg'"
transfer_executable	= false
#request_cpus		= 8
queue
