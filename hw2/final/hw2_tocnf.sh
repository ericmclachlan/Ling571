#!/bin/sh
#
# This is the job that will be submitted to condor.

hw=hw2
exDir=~/dropbox/18-19/571/$hw/
echo "Examples directory: $exDir"

# -------
# Hw2
# -------

INPUT_GRAMMAR_FILE=$1
OUTPUT_GRAMMAR_FILE=$2

# Parse the original Atis grammar.
# /usr/bin/env python3 Parse.py $exDir/atis.cfg $exDir/sentences.txt > hw2_orig_output.txt
# cat hw2_orig_output.txt

# This is the important part: Create a CNF grammar from the original Atis grammar.
#/usr/bin/env python3 ConvertToCNF.py $exDir/atis.cfg > hw2_grammar_cnf.cfg
/usr/bin/env python3 ConvertToCNF.py $INPUT_GRAMMAR_FILE > $OUTPUT_GRAMMAR_FILE
# cat hw2_grammar_cnf.cfg

# Parse the CNF Atis grammar.
# /usr/bin/env python3 Parse.py hw2_grammar_cnf.cfg $exDir/sentences.txt > hw2_cnf_output.txt
# cat hw2_cnf_output.txt
