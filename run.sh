#!/bin/sh
#
# Generates the output required for hw9 submission.

hw=hw9
exDir=~/dropbox/18-19/571/$hw

input_grammar_filename="$exDir/grammar.cfg"
test_sentence_filename="$exDir/coref_sentences.txt"
output_filename="hw9_output.txt"

./hw9_coref.sh $input_grammar_filename $test_sentence_filename > $output_filename
