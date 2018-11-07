#!/bin/sh
#
# Generates the output required for Hw7 submission.

hw=hw7
exDir=~/dropbox/18-19/571/$hw

./clean.sh

# Generate Similarity Files:

window[0]=2
window[1]=2
window[2]=10

weighting[0]=FREQ
weighting[1]=PMI
weighting[2]=PMI

judgement_file=$exDir/mc_similarity.txt

for i in 0 1 2 ; do
	
	./hw7_dist_similarity.sh "${window[$i]}" "${weighting[$i]}" $judgement_file "hw7_sim_${window[$i]}_${weighting[$i]}_output.txt"

done


# Generate CBOW Files:

window[0]=2

for i in 0 ; do

	./hw7_cbow_similarity.sh "${window[$i]}" $judgement_file "hw7_sim_${window[$i]}_CBOW_output.txt"

done
