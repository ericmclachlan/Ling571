#!/bin/sh
#
# Implements and evaluates WordNet-based word sense disambiguation algorithm based on Resnik's approach.

hw=hw9
exDir=/dropbox/18-19/571/$hw/


information_content_file_type=$1	# The source of the information content file.
wsd_test_filename=$2				# The name of the file that contains the lines of "probe-word, noun group words" pairs on which to evaluate your system.
judgment_file=$3					# The name of the input file holding human judgments of the pairs of words and their similarity to evaluate against.
output_filename=$4					# The name of the file to which you should write your results.

echo /usr/bin/env python3 Hobbs.py $information_content_file_type $wsd_test_filename $judgment_file > $output_filename
/usr/bin/env python3 Hobbs.py $information_content_file_type $wsd_test_filename $judgment_file > $output_filename

