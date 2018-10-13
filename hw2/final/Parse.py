import argparse
import nltk
import os

class Parse:
    """A parser that processes sentences acccording to the rules of a specified grammar."""

    def parse(self, grammarFilePath, sentenceFilePath):
        """Parses the sentences found in sentenceFilePath using the grammar found in grammarFilePath."""
    
        # Load the grammar using NLTK:
        grammarFilePath = os.path.abspath(grammarFilePath)
        rules = nltk.data.load(grammarFilePath, 'text')
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


def main():
    """Calls parse with the parameters passed on the command line."""

    parser = argparse.ArgumentParser(description='Parses the specified sentences using the specified grammar.')
    parser.add_argument('grammarFile', type=str, help='the name of the file containing the grammar.')
    parser.add_argument('sentenceFile', type=str, help='the name of the file containing the sentences.')
    ns = parser.parse_args()

    # Input Validation:
    parse = Parse()
    parse.parse(ns.grammarFile, ns.sentenceFile)
    

if __name__ == "__main__":
    main()
