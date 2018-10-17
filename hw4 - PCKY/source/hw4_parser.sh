#!/bin/sh
#
# Code implementing PCKY.

hw=hw4
exDir=~/dropbox/18-19/571/$hw/
echo "Examples directory: $exDir"

# -------
# hw4: 2
# -------

input_PCFG_file=$1
test_sentence_filename=$2
output_parse_filename=$3

# Use the PCFG to return the most probable parse for each sentence in $test_sentence_filename.
/usr/bin/env python3 PcnfParser.py $input_PCFG_file $test_sentence_filename > $output_parse_filename

