import argparse
import gensim
import sys

from typing import List
from ASimilarity import ASimilarity

class CbowSimilarity(ASimilarity):

    model = None

    def __init__(self, window: int):
        super().__init__(window)

        eprint('Generating gensim Word2Vec model...')
        self.model = gensim.models.Word2Vec([self.words], size=100, window=self.window, min_count=1, workers=1)

    def calculate_similarity(self, w_1: str, w_2: str):
        return self.model.wv.similarity(w_1, w_2)


def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description='Computes similarities and correlations over word pairs.')
    parser.add_argument('window', type=int, help='An integer specifying the size of the context window for your model. '
        + 'For a window value of 2, the window should span the two words before and the two words after the current word.')
    parser.add_argument('judgment_filename', type=str, help='The name of the input file holding human judgments of the pairs of words and their similarity to evaluate against, mc_similarity.txt.', default=None)
    args = parser.parse_args()
    eprint(args)

    similarity_engine = CbowSimilarity(args.window)
    similarity_engine.run(args.judgment_filename)

    
def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)
    pass


if __name__ == "__main__":
    main()
