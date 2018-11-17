#!/bin/sh
#
# Generates the output required for hw8 submission.

hw=hw8
exDir=~/dropbox/18-19/571/$hw

information_content_file_type="nltk"
wsd_test_filename="$exDir/wsd_contexts.txt"
judgment_filename="$exDir/mc_similarity.txt"
output_filename="hw8_output.txt"

./hw8_resnik_wsd.sh $information_content_file_type $wsd_test_filename $judgment_filename $output_filename
