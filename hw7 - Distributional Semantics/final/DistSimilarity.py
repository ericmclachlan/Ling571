import argparse
import math
import nltk
import sys

from ASimilarity import ASimilarity
from CollocationMatrix import CollocationMatrix

class DistributionalSimilarity(ASimilarity):
    
    matrix = None

    def __init__(self, window: int):
        super().__init__(window)

        eprint('Generating CollocationMatrix...')
        self.matrix = CollocationMatrix()

        i = 0
        for w_1 in self.words:
            assert self.words[i] == w_1
            # Increment the count of words we've seen.
            for j in range(-self.window, self.window+1):
                # Skip counting the word itself.
                if j == 0:
                    continue
                
                # At the beginning and end of the sentence,
                # you can either skip counting, or add a
                # unique "<START>" or "<END>" token to indicate
                # the word being colocated at the beginning or
                # end of sentences.
                if 0 < i+j < len(self.words):
                    w_2 = self.words[i+j]
                
                    self.matrix.add_pair(w_1, w_2)                
            i += 1
        
    def calculate_similarity(self, w1: str, w2: str):
        w1_id = self.matrix.word_id(w1)
        w2_id = self.matrix.word_id(w2)

        if w1_id is None or w2_id is None:
            return 0

        sumOfASquared = 0
        sumOfBSquared = 0
        sumOfTheProducts = 0

        # Iterate over each of the words that collocate with w1. (w1 is chosen arbitrarilly).
        row_dictionary_w1 = {}
        row_dictionary_w2 = {}
        for current_id in self.matrix[w1_id].keys():
            count_of_w1_with_current = self.get_weight(w1_id, current_id)
            row_dictionary_w1[self.matrix._id_mapping[current_id]] = count_of_w1_with_current
            assert w2_id in self.matrix
            if current_id in self.matrix[w2_id]:
                count_of_w2_with_current = self.get_weight(w2_id, current_id)
                row_dictionary_w2[self.matrix._id_mapping[current_id]] = count_of_w2_with_current
                sumOfASquared += count_of_w1_with_current * count_of_w1_with_current
                sumOfBSquared += count_of_w2_with_current * count_of_w2_with_current
                sumOfTheProducts += (count_of_w1_with_current * count_of_w2_with_current);
                
        sorted_list_w1 = sorted(row_dictionary_w1, key=row_dictionary_w1.get, reverse=True)
        print(w1+':', end='')
        for i in range(min(10, len(row_dictionary_w1))):
            word = sorted_list_w1[i]
            print(' {}:{}'.format(word, row_dictionary_w1[word]), end='')
        print()

        sorted_list_w2 = sorted(row_dictionary_w2, key=row_dictionary_w2.get, reverse=True)
        print(w2+':', end='')
        for i in range(min(10, len(row_dictionary_w2))):
            word = sorted_list_w2[i]
            print(' {}:{}'.format(word, row_dictionary_w2[word]), end='')
        print()

        result = sumOfTheProducts / math.sqrt(sumOfASquared * sumOfBSquared)
        return result
        
    def get_weight(self, w1_id: int, w2_id: int):
        assert False

class FreqSimilarity(DistributionalSimilarity):
    
    def get_weight(self, w1_id, w2_id):
        weight = self.matrix[w1_id][w2_id]
        return weight
        

class PmiSimilarity(DistributionalSimilarity):
    
    def get_weight(self, w1_id, w2_id):
        w1 = self.matrix._id_mapping[w1_id]
        w2 = self.matrix._id_mapping[w2_id]
        total_contexts = self.matrix.total_sum
    
        p_w = self.matrix.get_row_sum(w1) / total_contexts
        p_f = self.matrix.get_col_sum(w2) / total_contexts

        p_joint = self.matrix.get_pair(w1, w2) / total_contexts

        p_marginal = p_w * p_f

        if p_marginal == 0:
            return math.nan
        elif p_joint == 0:
            return 0
        else:
            return max(0, math.log(p_joint / p_marginal))
                             

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
    
    if args.weighting == 'FREQ':
        similarity_engine = FreqSimilarity(args.window)
    elif args.weighting == 'PMI':
        similarity_engine = PmiSimilarity(args.window)
    else:
        assert False

    similarity_engine.run(args.judgment_filename)
    
    #eprint("{},{},{}".format('grand', 'jury', similarity_engine.calculate_similarity('grand', 'jury')))
    #eprint("{},{},{}".format('jury', 'fulton', similarity_engine.calculate_similarity('jury', 'fulton')))


def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)
    pass


if __name__ == "__main__":
    main()
