#!/bin/sh
#
# This is the job that will be submitted to condor.

hw=hw4
exDir=/dropbox/18-19/571/$hw
toolsDir=/dropbox/18-19/571/$hw/tools
dataDir=/dropbox/18-19/571/$hw/data
echo "Examples directory: $exDir"

# -------
# hw4_ec
# -------

treebank_filename=$1				# parses.train			: The name of the file holding the parsed sentences, one parse per line, in Chomsky Normal Form.
output_PCFG_file=$2					# hw4_trained.pcfg		: The name of the file where the induced grammar should be written.
test_sentence_filename=$3			# sentences.txt			: The name of the file holding the test sentences to be parsed.
baseline_parse_output_filename=$4	# parses_base.out		: Output parses from your baseline PCFG parser
input_PCFG_file=$5					# hw4_trained.pcfg      : The name of the file holding the induced PCFG grammar to be read.
baseline_eval=$6					# parses_base.eval		: evalb output for your baseline parses


# 1. Deduce a CFG grammar based on the parses included in the $treebank_filename:
./hw4_topcfg_oov.sh $treebank_filename 0.1 $output_PCFG_file


# 2. Perform PCKY Parsing:
./hw4_parser.sh $input_PCFG_file $test_sentence_filename $baseline_parse_output_filename


# 3. Evaluating the PCKY Parser:
$toolsDir/evalb -p $toolsDir/COLLINS.prm $dataDir/parses.gold $baseline_parse_output_filename > $baseline_eval



