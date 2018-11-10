#!/bin/sh
#
# Performs  parsing and compositional semantic analysis.

hw=hw7
exDir=/dropbox/18-19/571/$hw/


window=$1				# An integer specifying the size of the context window for your model. For a window value of 2, the window should span the two words before and the two words after the current word.
weighting=$2			# A string specifying the weighting scheme to apply: "FREQ" or "PMI", where:
						# 	FREQ: Refers to "term frequency", the number of times the word appeared in the context of the target
						# 	PMI: (Positive) Point-wise Mutual Information: A variant of PMI where negative association scores are removed.
judgment_filename=$3	# The name of the input file holding human judgments of the pairs of words and their similarity to evaluate against, mc_similarity.txt.
output_filename=$4		# The name of the output file with the results of computing similarities and correlations over the word pairs.

/usr/bin/env python3 DistSimilarity.py $window $weighting $judgment_filename > $output_filename

