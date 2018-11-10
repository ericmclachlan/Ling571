import nltk
import string
import sys

from scipy.stats.stats import spearmanr

class ASimilarity(object):
    """A base class for common logic related to calcuting similarity."""
    
    window = -1
    words = None

    def __init__(self, window: int):
        self.window = window

        nltk.download('brown')
        eprint('Reading Browns corpus...')
        raw_words = nltk.corpus.brown.words()

        eprint('Performing preprocessing...')
        self.words = self.preprocess(raw_words)

        
    def preprocess(self, raw_words):
        words = []
        for raw_word in raw_words:
            #eprint(raw_word)
            # Remove punctuation:
            raw_word = raw_word.translate(str.maketrans("","", string.punctuation))
            if len(raw_word) > 0:
                # Add the lowercase equivalent of this non-punctuation word to the sentence.
                raw_word = raw_word.lower()
                words.append(raw_word)
            #    eprint(raw_word)
            #eprint()
        return [ words ]
    

    def run(self, judgement_file: str):
        # Load the reference reference material.
        eprint('Reading judgement file...')
        with open(judgement_file, "r") as f:
            lines = f.readlines()
        left_list = []
        right_list = []
        calculated_similarity_list = []
        similarity_wordvec_list = []
        i = 0
        eprint('Generating output...')
        for line in lines:
            components = line.split(',')

            left = components[0].strip()
            right = components[1].strip()
            correlation_gold = float(components[2].strip())

            left_list.append(left)
            right_list.append(right)
            calculated_similarity_list.append(correlation_gold)
        
            #eprint('{},{},{}'.format(left, right, correlation_gold) + '*')
            #try:
            similarity = self.calculate_similarity(left, right)
            #except KeyError:
            #    similarity = 0

            similarity_wordvec_list.append(similarity)

            print('{},{},{}'.format(left, right, similarity))
            #eprint('{},{},{}'.format(left, right, similarity))

            i += 1

        # Measure the Correlation:
        result = spearmanr(calculated_similarity_list, similarity_wordvec_list)

        print('correlation:' + str(result.correlation))
        eprint('Operation Completed Successfully.')
    

def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)
    pass