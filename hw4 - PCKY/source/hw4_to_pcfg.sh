#!/bin/sh
#
# This is the job that will be submitted to condor.

hw=hw4
exDir=~/dropbox/18-19/571/$hw/
echo "Examples directory: $exDir"

# -------
# hw4: 1
# -------

treebank_filename=$1				# The name of the file holding the parsed sentences, one parse per line, in Chomsky Normal Form.
output_PCFG_file=$2					# The name of the file where the induced grammar should be written.

# Induce a PCFG grammar from the CNF parses.
/usr/bin/env python3 ToPcfg.py $treebank_filename > $output_PCFG_file

