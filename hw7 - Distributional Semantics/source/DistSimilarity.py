import argparse
import nltk
import sys

        
def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description='Computes similarities and correlations over word pairs.')
    parser.add_argument('window', type=int, help='An integer specifying the size of the context window for your model. '
        + 'For a window value of 2, the window should span the two words before and the two words after the current word.')
    parser.add_argument('weighting', type=str, help='A string specifying the weighting scheme to apply: "FREQ" or "PMI", where: '
        + ' FREQ: Refers to "term frequency", the number of times the word appeared in the context of the target'
        + ' PMI: (Positive) Point-wise Mutual Information: A variant of PMI where negative association scores are removed.')
    parser.add_argument('judgment_filename', type=str, help='The name of the input file holding human judgments of the pairs of words and their similarity to evaluate against, mc_similarity.txt.', default=None)
    args = parser.parse_args()
    eprint(args)
    
    # Load the reference reference material.
    with open(args.judgment_filename, "r") as f:
        lines = f.readlines()


    eprint('Operation Complete.')


def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)
    pass


if __name__ == "__main__":
    main()
