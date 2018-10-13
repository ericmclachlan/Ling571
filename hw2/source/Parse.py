import argparse
import nltk
import os

class Parse:
    """A parser that processes sentences acccording to the rules of a specified grammar."""

    def parse(self, grammar_file_path, sentence_filePath):
        """Parses the sentences found in sentence_filePath using the grammar found in grammar_filePath."""
    
        # Load the grammar using NLTK:
        grammar_file_path = os.path.abspath(grammar_file_path)
        rules = nltk.data.load(grammar_file_path, 'text')
        grammar = nltk.CFG.fromstring(rules)

        # Load the parser using NLTK:
        parser = nltk.parse.EarleyChartParser(grammar)

        # Iterate over each of the sentences in the sentences file,
        # writing the number of parses for each sentence:
        sentence_file = open(sentence_filePath, "r")
        lines = sentence_file.readlines()
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

        sentence_file.close()


def main():
    """Calls parse with the parameters passed on the command line."""

    parser = argparse.ArgumentParser(description='Parses the specified sentences using the specified grammar.')
    parser.add_argument('grammar_file', type=str, help='the name of the file containing the grammar.')
    parser.add_argument('sentence_file', type=str, help='the name of the file containing the sentences.')
    ns = parser.parse_args()

    # Input Validation:
    parse = Parse()
    parse.parse(ns.grammar_file, ns.sentence_file)
    

if __name__ == "__main__":
    main()
