import argparse
import nltk
import operator
import sys

class ToPcfg(object):
    """Loads example sentences with POS word tags and induces a PCFG from those rules."""
    
    production_count = {}
    lhs_count = {}
    count_per_token = {}
    token_count = 0
    start_symbol = None
    hide_proportion = 0.0

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
        sorted_tokens = sorted(self.count_per_token.items(), key=operator.itemgetter(1))
        hide_target = int(round(self.hide_proportion * self.token_count, 0))
        words_to_substitute = {}
        # Determine which words we should remove and add them to the words_to_substitute lookup.
        i = 0
        while hide_target > 0:
            production = sorted_tokens[i][0]
            count = sorted_tokens[i][1]
            hide_target -= count
            words_to_substitute[production] = count
            i += 1
        unk_production_count = {}
        productions_scheduled_for_removal = []
        substitute_productions = []
        for production in self.production_count.keys():
            if len(production.rhs()) == 1:
                # We have a terminal:
                token = production.rhs()[0]
                if token in words_to_substitute:
                    lhs = production.lhs()
                    # We need to substitute this token production with an <UNK> production.
                    unk_production = nltk.Production(lhs, {'<UNK>'})
                    # Decrease the counter for the number of times this productions was used.
                    production_count = self.production_count[production]
                    self.production_count[production] -= production_count
                    # Instead, increase the counter for the number of times the corresponding UNK-production is used.
                    if unk_production in unk_production_count:
                        unk_production_count[unk_production] += production_count
                    else:
                        unk_production_count[unk_production] = production_count
        for unk_production in unk_production_count.keys():
            self.production_count[unk_production] = unk_production_count[unk_production]
        # Validation
        count = 0
        for production in self.production_count.keys():
            if len(production.rhs()) == 1:
                count += self.production_count[production]
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
        if (production not in self.production_count):
            self.production_count[production] = 1
        else:
            self.production_count[production] += 1
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
        sorted_productions = sorted(self.production_count)

        # Ew: Print productions starting with the start_symbol, first.
        for production in sorted_productions:
            lhs = production.lhs()
            if (lhs == self.start_symbol and self.production_count[production] != 0 and self.lhs_count[lhs] != 0):
                print(production, '[' + str(self.production_count[production] / self.lhs_count[lhs]) + ']')

        # Print the rest of the productions rules.
        for production in sorted_productions:
            lhs = production.lhs()
            if (lhs != self.start_symbol and self.production_count[production] != 0 and  self.lhs_count[lhs] != 0):
                print(production, '[' + str(self.production_count[production] / self.lhs_count[lhs]) + ']')
        
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
