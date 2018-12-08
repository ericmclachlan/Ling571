"""
Hw9: An Exploration of Hobbs Algorithm.
"""

import argparse
import nltk
import re
import sys


class Hobbs():
    """Explores the Hobbs algorithm for pronomial anaphora resolution."""

    def __init__(self):
        self.gender = { 'he': 'm', 'she': 'f', 'his': 'm', 'her': 'f'}


    def run(self, input_grammar_filename: str, test_sentence_filename: str):
        """Runs this command."""
 
        # 1. Read in your grammar.
        with open(input_grammar_filename, "r") as f:
            grammar_as_text = f.read()
        #grammar = nltk.CFG.fromstring(grammar_as_text)
        #parser = nltk.EarleyChartParser(grammar)
        grammar = nltk.grammar.FeatureGrammar.fromstring(grammar_as_text)
        parser = nltk.parse.FeatureEarleyChartParser(grammar, trace=0)

        # 2. Read in the file of sentence pairs with pronouns to resolve.
        with open(test_sentence_filename, "r") as file_stream:
            lines = file_stream.readlines()

        # 3. For each (pronoun, sentence pair) set:
        line_no = 0
        while line_no < len(lines):
            line1 = lines[line_no].strip()
            line2 = lines[line_no + 1].strip()
            eprint(line1)
            eprint(line2)
            
            # 3.a. Parse the sentences with your grammar.
            s_0 = nltk.tree.ParentedTree.convert(parser.parse_one(nltk.word_tokenize(line1)))
            s_1 = nltk.tree.ParentedTree.convert(parser.parse_one(nltk.word_tokenize(line2)))
            pronouns_productions = grammar.productions(lhs=nltk.grammar.FeatStructNonterminal('PRP'))
            for pronoun_production in pronouns_productions:
                leaf_values = s_1.leaves()
                pronoun = pronoun_production.rhs()[0]
                if pronoun not in leaf_values:
                    continue
                
                # 3.b. Print out the pronoun and the corresponding parses.
                print('{} {} {}'.format(pronoun, \
                    #parse1, parse2
                    s_0.pformat(margin=float("inf")).replace('[]', ''), \
                    s_1.pformat(margin=float("inf")).replace('[]', '') \
                                        ))

                pronoun_index = leaf_values.index(pronoun)
                #pronoun_node = s_1.pos()[pronoun_index]
                tree_location = s_1.leaf_treeposition(pronoun_index)
                pronoun_node = s_1[tree_location[0:-1]]

                #for node in s_1:
                #    label = nltk.grammar.FeatStructNonterminal(node.label())
                #    if pronoun_production == label[nltk.featstruct.Feature('type')]:
                #        pronoun_node = label
                #        break

                # 3.c. Use the Hobbs algorithm to (attempt to) resolve the pronoun in the context.
                is_accepted = False
                for antecedent in self.get_hobbs_nominees(pronoun_node, [s_0, s_1]):
                    # 3.c.i) Identify each parse tree node corresponding to 'X' in the algorithm, 
                    # writing out the corresponding NP or S (or SBAR) constituent.
                    print(antecedent)
                    
                    # 3.c.ii) Identify each node proposed as an antecedent.
                    # 3.c.iii) Reject any proposed node ruled out by agreement.
                    reason_for_failure = self.check_agreement(pronoun_node, antecedent)

                    if reason_for_failure is None:
                        print('Accept')
                        is_accepted = True
                        break
                if not is_accepted:
                    print('Reject - {}', reason_for_failure)
                print('--> Correct? Incorrect? Why? Which syntactic and semantic preferences are required?')
                    
            line_no += 3

        eprint('Done.')

    def get_hobbs_nominees(self, pronoun, sentences: []):
        yield pronoun


        return

    def check_agreement(self, pronoun, antecedent):
        """Performs agreement checks beween the pronoun and the proposed antecedent."""
        
        # Input Validation:
        if not pronoun or not antecedent:
            #assert False
            return None

        pronoun_agr = nltk.grammar.FeatStructNonterminal(pronoun.label())['NUM']
        antecedent_agr = nltk.grammar.FeatStructNonterminal(antecedent.label())['NUM']
        
        # Number check:
        if pronoun_agr != antecedent_agr:
        #if not antecedent_agr.subsumes(pronoun_agr):
            return 'number'
        
        # Gender check:
        
        # Person check (?):

        return None


def main():
    """The main method."""

    # Parse the command line arguments.
    parser = argparse.ArgumentParser( \
        description='Explores the Hobbs algorithm.')
    parser.add_argument('input_grammar_filename', type=str, \
        help='The name of the file that holds the grammar to be used to parse the sentences.')
    parser.add_argument('test_sentence_filename', \
        help='The name of the file that holds the pairs of sentences that form contexts for pronoun resolution. ' + \
        'Each sentence appears on a line by itself, with a blank between pairs of sentences.')
    args = parser.parse_args()
    eprint(args)

    command = Hobbs()
    command.run(args.input_grammar_filename, args.test_sentence_filename)


def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)
    pass


if __name__ == "__main__":
    main()
