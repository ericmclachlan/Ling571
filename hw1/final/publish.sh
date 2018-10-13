#!/bin/sh

exDir=~/dropbox/18-19/571/hw1
echo "Examples directory: $exDir"

# Removes files:
rm -fv condor.log
rm -fv condor.out
rm -fv condor.err

# Zip it!
tar -czf hw1.tar.gz .

# Validation
bash $exDir/check_hw1.sh $exDir/submit-file-list
