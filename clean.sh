#!/bin/sh

hw=hw5
exDir=~/dropbox/18-19/571/$hw/

# Remove files generated by all projects.
rm -fv condor.log
rm -fv condor.out
rm -fv condor.err
rm -fv snippets.sh
rm -fv hw*.tar.gz


# Remove folders generated by this project:
# for f in $(cat $exDir\submit-file-list); 
# do 
  # if [ ${f: -3} != ".sh" ]
  # then 
	# rm -- "$f"
  # else
	# echo "Leaving $f"
  # fi
# done

# Remove files generated by this project:
rm -fv hw5_output.txt
