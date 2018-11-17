import argparse
import nltk
import sys

from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import information_content
from scipy.stats.stats import spearmanr


class WordSenseDisambiguator(object):
    """Computes similarities and correlations over word pairs."""

    model = None
    brown_ic = None

    def __init__(self):
        # Download the wordnet library:
        nltk.download('wordnet', quiet=True)
        # Download the information content for the Brown corpus:
        nltk.download('wordnet_ic', quiet=True)
        self.brown_ic = nltk.corpus.wordnet_ic.ic('ic-brown-resnik-add1.dat')


    def run(self, wsd_test_filename: str, judgment_filename: str):
        
        eprint("Simple Tests: Starting ...")
        eprint("--------------------------")

        eprint(wordnet.synsets('artifact', pos='n'))
        eprint(wordnet.synsets('artifact', pos='n')[0].name())

        artifact = wordnet.synset('artifact.n.01')
        eprint(information_content(artifact, self.brown_ic))

        # Hypernyms:
        eprint(wordnet.synsets('artifact', pos='n')[0].hypernyms())

        # Common hypernyms:
        hat = wordnet.synsets('hat', pos='n')[0]
        glove = wordnet.synsets('glove', pos='n')[0]
        eprint(hat.common_hypernyms(glove))
        
        eprint("Simple Tests: Completed.")
        eprint("--------------------------")

        # Load the reference reference material.
        eprint('Reading judgement file...')
        with open(judgment_filename, "r") as f:
            lines = f.readlines()

        left_list = []
        right_list = []
        calculated_similarity_list = []
        gold_similarity_list = []
        eprint('Generating output...')
        for line in lines:
            components = line.split(',')

            left = components[0].strip()
            right = components[1].strip()
            correlation_gold = float(components[2].strip())

            left_list.append(left)
            right_list.append(right)
            gold_similarity_list.append(correlation_gold)

            calculated_similarity = self.calculate_similarity(left, right)
            calculated_similarity_list.append(calculated_similarity)

            print('{},{},{}'.format(left, right, calculated_similarity))

        # Measure the Correlation:
        result = spearmanr(calculated_similarity_list, gold_similarity_list, nan_policy='omit')

        print('correlation:' + str(result.correlation))
        eprint('Operation Completed.')
    

    def calculate_similarity(self, left: str, right: str) -> float:
        left_synsets = wordnet.synsets(left, pos='n')
        #eprint(left_synsets)
        right_synsets = wordnet.synsets(right, pos='n')
        #eprint(right_synsets)
        # Cheat: Test using the built-in Resnik similarity function.
        max_similarity = None
        for left_synset in left_synsets:
            for right_synset in right_synsets:
                calculated_similarity = wordnet.res_similarity(left_synset, right_synset, self.brown_ic)
                if max_similarity is None or calculated_similarity > max_similarity:
                    max_similarity = calculated_similarity
        return max_similarity


def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description='Computes similarities and correlations over word pairs.')
    parser.add_argument('information_content_file_type', type=str, choices=['nltk', 'myic'], \
        help='Specify the source of the information content file.')
    parser.add_argument('wsd_test_filename', \
        help='The name of the file that contains the lines of "probe-word, noun group words" pairs.')
    parser.add_argument('judgment_filename', \
        help='The input file holding human judgments of the pairs of words and their similarity to evaluate against.')
    args = parser.parse_args()
    eprint(args)

    command = WordSenseDisambiguator()
    command.run(args.wsd_test_filename, args.judgment_filename)

    
def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)
    pass


if __name__ == "__main__":
    main()
