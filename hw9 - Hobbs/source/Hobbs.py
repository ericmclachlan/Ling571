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
            leaves = s_1.leaves()
            for leaf in leaves:
                pronoun_production = grammar.productions(lhs=nltk.grammar.FeatStructNonterminal('PRP'), rhs=leaf)
                # Ignore non-pronouns
                if pronoun_production is None or len(pronoun_production) == 0:
                    continue

                assert len(pronoun_production) == 1
                pronoun = pronoun_production[0].rhs()[0]
                if pronoun not in leaves:
                    continue
                
                # 3.b. Print out the pronoun and the corresponding parses.
                print('{} {} {}'.format(pronoun,
                    pretty_format(s_0),
                    pretty_format(s_1)))

                pronoun_index = leaves.index(pronoun)
                tree_location = s_1.leaf_treeposition(pronoun_index)
                pronoun_node = s_1[tree_location[0:-1]]

                # 3.c. Use the Hobbs algorithm to (attempt to) resolve the pronoun in the context.
                is_accepted = False
                for proposed_antecedent in self.get_hobbs_proposed_antecedents(pronoun_node, [s_0, s_1]):
                    # 3.c.i) Identify each parse tree node corresponding to 'X' in the algorithm, 
                    # writing out the corresponding NP or S (or SBAR) constituent.
                    print(pretty_format(proposed_antecedent))
                    
                    # 3.c.ii) Identify each node proposed as an antecedent.
                    # 3.c.iii) Reject any proposed node ruled out by agreement.
                    reason_for_failure = self.check_agreement(pronoun_node, proposed_antecedent)

                    if reason_for_failure:
                        print('Reject - {}'.format(reason_for_failure))
                    else:
                        print('Accept')
                        is_accepted = True
                        break
                print('--> Correct? Incorrect? Why? Which syntactic and semantic preferences are required?')
                    
            line_no += 3

        eprint('Done.')


    def display_tree_graph(self, X):
        tree_as_text = pretty_format(X)
        tree = nltk.Tree.fromstring(tree_as_text)
        tree.pretty_print()

    def get_hobbs_proposed_antecedents(self, pronoun, sentences: []):
        p = []
        # 1. Begin at the noun phrase (NP) node immediately dominating the pronoun
        X = pronoun.parent()
        sentences.pop()

        # 2. Go up the tree to the first NP or sentence (S) node encountered. 
        # Call this node X, and call the path used to reach it p.
        p.append(X)
        X = X.parent()
        while not self.is_NP_or_S(X):
            p.append(X)
            X = X.parent()

        self.display_tree_graph(X)
        # 3. Traverse all branches below node X to the left of path p in a left-to-right, breadthfirst fashion. 
        # Propose as the antecedent any encountered NP node that has an NP or S node between it and X.
        stack = []
        for child in X:
            # Process items to the left of path p:
            if not child in p:
                stack.append(child)
            # Don't process items to the right of path p:
            else:
                break

        # If node X is the highest S node in the sentence, 
        # traverse the surface parse trees of previous sentences in the text in order of recency, 
        # the most recent first; each tree is traversed in a left-to-right, breadth-first manner, and 
        # when an NP node is encountered, it is proposed as antecedent. 
        # If X is not the highest S node in the sentence, continue to step 5.
        if len(stack) == 0 and len(sentences) > 0:
            sentence = sentences.pop()
            X = None
            for child in sentence:
                stack.append(child)
            self.display_tree_graph(sentence)

        # TRAVERSE:
        while len(stack) > 0:
            item = stack.pop(0)
            for child in item:
                stack.insert(len(stack), child)
            
            if self.has_NP_or_S_between_self_and_X(item, X):
                yield item
            



        return

    def is_NP_or_S(self, X):
        POS = X.label()[nltk.featstruct.Feature('type')]
        return POS == 'S' or POS == 'NP'

    def has_NP_or_S_between_self_and_X(self, item, X):
        while item and item != X:
            if type(item) == str:
                # Ignore terminal symbols
                return False
            POS = item.label()[nltk.featstruct.Feature('type')]
            if POS == 'S' or POS == 'NP':
                return True
            elif X:
                item = item.parent()
            else:
                return False

        return False


    def check_agreement(self, pronoun, antecedent):
        """Performs agreement checks beween the pronoun and the proposed antecedent."""
        
        # Input Validation:
        if not pronoun or not antecedent:
            #assert False
            return None

        pronoun_agr = nltk.grammar.FeatStructNonterminal(pronoun.label())
        antecedent_agr = nltk.grammar.FeatStructNonterminal(antecedent.label())
        
        # Number check:
        if 'NUM' in pronoun_agr and 'NUM' in antecedent_agr and pronoun_agr['NUM'] != antecedent_agr['NUM']:
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


def pretty_format(tree):
    text = re.sub('\[[^]]*\]', '', tree.pformat(margin=float("inf")))
    return text

def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)
    pass


if __name__ == "__main__":
    main()
