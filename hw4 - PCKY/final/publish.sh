#!/bin/sh

hw=hw4
exDir=~/dropbox/18-19/571/$hw
>&2 echo "Examples directory: $exDir"

tarFile=$hw.tar.gz

# Removes files:
rm -fv condor.log
rm -fv condor.out
rm -fv condor.err
rm -fv snippets.sh

# Zip it!
tar -czf $tarFile .

# Validation
bash $exDir/check_$hw.sh $tarFile
