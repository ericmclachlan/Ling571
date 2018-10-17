#!/bin/sh
#
# Code implementing PCKY.

hw=hw4
exDir=~/dropbox/18-19/571/$hw/
echo "Examples directory: $exDir"

# --------
# hw4: 2.1
# --------

input_PCFG_file=$1
test_sentence_filename=$2
output_parse_filename=$3

# This is the important part: Create a CNF grammar from the original Atis grammar.
#/usr/bin/env python3 CnfParser.py $exDir/atis.cfg > hw4_grammar_cnf.cfg
/usr/bin/env python3 ToPcky.py $input_PCFG_file $test_sentence_filename > $output_parse_filename

