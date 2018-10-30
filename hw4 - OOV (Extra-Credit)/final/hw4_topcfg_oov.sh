#!/bin/sh
#
# This is the job that will be submitted to condor.

# -------
# hw4_ec
# -------

treebank_filename=$1				# The name of the file holding the parsed sentences, one parse per line, in Chomsky Normal Form.
hide_proportion=$2					# A float between 0 and 1 that changes the amount of words to replace with the <UNK> tag.
output_PCFG_file=$3					# The name of the file where the induced grammar should be written.

# Induce a PCFG grammar from the CNF parses.
/usr/bin/env python3 ToPcfg.py $treebank_filename $hide_proportion > $output_PCFG_file

