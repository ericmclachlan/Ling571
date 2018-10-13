#!/bin/sh

# Usage: 
#	hw1_parse.sh <GRAMMAR_FILE> <TEST_SENTENCE_FILE> <OUTPUT_FILE>

# Parameters:
#	$1:	GRAMMAR_FILE:		The name of the file holding the grammar rules in the NLTK .cfg format.
#	$2:	TEST_SENTENCE_FILE:	The name of the file holding the set of sentences to parse, one sentence per line.
#	$3:	OUTPUT_FILE:		The name of output file for your system.

GRAMMAR_FILE=$1
TEST_SENTENCE_FILE=$2
OUTPUT_FILE=$3

echo "GRAMMAR_FILE: $GRAMMAR_FILE"
echo "TEST_SENTENCE_FILE: $TEST_SENTENCE_FILE"
echo "OUTPUT_FILE: $OUTPUT_FILE"

#set -x	# echo on
#time 
/usr/bin/env python3 source.py $GRAMMAR_FILE $TEST_SENTENCE_FILE > $OUTPUT_FILE
