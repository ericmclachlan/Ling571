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
TEST_SENTENCE_FILENAME=$2
OUTPUT_GRAMMAR_FILE=$3

# This is the important part: Create a CNF grammar from the original Atis grammar.
#/usr/bin/env python3 CnfParser.py $exDir/atis.cfg > hw2_grammar_cnf.cfg
/usr/bin/env python3 CnfParser.py $INPUT_GRAMMAR_FILE $TEST_SENTENCE_FILENAME > $OUTPUT_GRAMMAR_FILE

