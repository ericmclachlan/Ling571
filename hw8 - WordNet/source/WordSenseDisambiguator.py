"""
Hw8: Word-sense Disambiguation
"""

import argparse
import math
from typing import List
import sys
import nltk
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import information_content
from scipy.stats.stats import spearmanr


class WordSenseDisambiguator():
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
        """Runs this command."""

        self.__process_word_sense_disambiguation(wsd_test_filename)
        self.__process_human_judgement(judgment_filename)

        eprint('Done.')

    
    def wsim(self, left_synsets, right_synsets):
        """Calculates the highest information and the most_informative_subsumer (c)."""
        i = 0.0    # Information
        most_informative_left = None
        most_informative_right = None
        milcs = None
        for left_synset in left_synsets:
            for right_synset in right_synsets:
                (information, lcs) = self.sim(left_synset, right_synset)
                if information > i:
                    i = information
                    most_informative_left = left_synset
                    most_informative_right = right_synset
                    c = lcs
        return (i, milcs)


    def sim(self, c1, c2):
        """Find the most informative subsumer of these 2 concepts."""
        hypernyms = c1.common_hypernyms(c2)
        most_information = None
        most_informative_hypernym = None
        information = []
        for hypernym in hypernyms:
            hypernym_ic = information_content(hypernym, self.brown_ic)
            information.append(hypernym_ic)
            if most_information is None or hypernym_ic > most_information:
                most_information = hypernym_ic
                most_informative_hypernym = hypernym
        return (most_information, most_informative_hypernym)



    def __process_word_sense_disambiguation(self, wsd_test_filename):
        """Parses and handles the word-sense disambiguation aspect of the assignment."""
        
        eprint('Disambiguating...')

        with open(wsd_test_filename, "r") as file_stream:
            lines = file_stream.readlines()

        for line in lines:
            components = line.split('	')

            word = components[0].strip()
            probe_words = components[1].strip().split(',')

            best_left = None
            max_support = 0.0

            #(left_synset, similarity) = self.calculate_similarity(word, probe_words)
            all_senses_of_w = wordnet.synsets(word, pos='n')
            support = [0.0] * len(all_senses_of_w)
            for probe_word in probe_words:
                mi_p = 0.0
                for sense_w_i in range(len(all_senses_of_w)):
                    milcs = None   # Most Informative Lowest Common Subsumer
                    mi = 0.0       # Most Information
                    for sense_p in wordnet.synsets(probe_word, pos='n'):
                        sense_w = all_senses_of_w[sense_w_i]
                        # CUSTOM
                        (i, lcs) = self.sim(sense_w, sense_p)
                        # BUILTIN
                        #(i, lcs) = (wordnet.res_similarity(sense_w, sense_p, self.brown_ic), self.wsim([sense_p], [sense_w]))
                        if i > mi:
                            mi = i
                            milcs = lcs
                    support[sense_w_i] += mi
                    if mi > mi_p:
                        mi_p = mi
                print('({}, {}, {:.10f}) '.format(word, probe_word, mi_p), end='')
            max_support = max(support)
            sense_w_i = support.index(max_support)
            sense_w = all_senses_of_w[sense_w_i]

            print()
            if max_support is None:
                print()
            else:
                print(sense_w.name())

        eprint('Disambiguating: Complete.')


    def __process_human_judgement(self, judgment_filename):
        """Parses and handles the human judgement aspect of the assignment."""
        
        eprint('Judging ...')

        with open(judgment_filename, "r") as file_stream:
            lines = file_stream.readlines()

        calculated_similarity_list = []
        gold_similarity_list = []
        for line in lines:
            components = line.split(',')

            word = components[0].strip()
            right = components[1].strip()
            correlation_gold = float(components[2].strip())

            gold_similarity_list.append(correlation_gold)
            probe_words = [ right ]
            #(_, similarity) = self.calculate_similarity(word, probe_words)
            
            all_senses_of_w = wordnet.synsets(word, pos='n')
            support = [0.0] * len(all_senses_of_w)
            for sense_w_i in range(len(all_senses_of_w)):
                for probe_word in probe_words:
                    milcs = None   # Most Informative Lowest Common Subsumer
                    mi = 0.0       # Most Information
                    for sense_p in wordnet.synsets(probe_word, pos='n'):
                        sense_w = all_senses_of_w[sense_w_i]
                        # CUSTOM
                        (i, lcs) = self.sim(sense_w, sense_p)
                        # BUILTIN
                        #(i, lcs) = (wordnet.res_similarity(sense_w, sense_p, self.brown_ic), self.wsim([sense_p], [sense_w]))
                        if i > mi:
                            mi = i
                            milcs = lcs
                    support[sense_w_i] += mi
            max_support = max(support)
            sense_w_i = support.index(max_support)
            sense_w = all_senses_of_w[sense_w_i]

            calculated_similarity_list.append(max_support)
            print('{},{}:{}'.format(word, right, max_support))

        # Measure the correlation between the human judgements and the calculated similarities:
        result = spearmanr(calculated_similarity_list, gold_similarity_list, nan_policy='omit')

        print('Correlation:' + str(result.correlation))

        eprint('Judgement: Complete.')


def main():
    """The main method."""

    # Parse the command line arguments.
    parser = argparse.ArgumentParser( \
        description='Computes similarities and correlations over word pairs.')
    parser.add_argument('information_content_file_type', type=str, choices=['nltk', 'myic'], \
        help='Specify the source of the information content file.')
    parser.add_argument('wsd_test_filename', \
        help='The file containing the "probe, noun group" word-pairs.')
    parser.add_argument('judgment_filename', \
        help='The file holding human judgments of the pairs of words and their similarity.')
    args = parser.parse_args()
    eprint(args)

    command = WordSenseDisambiguator()
    command.run(args.wsd_test_filename, args.judgment_filename)


def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    main()
