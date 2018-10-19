import argparse
import nltk
import sys

class ToPcfg(object):
    """Loads example sentences with POS word tags and induces a PCFG from those rules."""
    
    production_count = {}
    lhs_count = {}
    start_symbol = None

    def __init__(self, treebank_filename : str):
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
            production =  nltk.Production(nltk.Nonterminal(label), [ node[0] ])

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
            if (production.lhs() == self.start_symbol):
                print(production, '[' + str(self.production_count[production] / self.lhs_count[production.lhs()]) + ']')

        # Print the rest of the productions rules.
        for production in sorted_productions:
            if (production.lhs() != self.start_symbol):
                print(production, '[' + str(self.production_count[production] / self.lhs_count[production.lhs()]) + ']')
        
def main():
    # Parse the command line arguments.
    # If none are provided, use the SVM classifier.
    parser = argparse.ArgumentParser(description='Code to induce the PCFG')
    parser.add_argument('treebank_filename'
                        , type=str
                        , help='The name of the file holding the parsed sentences, one parse per line, in Chomsky Normal Form.'
                        )
    args = parser.parse_args()
    eprint(args)

    converter = ToPcfg(args.treebank_filename)
    converter.generate_pcfg()


def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    main()
