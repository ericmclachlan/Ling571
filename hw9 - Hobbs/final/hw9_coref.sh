#!/bin/sh
#
# Implements and evaluates WordNet-based word sense disambiguation algorithm based on Resnik's approach.

hw=hw9
exDir=/dropbox/18-19/571/$hw/

input_grammar_filename=$1
test_sentence_filename=$2
output_filename=$3

/usr/bin/env python3 Hobbs.py $input_grammar_filename $test_sentence_filename > $output_filename

