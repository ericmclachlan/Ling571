import argparse
import nltk
import os
import sys
import time

class CnfParser(object):
    """A parser that applies the grammar to find out all available interpretations of a sentence."""

    grammar = None

    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, tokens):
        productions = tokens
        length = len(tokens)

        table = []
        i = 0
        for r_i in range(length):
            table.append([])
            for c_i in range(length + 1):
                if c_i == r_i:
                    # c_i chosen arbitrary out of c_i and r_i (which are equal).
                    table[r_i].append(tokens[c_i])
                elif c_i == i + 1:
                    nonterminals_to_token = set()
                    for p in self.grammar.productions(rhs=tokens[i]):
                        nonterminals_to_token.add(p.lhs())
                    table[r_i].append(nonterminals_to_token)
                elif c_i > i:
                    table[r_i].append(set())
                else:
                    table[r_i].append(None)
            i += 1
        self.print_table(table)

        for c_i in range(2, length + 1):
            for r_i in range(c_i - 2, -1, -1):
                pivot = table[r_i][c_i]
                if pivot is None:
                    continue

                for offset in range(r_i + 1, c_i):

                    left_of_pivot = table[r_i][offset]
                    assert left_of_pivot is not None
                    below_pivot = table[offset][c_i]
                    assert below_pivot is not None

                    for p in self.grammar.productions():
                        rhs = p.rhs()
                        if len(rhs) == 2 and rhs[0] in left_of_pivot and below_pivot is not None and rhs[1] in below_pivot:
                            pivot.add(p.lhs())
                
                pivot.add("*")
                self.print_table(table)
                pivot.remove("*")

                time.sleep(1)

        return None

    def print_table(self, table):
        eprint()
        str_table = []
        for r_i in range(len(table)):
            str_table.append([])
            for c_i in range(len(table[0])):
                if table[r_i][c_i] is None:
                    str_table[r_i].append('')
                elif len(str(table[r_i][c_i])) > 0:
                    str_table[r_i].append(str(table[r_i][c_i]))
                else:
                    str_table[r_i].append('')

        longest_cols = [
            (max([len(str(r_i[i])) for r_i in table]) + 3)
            for i in range(len(table[0]))
        ]
        row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
        for r_i in str_table:
            eprint(row_format.format(*r_i))
 

    def parse_sentence(self, line):
        tokens = nltk.word_tokenize(line)
        print(line)
        no_of_parses = 0
        parses = self.parse(tokens)
        if parses is not None:
            for interpretation in parses:
                print(interpretation)
                no_of_parses += 1
        print('Number of parses: ', no_of_parses)
        print()

    def parse_all_sentences(self, lines):

            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    self.parse_sentence(line)

def main():
    """Calls parse with the parameters passed on the command line."""

    # Input Validation:    
    parser = argparse.ArgumentParser(description='Parses the specified sentences using the specified grammar.')
    parser.add_argument('grammar_file_path', type=str, help='the name of the file containing the grammar.')
    parser.add_argument('sentence_file_path', type=str, help='the name of the file containing the sentences.')
    ns = parser.parse_args()

    # Load the grammar using NLTK:
    rules = nltk.data.load('file://' + ns.grammar_file_path, 'text')
    grammar = nltk.CFG.fromstring(rules)

    # Load the parser using NLTK:
    parser = CnfParser(grammar)
    
     # Iterate over each of the sentences in the sentences file,
    # writing the number of parses for each sentence:
    with open(ns.sentence_file_path, "r") as sentence_file:
        lines = sentence_file.readlines()
        parser.parse_all_sentences(lines)
    
    eprint('Done.')

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    main()
