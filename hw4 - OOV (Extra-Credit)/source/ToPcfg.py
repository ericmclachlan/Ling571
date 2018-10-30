import argparse
import nltk
import operator
import sys

class ToPcfg(object):
    """Loads example sentences with POS word tags and induces a PCFG from those rules."""
    
    count_per_production = {}
    lhs_count = {}
    count_per_token = {}
    token_count = 0
    start_symbol = None
    hide_proportion = 0.0
    probability_per_production = {}

    def __init__(self, treebank_filename : str, hide_proportion: float):
        self.hide_proportion = hide_proportion
        # Iterate over each of the sentences in the sentences file,
        # writing the number of parses for each sentence:
        with open(treebank_filename, "r") as treebank_file:
            lines = treebank_file.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                #eprint(line)
                my_tree = nltk.Tree.fromstring(line)
                my_root = self.__count_productions_recursively(my_tree)
                if self.start_symbol is None and my_tree is not None:
                    self.start_symbol = my_root.lhs()
        self.hide_some_tokens()

    def hide_some_tokens(self):
        # Sort the dictionary of tokens by the token_count:
        for production in self.count_per_production.keys():
            if self.count_per_production[production] == 0 or self.lhs_count[production.lhs()] == 0:
                self.probability_per_production[production] = 0
            else:
                self.probability_per_production[production] = self.count_per_production[production] / self.lhs_count[production.lhs()]
        
        sorted_productions = sorted(self.probability_per_production.items(), key=operator.itemgetter(1))
        hide_target = int(round(self.hide_proportion * self.token_count, 0))
        count_per_unk_production = {}
        # Look for the least probable productions and "delete" them by reducing their count to 0.
        # Instead, the weight is transferred to an corresponding <UNK> production, 
        # which may pool over several productions that share the same LHS.
        i = 0
        while hide_target > 0:
            production = sorted_productions[i][0]
            if len(production.rhs()) == 1:
                # We have a terminal:
                lhs = production.lhs()
                count = int(sorted_productions[i][1] * self.lhs_count[lhs])
                assert self.count_per_production[production] == count
                hide_target -= count
                # We need to substitute this token production with an <UNK> production.
                unk_production = nltk.Production(lhs, {'<UNK>'})
                # Transfer the weight of this production to the corresponding UNK-production:
                self.count_per_production[production] = 0
                self.probability_per_production[production] = 0
                if unk_production in count_per_unk_production:
                    count_per_unk_production[unk_production] += count
                else:
                    count_per_unk_production[unk_production] = count
            i += 1
        # We couldn't add to or remove from the production collection in the previous iteration, 
        # so we're going to make the necessary insertions now.
        for unk_production in count_per_unk_production.keys():
            self.count_per_production[unk_production] = count_per_unk_production[unk_production]
            if self.count_per_production[unk_production] == 0 or self.lhs_count[unk_production.lhs()] == 0:
                self.probability_per_production[unk_production] = 0
            else:
                self.probability_per_production[unk_production] = self.count_per_production[unk_production] / self.lhs_count[unk_production.lhs()]
        
        # Validation: Double check that we have the same number of tokens both before and after "hiding" tokens.
        count = 0
        for production in self.count_per_production.keys():
            if len(production.rhs()) == 1:
                count += self.count_per_production[production]
        assert count == self.token_count

    def __count_productions_recursively(self, node : nltk.Tree) -> nltk.Nonterminal:
        """Recursively parses a tree representation of a sentence."""
        label = node.label()
        # Traverse the tree:
        if (len(node) == 2):
            # Handle non-leaf nodes:
            left = self.__count_productions_recursively(node[0])
            right = self.__count_productions_recursively(node[1])
            production =  nltk.Production(nltk.Nonterminal(label), [ nltk.Nonterminal(left.lhs()), nltk.Nonterminal(right.lhs()) ])
        else:
            # Handle leaf node.
            token = node[0]
            self.token_count += 1
            if (token not in self.count_per_token):
                self.count_per_token[token] = 1
            else:
                self.count_per_token[token] += 1
            production =  nltk.Production(nltk.Nonterminal(label), [ token ])

        # Update our count of this particular productions.
        if (production not in self.count_per_production):
            self.count_per_production[production] = 1
        else:
            self.count_per_production[production] += 1
        # Update our count of all productions with a particular LHS.
        lhs = production.lhs()
        if (lhs not in self.lhs_count):
            self.lhs_count[lhs] = 1
        else:
            self.lhs_count[lhs] += 1
        return production

    def generate_pcfg(self):
        """Writes the PCFG to STDOUT."""

        # Bling: Sort the production rules.
        sorted_productions = sorted(self.count_per_production)

        # Ew, gross: Print productions starting with the start_symbol, first.
        for production in sorted_productions:
            if production.lhs() == self.start_symbol and self.probability_per_production[production] != 0:
                print(production, '[' + str(self.probability_per_production[production]) + ']')

        # Print the rest of the productions rules.
        for production in sorted_productions:
            if production.lhs() != self.start_symbol and self.probability_per_production[production] != 0:
                print(production, '[' + str(self.probability_per_production[production]) + ']')
        
def main():
    # Parse the command line arguments.
    # If none are provided, use the SVM classifier.
    parser = argparse.ArgumentParser(description='Code to induce the PCFG')
    parser.add_argument('treebank_filename'
                        , type=str
                        , help='The name of the file holding the parsed sentences, one parse per line, in Chomsky Normal Form.'
                        )
    parser.add_argument('hide_proportion'
                        , type=float
                        , help='A float between 0 and 1 that changes the percentage of words to replace with the <UNK> tag.'
                        , default=0
                        )
    args = parser.parse_args()
    eprint(args)

    converter = ToPcfg(args.treebank_filename, args.hide_proportion)
    converter.generate_pcfg()


def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    main()
