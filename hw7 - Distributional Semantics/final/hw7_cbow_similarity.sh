#!/bin/sh
#
# Performs  parsing and compositional semantic analysis.

hw=hw7
exDir=/dropbox/18-19/571/$hw/


window=$1				# An integer specifying the size of the context window for your model. For a window value of 2, the window should span the two words before and the two words after the current word.
judgment_filename=$2	# The name of the input file holding human judgments of the pairs of words and their similarity to evaluate against, mc_similarity.txt.
output_filename=$3		# The name of the output file with the results of computing similarities and correlations over the word pairs.

# Set required hash seed variable
export PYTHONHASHSEED=1

/usr/bin/env python3 CbowSimilarity.py $window $judgment_filename > $output_filename

