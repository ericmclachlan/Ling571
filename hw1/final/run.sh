#!/bin/sh
#
# This is the job that will be submitted to condor.

exDir=~/dropbox/18-19/571/hw1/
echo "Examples directory: $exDir"

# -------
# Hw1: Q1
# -------

./hw1_parse.sh $exDir/grammar.cfg $exDir/sentences.txt hw1_parse.out
cat hw1_parse.out