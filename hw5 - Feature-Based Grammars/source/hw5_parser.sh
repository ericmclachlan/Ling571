#!/bin/sh
#
# Code implementing PCKY.

hw=hw5
exDir=/dropbox/18-19/571/$hw/
#echo "Examples directory: $exDir"


input_grammar_filename=$1		# The name of the file holding the feature-based grammar that you created to implement the necessary grammatical constraints.
input_sentence_filename=$2		# The name of the file holding the sentences to test for grammaticality and parse.
output_filename=$3				# The name of the file to write the results of your grammaticality parsing test.

/usr/bin/env python3 FcfgTester.py $input_grammar_filename $input_sentence_filename > $output_filename

