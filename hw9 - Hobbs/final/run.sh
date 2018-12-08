#!/bin/sh
#
# Generates the output required for hw9 submission.

hw=hw9
exDir=~/dropbox/18-19/571/$hw

input_grammar_filename=$1
test_sentence_filename=$2
output_filename=$3

./hw9_coref.sh $input_grammar_filename $test_sentence_filename $output_filename
