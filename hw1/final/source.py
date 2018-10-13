import sys

# Input Validation:
if len(sys.argv) != 3:
    print('Invalid number of arguments.')
    print(str(sys.argv))
    exit()

grammarFilePath = sys.argv[1];
sentenceFilePath = sys.argv[2];

# Load the grammar using NLTK:
import nltk
rules = nltk.data.load('file://' + grammarFilePath, 'text')
grammar = nltk.CFG.fromstring(rules)

# Load the parser using NLTK:
parser = nltk.parse.EarleyChartParser(grammar)

# Iterate over each of the sentences in the sentences file,
# writing the number of parses for each sentence:
sentenceFile = open(sentenceFilePath, "r")
lines = sentenceFile.readlines()
totalNoOfParses = 0
for line in lines:
    noOfParses = 0
    tokens = nltk.word_tokenize(line)
    print(line, end="")
    for interpretation in parser.parse(tokens):
        print(interpretation)
        noOfParses = noOfParses + 1
    print('Number of parses:', noOfParses)
    print()
    totalNoOfParses = totalNoOfParses + noOfParses

print('Average parses per sentence:', totalNoOfParses / len(lines))

sentenceFile.close()

