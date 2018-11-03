#!/bin/sh
#
# Performs  parsing and compositional semantic analysis.

hw=hw6
exDir=/dropbox/18-19/571/$hw/


input_grammar_filename=$1		# The name of the file holding the grammar with FOL semantic attachments that you created to implement the rule-to-rule style compositional semantic analysis.
input_sentences_filename=$2		# The name of the file holding the sentences to parse and perform semantic analysis on.
output_filename=$3				# The name of the file to write the results of your automatic semantic analysis.

/usr/bin/env python3 SemanticFcfgParser.py $input_grammar_filename $input_sentences_filename > $output_filename

