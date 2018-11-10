import argparse
import gensim
import nltk
import sys
import re
import string

from scipy.stats.stats import spearmanr
from typing import List

        
def __preprocess_to_lowercase_and_remove_punctuation(raw_sents):
    sents = []
    for raw_sent in raw_sents:
        eprint(' '.join(raw_sent))
        sent = []
        for raw_word in raw_sent:
            # Remove punctuation:
            raw_word = raw_word.translate(str.maketrans("","", string.punctuation))
            if len(raw_word) > 0:
                # Add the lowercase equivalent of this non-punctuation word to the sentence.
                sent.append(raw_word.lower())
        sents.append(sent)
        eprint (' '.join(sent))
    return sents

def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description='Computes similarities and correlations over word pairs.')
    parser.add_argument('window', type=int, help='An integer specifying the size of the context window for your model. '
        + 'For a window value of 2, the window should span the two words before and the two words after the current word.')
    parser.add_argument('judgment_filename', type=str, help='The name of the input file holding human judgments of the pairs of words and their similarity to evaluate against, mc_similarity.txt.', default=None)
    args = parser.parse_args()
    eprint(args)

    nltk.download('brown')
    eprint('Reading Browns corpus...')
    raw_sents = nltk.corpus.brown.sents()
    eprint('Preprocessing...')
    sents = __preprocess_to_lowercase_and_remove_punctuation(raw_sents)
    eprint('Generating gensim Word2Vec model...')
    model = gensim.models.Word2Vec(sents, size=100, window=args.window, min_count=1, workers=1)
    
    # Load the reference reference material.
    eprint('Reading judgement file...')
    with open(args.judgment_filename, "r") as f:
        lines = f.readlines()
    left_list = []
    right_list = []
    similarity_gold_list = []
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
        similarity_gold_list.append(correlation_gold)
        
        eprint('{},{},{}'.format(left, right, correlation_gold) + '*')

        similarity_wordvec = model.wv.similarity(left, right)
        similarity_wordvec_list.append(similarity_wordvec)

        print('{},{},{}'.format(left, right, similarity_wordvec))
        eprint('{},{},{}'.format(left, right, similarity_wordvec))

        i += 1

    correlation_result = spearmanr(similarity_wordvec_list, similarity_gold_list)
    print('correlation:' + str(correlation_result.correlation))
    eprint('Operation Completed Successfully.')


def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)
    pass


if __name__ == "__main__":
    main()
